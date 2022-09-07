import os, joblib
import pandas as pd
import datascience.utils as utils
from datascience.loader import trainingDataLoader
from datascience.definition import DataMode, ScalingMethod


class DataPreparer:
    def __init__(
        self,
        dataMode: DataMode = DataMode.full,
        scalingMethod: ScalingMethod = ScalingMethod.standard,
    ):

        self.dataMode = dataMode
        self.scalingMethod = scalingMethod

        self.name = "{}.{}".format(
            self.dataMode.name,
            self.scalingMethod.name,
        ).lower()

        self.dataPrepFile = os.path.join(
            os.path.dirname(__file__),
            "saved/dataprep/{}.z".format(self.name),
        ).lower()
        os.makedirs(os.path.dirname(self.dataPrepFile), exist_ok=True)

        self.scaler = None
        self.pca = None
        self.trainingData = None
        self.trainingTarget = None
        self.loaded = False

    def __str__(self):
        return self.name

    def load(self):
        if os.path.exists(self.dataPrepFile):
            self.scaler, self.pca, self.trainingData, self.trainingTarget = joblib.load(
                self.dataPrepFile
            )
            self.loaded = True

    def fit_and_save(self):
        trainingTarget, trainingData = trainingDataLoader.get()

        # Apply scaler
        numData = trainingData[utils.getNumericalColumnList()]
        catData = trainingData[utils.getCategoricalColumnList()]
        if numData.shape[1] + catData.shape[1] != trainingData.shape[1]:
            print("full data", trainingData.shape)
            print("numerical data", numData.shape)
            print("categorical data", catData.shape)
            raise Exception("Some data seem to be lost...")
        self.scaler = utils.getScaler(self.scalingMethod)
        scaledNumData = pd.DataFrame(
            self.scaler.fit_transform(numData),
            index=numData.index,
            columns=numData.columns,
        )
        trainingData = pd.merge(
            left=scaledNumData, right=catData, left_index=True, right_index=True
        )

        # Apply column selection or PCA
        if self.dataMode is DataMode.selected:
            trainingData = trainingData.drop(utils.getNotSelectedColumnList(), axis=1)
        elif self.dataMode is DataMode.reduced:
            self.pca = utils.getPCA(self.scalingMethod)
            trainingData = self.pca.fit_transform(trainingData)

        # save transformed training data for future classifier training
        self.trainingData = trainingData
        self.trainingTarget = trainingTarget

        # Remove previously saved preparer
        if os.path.exists(self.dataPrepFile):
            os.remove(self.dataPrepFile)

        # Save current execution of preparer
        joblib.dump(
            (self.scaler, self.pca, self.trainingData, self.trainingTarget),
            self.dataPrepFile,
        )

    def getPreparedTrainingData(self):
        return self.trainingTarget, self.trainingData

    def transform(self, userData: pd.DataFrame):
        if userData is None:
            raise Exception("Cannot transform NULL data...")
        if self.scaler is None:
            raise Exception("Data preparer was not fitted yet...")
        if self.dataMode is DataMode.reduced and self.pca is None:
            raise Exception("Data preparer was not fitted yet...")

        # Replace None by Median/Mode
        if userData.isnull().sum().sum() > 0:
            for column in utils.getNumericalColumnList():
                userData[column] = userData[column].fillna(
                    self.trainingData[column].median()
                )
            for column in utils.getCategoricalColumnList():
                userData[column] = userData[column].fillna(
                    self.trainingData[column].mode()[0]
                )

        numData = userData[utils.getNumericalColumnList()]
        catData = userData[utils.getCategoricalColumnList()]
        scaledNumData = pd.DataFrame(
            self.scaler.transform(numData),
            index=numData.index,
            columns=numData.columns,
        )
        transformed = pd.merge(
            left=scaledNumData,
            right=catData,
            left_index=True,
            right_index=True,
        )
        if self.dataMode is DataMode.selected:
            transformed = transformed.drop(utils.getNotSelectedColumnList(), axis=1)
        elif self.dataMode is DataMode.reduced:
            transformed = self.pca.transform(userData)

        return transformed
