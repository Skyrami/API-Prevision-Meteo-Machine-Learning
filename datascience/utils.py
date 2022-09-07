import numpy as np

# Importation des bibliothèques de resampling
from imblearn.over_sampling import SMOTE, SMOTENC
from imblearn.under_sampling import NearMiss

# Importation des bibliothèques de machine learning
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression

from datascience.definition import ClassifierId, ScalingMethod


def getNumericalColumnList():
    return [
        "WindGustSpeed",
        "WindSpeed9am",
        "WindSpeed3pm",
        "Humidity9am",
        "Humidity3pm",
        "Evaporation",
        "MinTemp",
        "MaxTemp",
        "Pressure9am",
        "Pressure3pm",
        "Rainfall",
        "Sunshine",
        "Temp9am",
        "Temp3pm",
    ]


def getCategoricalColumnList():
    return [
        "Location",
        "Cloud9am",
        "Cloud3pm",
        "WindGustDir",
        "WindDir9am",
        "WindDir3pm",
        "RainToday",
        "Year",
        "Quater",
        "Month",
        "Day",
    ]


def replaceYesAndNo(givenDataframe):
    """
    Method to replace 'YES' and 'NO' string by 1 and 0
    """
    return givenDataframe.replace(to_replace={"No": 0, "Yes": 1})


def replaceWindDirection(givenDataframe):
    """
    Method to replace wind direction (string enum like 'N' or 'SSW') by numerical enum:
    N   -> 1
    NNE -> 2
    NE  -> 3
    ENE -> 4
    E   -> 5
    ESE -> 6
    SE  -> 7
    SSE -> 8
    S   -> 9
    SSW -> 10
    SW  -> 11
    WSW -> 12
    W   -> 13
    WNW -> 14
    NW  -> 15
    NNW -> 16
    """
    return givenDataframe.replace(
        to_replace={
            "N": 1,
            "NNE": 2,
            "NE": 3,
            "ENE": 4,
            "E": 5,
            "ESE": 6,
            "SE": 7,
            "SSE": 8,
            "S": 9,
            "SSW": 10,
            "SW": 11,
            "WSW": 12,
            "W": 13,
            "WNW": 14,
            "NW": 15,
            "NNW": 16,
        }
    )


def replaceLocation(givenDataframe):
    """
    Method to replace location name by numerical enum:
    Brisbane  -> 1
    GoldCoast -> 2
    Newcastle -> 3
    Sydney    -> 4
    Canberra  -> 5
    Melbourne -> 6
    Adelaide  -> 7
    Perth     -> 8
    """
    return givenDataframe.replace(
        to_replace={
            "Brisbane": 1,
            "GoldCoast": 2,
            "Newcastle": 3,
            "Sydney": 4,
            "Canberra": 5,
            "Melbourne": 6,
            "Adelaide": 7,
            "Perth": 8,
        }
    )


def getNotSelectedColumnList():
    return [
        "Location",
        "MinTemp",
        "MaxTemp",
        #'Rainfall',
        "Evaporation",
        #'Sunshine',
        "WindGustDir",
        #'WindGustSpeed',
        "WindDir9am",
        "WindDir3pm",
        "WindSpeed9am",
        "WindSpeed3pm",
        "Humidity9am",
        #'Humidity3pm',
        #'Pressure9am',
        "Pressure3pm",
        "Cloud9am",
        #'Cloud3pm',
        "Temp9am",
        #'Temp3pm',
        "RainToday",
        "Day",
        "Month",
        "Year",
        "Quater",
    ]


def fillNumericalByMedian(dataframe):
    """
    Will replace all NAN from given columns by median value if column is numerical.
    """
    newDataframe = dataframe.copy()
    for attribute in getNumericalColumnList():
        if attribute in dataframe.columns:
            newDataframe[attribute] = newDataframe[attribute].fillna(
                newDataframe[attribute].median()
            )
    return newDataframe


def fillCategoricalByMode(dataframe):
    """
    Will replace all NAN from given columns by mode value if column is categorical.
    """
    newDataframe = dataframe.copy()
    for attribute in getCategoricalColumnList():
        if attribute in dataframe.columns:
            newDataframe[attribute] = newDataframe[attribute].fillna(
                newDataframe[attribute].mode()[0]
            )
    return newDataframe


def getScaler(scalingMethod: ScalingMethod):
    if scalingMethod is ScalingMethod.standard:
        return StandardScaler()
    elif scalingMethod is ScalingMethod.minmax:
        return MinMaxScaler()
    elif scalingMethod is ScalingMethod.robust:
        return RobustScaler()
    else:
        raise Exception("Unknown scaling method '{}'", scalingMethod.name)


def getPCA(scalingMethod: ScalingMethod):
    if scalingMethod is ScalingMethod.standard:
        return PCA(n_components=9)
    elif scalingMethod is ScalingMethod.minmax:
        return PCA(n_components=7)
    elif scalingMethod is ScalingMethod.robust:
        return PCA(n_components=7)
    else:
        raise Exception("Unknown scaling method '{}'", scalingMethod.name)


def doUnderSampling(XCandidate, yCandidate):
    undersample = NearMiss(version=1, n_neighbors=3)
    return undersample.fit_resample(XCandidate, yCandidate)


def doOverSampling(XCandidate, yCandidate):
    """
    Do oversampling on given data and returned new oversampled data
    Use SMOTE method, or SMOTENC if there is categorical columns
    """
    # Check if there is categorical data in given dataframe
    categoricalIndices = []
    if type(XCandidate) is not np.ndarray:
        for cat in getCategoricalColumnList():
            if cat in XCandidate.columns:
                categoricalIndices.append(XCandidate.columns.get_loc(cat))

    # Warn: Do not use SMOTE when there is categorical data, call SMOTENC instead
    if len(categoricalIndices) == 0:
        sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    else:
        sm = SMOTENC(
            categorical_features=categoricalIndices,
            k_neighbors=3,
            sampling_strategy=0.75,
        )

    # Do oversampling and return new X and y
    XSmote, ySmote = sm.fit_resample(XCandidate, yCandidate)
    return XSmote, ySmote


def getClassifier(classifierId: ClassifierId):
    if classifierId is ClassifierId.KNeighbors3:
        return KNeighborsClassifier(3)
    elif classifierId is ClassifierId.KNeighbors5:
        return KNeighborsClassifier(5)
    elif classifierId is ClassifierId.KNeighbors7:
        return KNeighborsClassifier(7)
    # elif classifierId is ClassifierId.LogisticRegression:
    #    return LogisticRegression(solver="newton-cg", max_iter=1000)
    elif classifierId is ClassifierId.LinearSVM:
        return SVC(kernel="linear", C=0.025)
    # elif classifierId is ClassifierId.RBFSVM:
    #    return SVC(gamma=2, C=1)
    # elif classifierId is ClassifierId.GaussianProcess:
    #    return GaussianProcessClassifier(1.0 * RBF(1.0))
    elif classifierId is ClassifierId.NeuralNet:
        return MLPClassifier(alpha=1, max_iter=1000)
    elif classifierId is ClassifierId.ADABoost:
        return AdaBoostClassifier()
    elif classifierId is ClassifierId.NaiveBayes:
        return GaussianNB()
    elif classifierId is ClassifierId.QuadraticDiscriminantAnalysis:
        return QuadraticDiscriminantAnalysis()
    elif classifierId is ClassifierId.DecisionTree:
        return DecisionTreeClassifier(max_depth=5)
    elif classifierId is ClassifierId.RandomForest:
        return RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
    else:
        raise Exception("Unknown classifier id'{}'", classifierId.name)
