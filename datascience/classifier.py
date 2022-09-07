import os, time, joblib
import pandas as pd
import datascience.utils as utils
from datascience.preparer import DataPreparer
from datascience.definition import ClassifierId, DataMode, ScalingMethod, SamplingMethod
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from sklearn.model_selection import cross_validate


class DataClassifier:
    def __init__(
        self,
        classifierId: ClassifierId,
        dataMode: DataMode = DataMode.full,
        scalingMethod: ScalingMethod = ScalingMethod.standard,
        samplingMethod: SamplingMethod = SamplingMethod.none,
    ):
        self.classifierId = classifierId
        self.dataMode = dataMode
        self.scalingMethod = scalingMethod
        self.samplingMethod = samplingMethod

        self.name = "{}.{}.{}.{}".format(
            self.dataMode.name,
            self.scalingMethod.name,
            self.samplingMethod.name,
            self.classifierId.name,
        ).lower()

        self.classifierFile = os.path.join(
            os.path.dirname(__file__),
            "saved/{}/{}.z".format(self.classifierId.name, self.name),
        )
        os.makedirs(os.path.dirname(self.classifierFile), exist_ok=True)

        self.dataPreparer = DataPreparer(self.dataMode, self.scalingMethod)
        self.classifier = utils.getClassifier(self.classifierId)
        self.stats = None
        self.loaded = False

    def __str__(self):
        return self.name

    def load(self):
        # First load data preparer
        self.dataPreparer.load()
        if not self.dataPreparer.loaded:
            print("Data Preparer not loaded".format(self.dataPreparer.name))
            return
        # Then load the classifier itself, or train it if needed
        if os.path.exists(self.classifierFile):
            self.classifier, self.stats = joblib.load(self.classifierFile)
            self.loaded = True

    def fit_and_save(self):
        # Fit data preparer if needed
        if not self.dataPreparer.loaded:
            self.dataPreparer.fit_and_save()

        # Retrieve prepared data for training
        trainingTarget, trainingData = self.dataPreparer.getPreparedTrainingData()

        # Do resampling if needed
        if self.samplingMethod is SamplingMethod.over:
            trainingData, trainingTarget = utils.doOverSampling(
                trainingData, trainingTarget
            )
        elif self.samplingMethod is SamplingMethod.under:
            trainingData, trainingTarget = utils.doUnderSampling(
                trainingData, trainingTarget
            )

        # computing cross val
        scores = cross_validate(
            self.classifier,
            trainingData,
            trainingTarget,
            cv=5,
            scoring=(
                "accuracy",
                "balanced_accuracy",
                "average_precision",
                "f1",
                "precision",
                "recall",
                "jaccard",
                "roc_auc",
            ),
            return_train_score=False,
            error_score="raise",
        )

        # Compute and save classifier score
        self.stats = {}
        self.stats["Accuracy"] = scores["test_accuracy"].mean()
        self.stats["BalancedAccuracy"] = scores["test_balanced_accuracy"].mean()
        self.stats["AveragePrecision"] = scores["test_average_precision"].mean()
        self.stats["F1Score"] = scores["test_f1"].mean()
        self.stats["Precision"] = scores["test_precision"].mean()
        self.stats["Recall"] = scores["test_recall"].mean()
        self.stats["Jaccard"] = scores["test_jaccard"].mean()
        self.stats["ROC-AUC"] = scores["test_roc_auc"].mean()

        # Final training with full data
        self.classifier.fit(trainingData, trainingTarget)

        # Remove previously saved classifier
        if os.path.exists(self.classifierFile):
            os.remove(self.classifierFile)

        # Save current execution of classifier
        joblib.dump((self.classifier, self.stats), self.classifierFile)

    def predict(self, userData: pd.DataFrame):
        if userData is None:
            raise Exception("Cannot predict NULL data...")
        if userData.shape[0] != 1:
            raise Exception("Invalid user Data. Only one prediction at a time...")
        if self.dataPreparer is None or self.classifier is None:
            raise Exception("Classifier not loaded")
        return self.classifier.predict(self.dataPreparer.transform(userData))
