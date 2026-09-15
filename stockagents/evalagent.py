from curses import wrapper
import os
from deepeval import evaluate, settings
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval
import logging

logger = logging.getLogger(__name__)


class EvalAgent:
    @staticmethod
    def evaluate(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            pulled_data = ",".join([i.summary for i in args[1][0]])
            sentiment_logic_metric = GEval(
                name="Sentiment Validity",
                criteria="Assess whether the 'actual_output' sentiment score logically aligns with the text provided in the 'input'.",
                evaluation_params=[
                    SingleTurnParams.INPUT,
                    SingleTurnParams.ACTUAL_OUTPUT,
                ],
                threshold=0.7,
            )

            test_case = LLMTestCase(
                input=pulled_data,
                actual_output=str(result.sentiment_score),
                retrieval_context=[pulled_data],
            )

            results = evaluate(
                async_config=AsyncConfig(),
                test_cases=[test_case],
                metrics=[sentiment_logic_metric],
            )

            metric_data = results.dict()["test_results"][0]["metrics_data"][0]
            logger.info(
                f"Metric: {metric_data['name']} | Passed: {metric_data['success']} | Score: {metric_data['score']}"
            )
            if not metric_data["success"]:
                raise ValueError(
                    f"Invalid Sentiment. Reason for low quality: {metric_data['reason']}"
                )

            return result

        return wrapper
