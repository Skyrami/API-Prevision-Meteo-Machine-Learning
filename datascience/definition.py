from enum import Enum
from pydantic import BaseModel


DataMode = Enum(
    "DataMode", [("full", "FULL"), ("selected", "SELECTED"), ("reduced", "REDUCED")]
)


ScalingMethod = Enum(
    "ScalingMethod",
    [("standard", "STANDARD"), ("minmax", "MINMAX"), ("robust", "ROBUST")],
)


SamplingMethod = Enum(
    "SamplingMethod", [("none", "NONE"), ("under", "UNDER"), ("over", "OVER")]
)


ClassifierId = Enum(
    "ClassifierId",
    [
        ("KNeighbors3", "kn3"),
        ("KNeighbors5", "kn5"),
        ("KNeighbors7", "kn7"),
        # ("LogisticRegression", "lr"),
        ("LinearSVM", "lsvm"),
        # ("RBFSVM", "rbfsvm"),
        # ("GaussianProcess", "gp"),
        ("NeuralNet", "nn"),
        ("ADABoost", "adab"),
        ("NaiveBayes", "nb"),
        ("QuadraticDiscriminantAnalysis", "qda"),
        ("DecisionTree", "dt"),
        ("RandomForest", "rf"),
    ],
)

LocationList = Enum(
    "LocationList",
    [
        ("Brisbane", "Brisbane"),
        ("GoldCoast", "GoldCoast"),
        ("Newcastle", "Newcastle"),
        ("Sydney", "Sydney"),
        ("Canberra", "Canberra"),
        ("Melbourne", "Melbourne"),
        ("Adelaide", "Adelaide"),
        ("Perth", "Perth"),
    ],
)

CloudValue = Enum(
    "CloudValue",
    [
        ("0", 0),
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
    ],
)

WindDirection = Enum(
    "WindDirection",
    [
        ("N", "N"),
        ("NNE", "NNE"),
        ("NE", "NE"),
        ("ENE", "ENE"),
        ("E", "E"),
        ("ESE", "ESE"),
        ("SE", "SE"),
        ("SSE", "SSE"),
        ("S", "S"),
        ("SSW", "SSW"),
        ("SW", "SW"),
        ("WSW", "WSW"),
        ("W", "W"),
        ("WNW", "WNW"),
        ("NW", "NW"),
        ("NNW", "NNW"),
    ],
)

YesNo = Enum(
    "YesNo",
    [("Yes", "Yes"), ("No", "No")],
)
    
def getDataModeDescription(dataMode: DataMode):
    if dataMode is DataMode.full:
        return "Full data are used for classification"
    elif dataMode is DataMode.selected:
        return "Only a selection of columns with high correlation to target are kept for classification"
    elif dataMode is DataMode.reduced:
        return "A PCA reduction is performed on full data before classification"
    else:
        raise Exception("Unknown data mode'{}'", dataMode.name)


def getScalingMethodDescription(scalingMethod: ScalingMethod):
    if scalingMethod is ScalingMethod.standard:
        return "Standardize features by removing the mean and scaling to unit variance"
    elif scalingMethod is ScalingMethod.minmax:
        return "Transform features by scaling each feature to a given range"
    elif scalingMethod is ScalingMethod.robust:
        return "Robust scaling features by removing the median and scaling the data by the quantile range "
    else:
        raise Exception("Unknown scaling method '{}'", scalingMethod.name)


def getSamplingMethodDescription(samplingMethod: SamplingMethod):
    if samplingMethod is SamplingMethod.none:
        return "No over/under sampling will be applied before classifier training"
    elif samplingMethod is SamplingMethod.under:
        return "Under sampling will be applied before classifier training"
    elif samplingMethod is SamplingMethod.over:
        return "Over sampling will be applied before classifier training"
    else:
        raise Exception("Unknown sampling method'{}'", samplingMethod.name)


def getClassifierIdDescription(classifierId: ClassifierId):
    if classifierId is ClassifierId.KNeighbors3:
        return "KMeans classifier clusters data by trying to separate samples in 3 groups of equal variance, minimizing a criterion known (the inertia or the sum-of-squares)"
    elif classifierId is ClassifierId.KNeighbors5:
        return "KMeans classifier clusters data by trying to separate samples in 5 groups of equal variance, minimizing a criterion known (the inertia or the sum-of-squares)"
    elif classifierId is ClassifierId.KNeighbors7:
        return "KMeans classifier clusters data by trying to separate samples in 7 groups of equal variance, minimizing a criterion known (the inertia or the sum-of-squares)"
    # elif classifierId is ClassifierId.LogisticRegression:
    #    return ""
    elif classifierId is ClassifierId.LinearSVM:
        return "Linear Support Vector Classification is a linear model that creates a line or hyperplane that separates data into classes"
    # elif classifierId is ClassifierId.RBFSVM:
    #    return ""
    # elif classifierId is ClassifierId.GaussianProcess:
    #    return ""
    elif classifierId is ClassifierId.NeuralNet:
        return "A neural network is a collection of layers, each containing weights that get used alongside its other inputs to produce an output"
    elif classifierId is ClassifierId.ADABoost:
        return "It is called Adaptive Boosting as the weights are re-assigned to each instance, with higher weights assigned to incorrectly classified instances"
    elif classifierId is ClassifierId.NaiveBayes:
        return "A Naive Bayes classifier is a probabilistic machine learning model that’s used for classification task based on the Bayes theorem"
    elif classifierId is ClassifierId.QuadraticDiscriminantAnalysis:
        return "A classifier with a quadratic decision boundary, generated by fitting class conditional densities to the data and using Bayes’ rule"
    elif classifierId is ClassifierId.DecisionTree:
        return "DecisionTreeClassifier is a class capable of performing multi-class classification on a dataset"
    elif classifierId is ClassifierId.RandomForest:
        return "A random forest classifier, each tree in the ensemble is built from a sample drawn with from the training set"
    else:
        raise Exception("Unknown classifier id'{}'", classifierId.name)
