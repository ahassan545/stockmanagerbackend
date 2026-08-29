import mlflow
import os
import shutil
STATIC_PATH = "./machinelearning/staticmodels"

mlflow.set_tracking_uri(os.environ.get("TRACKING_URL"))
mlflow.sklearn.autolog()

class ModelManager:
    def __init__(self, model, name) -> None:
        self.model = model
        self.location = f"{STATIC_PATH}/{name}"
        self.run_name = name

    @staticmethod   
    def load(name) -> any:
        return mlflow.sklearn.load_model(f"{STATIC_PATH}/{name}")

    def __enter__(self):
        return mlflow.start_run(run_name=self.run_name)

    def __exit__(self, exc_type, exc_value, traceback):
        if os.path.exists(self.location):
            shutil.rmtree(self.location)
        mlflow.sklearn.save_model(self.model, path=self.location)