from datascience.definition import ClassifierId, DataMode, ScalingMethod, SamplingMethod
from datascience.classifier import DataClassifier


def loadAllClassifier():
    maxF1 = 0
    maxF1ClsName = None
    for clsId in ClassifierId:
        for dataMode in DataMode:
            for scalingMethod in ScalingMethod:
                for samplingMethod in SamplingMethod:
                    classifier = DataClassifier(
                        clsId, dataMode, scalingMethod, samplingMethod
                    )
                    classifier.load()
                    if not classifier.loaded:
                        classifier.fit_and_save()
                    if classifier.stats["F1Score"] > maxF1:
                        maxF1 = classifier.stats["F1Score"]
                        maxF1ClsName = classifier.name
    print("Best F1 score = {} and is {}".format(maxF1, maxF1ClsName))


# To initialize all classifiers if needed
if __name__ == "__main__":
    loadAllClassifier()
