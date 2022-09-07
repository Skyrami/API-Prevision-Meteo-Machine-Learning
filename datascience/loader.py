import os, math
import pandas as pd
from pydantic import BaseModel

import datascience.utils as utils
from datascience.definition import LocationList, CloudValue, WindDirection, YesNo


class TrainingDataLoader:
    def __init__(self):
        self.fullTrainingTarget = self.fullTrainingData = None

    def __load(self):
        # Data stored locally in case it stop being accessible at 'https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/rains.csv'
        print("LOAD TRAINING DATA !")
        dataframe = pd.read_csv(
            os.path.join(os.path.dirname(__file__), "data/rains.csv")
        )
        dataframe = dataframe.dropna(subset=["RainTomorrow"])
        dataframe = utils.fillNumericalByMedian(dataframe)
        dataframe = utils.fillCategoricalByMode(dataframe)
        dataframe["WindGustDir"] = utils.replaceWindDirection(dataframe["WindGustDir"])
        dataframe["WindDir9am"] = utils.replaceWindDirection(dataframe["WindDir9am"])
        dataframe["WindDir3pm"] = utils.replaceWindDirection(dataframe["WindDir3pm"])
        dataframe["Location"] = utils.replaceLocation(dataframe["Location"])
        dataframe["RainToday"] = utils.replaceYesAndNo(dataframe["RainToday"])
        dataframe["RainTomorrow"] = utils.replaceYesAndNo(dataframe["RainTomorrow"])
        dataframe["Day"] = dataframe["Date"].apply(lambda date: int(date.split("-")[2]))
        dataframe["Month"] = dataframe["Date"].apply(
            lambda date: int(date.split("-")[1])
        )
        dataframe["Year"] = dataframe["Date"].apply(
            lambda date: int(date.split("-")[0])
        )
        dataframe["Quater"] = dataframe["Date"].apply(
            lambda date: 1 + math.floor((int(date.split("-")[1]) - 1) / 3)
        )
        self.fullTrainingTarget = dataframe["RainTomorrow"]
        self.fullTrainingData = dataframe.drop(["Date", "RainTomorrow"], axis=1)

    def get(self):
        if self.fullTrainingTarget is None or self.fullTrainingData is None:
            self.__load()
        return self.fullTrainingTarget, self.fullTrainingData


trainingDataLoader = TrainingDataLoader()


class UserData(BaseModel):
    WindGustSpeed: float = None
    WindSpeed9am: float = None
    WindSpeed3pm: float = None
    Humidity9am: float = None
    Humidity3pm: float = None
    Evaporation: float = None
    MinTemp: float = None
    MaxTemp: float = None
    Pressure9am: float = None
    Pressure3pm: float = None
    Rainfall: float = None
    Sunshine: float = None
    Temp9am: float = None
    Temp3pm: float = None
    Location: LocationList
    Cloud9am: CloudValue = None
    Cloud3pm: CloudValue = None
    WindGustDir: WindDirection = None
    WindDir9am: WindDirection = None
    WindDir3pm: WindDirection = None
    RainToday: YesNo = None
    Date: str

    def getAsDataFrame(self):
        dataframe = pd.DataFrame(
            {
                "WindGustSpeed": [self.WindGustSpeed],
                "WindSpeed9am": [self.WindSpeed9am],
                "WindSpeed3pm": [self.WindSpeed3pm],
                "Humidity9am": [self.Humidity9am],
                "Humidity3pm": [self.Humidity3pm],
                "Evaporation": [self.Evaporation],
                "MinTemp": [self.MinTemp],
                "MaxTemp": [self.MaxTemp],
                "Pressure9am": [self.Pressure9am],
                "Pressure3pm": [self.Pressure3pm],
                "Rainfall": [self.Rainfall],
                "Sunshine": [self.Sunshine],
                "Temp9am": [self.Temp9am],
                "Temp3pm": [self.Temp3pm],
                "Location": [self.Location.name if self.Location is not None else None],
                "Cloud9am": [self.Cloud9am.name if self.Cloud9am is not None else None],
                "Cloud3pm": [self.Cloud3pm.name if self.Cloud3pm is not None else None],
                "WindGustDir": [
                    self.WindGustDir.name if self.WindGustDir is not None else None
                ],
                "WindDir9am": [
                    self.WindDir9am.name if self.WindDir9am is not None else None
                ],
                "WindDir3pm": [
                    self.WindDir3pm.name if self.WindDir3pm is not None else None
                ],
                "RainToday": [
                    self.RainToday.name if self.RainToday is not None else None
                ],
                "Day": [self.Date.split("-")[2]],
                "Month": [self.Date.split("-")[1]],
                "Year": [self.Date.split("-")[0]],
                "Quater": [1 + math.floor((int(self.Date.split("-")[1]) - 1) / 3)],
            }
        )
        dataframe["WindGustDir"] = utils.replaceWindDirection(dataframe["WindGustDir"])
        dataframe["WindDir9am"] = utils.replaceWindDirection(dataframe["WindDir9am"])
        dataframe["WindDir3pm"] = utils.replaceWindDirection(dataframe["WindDir3pm"])
        dataframe["Location"] = utils.replaceLocation(dataframe["Location"])
        dataframe["RainToday"] = utils.replaceYesAndNo(dataframe["RainToday"])
        return dataframe
