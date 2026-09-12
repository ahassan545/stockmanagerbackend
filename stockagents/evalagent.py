from curses import wrapper
import os
from deepeval import evaluate, settings
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval

class EvalAgent:
    # def __init__(self):
    #     settings.configure_local_model(
    #         model_name=os.environ.get("MODEL"),
    #         base_url=os.environ.get("OPEN_ROUTER_BASE_API"),
    #         api_key=os.environ.get("OPEN_ROUTER_API_KEY"),
    #     )

    @staticmethod
    def evaluate(func):
        def wrapper(*args, **kwargs):
            print("Before calling the function.")

            result = func(*args, **kwargs)

            pulled_data = ','.join([i.summary for i in args[1][0]])
            sentiment_logic_metric = GEval(
                name="Sentiment Validity",
                criteria="Assess whether the 'actual_output' sentiment score logically aligns with the text provided in the 'input'.",
                evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
                threshold=0.7
            )

            test_case = LLMTestCase(
                input=pulled_data,   
                actual_output=result.sentiment_score,
                retrieval_context=[pulled_data]
            )
            
            results = evaluate(
                test_cases=[test_case],
                metrics=[sentiment_logic_metric]
            )
            
            for decision in results:
                print(f"Metric: {decision[1][0].metrics_data[0].name} | Passed: {decision[1][0].metrics_data[0].success} | Score: {decision[1][0].metrics_data[0].score}")
                if not decision[1][0].metrics_data[0].success:
                    print(f"Reason for low quality: {decision[1][0].metrics_data[0].reason}")
            
            return result
        return wrapper

