from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import logging
from machinelearning.modelmanager import ModelManager

logger = logging.getLogger(__name__)

class LinearRegressionModel:
    def __init__(self, name: str = None):
        self.name: str =self.__module__.split('.')[-1] if not name else name
        self.regr: LinearRegression = self._load()

    def predict(self, data):
        if not self.regr:
            self.regr = self._load()        

        return self.regr.predict(data)
    
    def train(self, data):
        with ModelManager(self.regr, self.name):
            for ticker, X, y in data:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
                self.regr.fit(X_train, y_train)

                self.regr.predict(X_test)

                logging.info(f"Trained model for ticker {ticker}.")

    def _load(self):
        try:
            return ModelManager.load(self.name)
        except Exception as ex:
            logger.info(f"failed to load model with err: [{ex.message}].")

        return LinearRegression()