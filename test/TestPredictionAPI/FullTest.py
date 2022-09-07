import os


classifierToTest = [
    "kn3",
    "kn5",
    "kn7",
    "lsvm",
    "nn",
    "adab",
    "nb",
    "qda",
    "dt",
    "rf",
]
modeToTest = ["default", "FULL", "SELECTED", "REDUCED"]
scalingToTest = ["default", "STANDARD", "MINMAX", "ROBUST"]
samplingToTest = ["default", "NONE", "UNDER", "OVER"]

# test bad classifier
os.system(
    "python SingleTest.py {} {} {} {} {}".format(
        "fake", "default", "default", "default", 422
    )
)

# test bad data mode
os.system(
    "python SingleTest.py {} {} {} {} {}".format(
        "kn3", "fake", "default", "default", 422
    )
)

# test bad scaling method
os.system(
    "python SingleTest.py {} {} {} {} {}".format(
        "kn3", "default", "fake", "default", 422
    )
)

# test bad sampling method
os.system(
    "python SingleTest.py {} {} {} {} {}".format(
        "kn3", "default", "default", "fake", 422
    )
)


for clsId in classifierToTest:
    for dataMode in modeToTest:
        for scalingMethod in scalingToTest:
            for samplingMethod in samplingToTest:
                os.system(
                    "python SingleTest.py {} {} {} {} {}".format(
                        clsId, dataMode, scalingMethod, samplingMethod, 200
                    )
                )
