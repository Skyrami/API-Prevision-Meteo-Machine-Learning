import os, sys, json, requests


# définition du suelette des résultats
output = """
============================
    Prediction test
============================

request done at "/datascientest/rainproject/classifier/{classifierId}/predict"
| data_mode="{dataMode}"
| scaling_method="{scalingMethod}"
| sampling_method="{samplingMethod}"

with data = "{body}"


actual response = {response_body}

actual status code = {response_status_code}
expected status code = {expected_status_code}

==>  test status: {test_status}
==>  test body: {test_body}

"""


# définition de l'adresse de l'API
api_address = os.getenv("API_ADDRESS")
if api_address is None:
    raise Exception("Missing API_ADDRESS in environment variables")


# port de l'API
api_port = os.getenv("API_PORT")
if api_port is None:
    raise Exception("Missing API_PORT in environment variables")


# récupération des informations à tester
if len(sys.argv) < 5:
    raise Exception("Missing parameters")

if sys.argv[1] is None:
    raise Exception("Missing classifier ID")
else:
    classifier_id = sys.argv[1]

if sys.argv[2] is None:
    raise Exception("Missing data mode")
else:
    dataMode = sys.argv[2]
    if dataMode == "default":
        dataMode = None

if sys.argv[3] is None:
    raise Exception("Missing scaling method")
else:
    scalingMethod = sys.argv[3]
    if scalingMethod == "default":
        scalingMethod = None

if sys.argv[4] is None:
    raise Exception("Missing sampling method")
else:
    samplingMethod = sys.argv[4]
    if samplingMethod == "default":
        samplingMethod = None

if sys.argv[5] is None:
    raise Exception("Missing expected result")
else:
    expected_status_code = int(sys.argv[5])


# request body
request_body = {
    "WindGustSpeed": 35.0,
    "WindSpeed9am": 11.0,
    "WindSpeed3pm": 17.0,
    "Humidity9am": 65.0,
    "Humidity3pm": 56.0,
    "Evaporation": 8.8,
    "MinTemp": 20.4,
    "MaxTemp": 26.4,
    "Pressure9am": 1013.4,
    "Pressure3pm": 1010.7,
    "Rainfall": 0.0,
    "Sunshine": 11.3,
    "Temp9am": 22.9,
    "Temp3pm": 23.0,
    "Location": "Perth",
    "Cloud9am": 3,
    "Cloud3pm": 4,
    "WindGustDir": "SW",
    "WindDir9am": "SSW",
    "WindDir3pm": "WSW",
    "RainToday": "No",
    "Date": "2017-02-20",
}


# requête
r = requests.post(
    url="http://{address}:{port}/datascientest/rainproject/classifier/{classifier}/predict?".format(
        address=api_address,
        port=api_port,
        classifier=classifier_id,
    ),
    params={
        "data_mode": dataMode,
        "scaling_method": scalingMethod,
        "sampling_method": samplingMethod,
    },
    headers={
        "auth-token": "Ym9iOmJ1aWxkZXI=",
    },
    json=request_body,
)


# statut de la requête
response_status_code = r.status_code
response_body = json.loads(r.text)

# test status code
if response_status_code == expected_status_code:
    test_status = "SUCCESS"
else:
    test_status = "FAILURE"

# test response body structure
if expected_status_code == 422:
    test_body = "NA"
else:
    if response_body["RainTomorrow"] is not None and (
        response_body["RainTomorrow"] == "Yes" or response_body["RainTomorrow"] == "No"
    ):
        test_body = "SUCCESS"
    else:
        test_body = "FAILURE"

# affichage des résultats
if test_status == "SUCCESS" and (test_body == "SUCCESS" or test_body == "NA"):
    print(
        "{} + {} + {} + {} = SUCCESS".format(
            classifier_id, dataMode, scalingMethod, samplingMethod
        )
    )
else:
    print(
        "{} + {} + {} + {} = FAILURE".format(
            classifier_id, dataMode, scalingMethod, samplingMethod
        )
    )

# impression dans un fichier
log_file = "/home/tester/log/api_test.log"
with open(log_file, "a") as file:
    file.write(
        output.format(
            classifierId=classifier_id,
            dataMode=dataMode,
            scalingMethod=scalingMethod,
            samplingMethod=samplingMethod,
            body=request_body,
            response_body=response_body,
            response_status_code=response_status_code,
            expected_status_code=expected_status_code,
            test_status=test_status,
            test_body=test_body,
        )
    )
