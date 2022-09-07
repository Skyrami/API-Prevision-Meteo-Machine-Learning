import os, requests


# définition de l'adresse de l'API
api_address = os.getenv("API_ADDRESS")
if api_address is None:
    raise Exception("Missing API_ADDRESS in environment variables")


# port de l'API
api_port = os.getenv("API_PORT")
if api_port is None:
    raise Exception("Missing API_PORT in environment variables")

# définition du squelette des résultats
output = """
============================
    Status test
============================

request done at "/datascientest/rainproject/{statusVerb}"

actual response = {response_body}
actual status code = {response_status_code}
expected status code = {expected_status_code}

==>  test result: {test_result}

"""


# test ping request
r = requests.get(
    url="http://{address}:{port}/datascientest/rainproject/ping".format(
        address=api_address,
        port=api_port,
    ),
)

# statut de la requête
response_status_code = r.status_code
response_body = r.text


# test ping response
if response_status_code == 200 and response_body == "1":
    test_result = "SUCCESS"
else:
    test_result = "FAILURE"
print("Ping = {}".format(test_result))


# impression dans un fichier
log_file = "/home/tester/log/api_test.log"
with open(log_file, "a") as file:
    file.write(
        output.format(
            statusVerb="ping",
            response_body=response_body,
            response_status_code=response_status_code,
            expected_status_code="200",
            test_result=test_result,
        )
    )


# test healthcheck request
r = requests.get(
    url="http://{address}:{port}/datascientest/rainproject/healthcheck".format(
        address=api_address,
        port=api_port,
    ),
)

# statut de la requête
response_status_code = r.status_code
response_body = r.text


# test ping response
if response_status_code == 200 and response_body == "1":
    test_result = "SUCCESS"
else:
    test_result = "FAILURE"
print("HealthCheck = {}".format(test_result))


# impression dans un fichier
log_file = "/home/tester/log/api_test.log"
with open(log_file, "a") as file:
    file.write(
        output.format(
            statusVerb="healthcheck",
            response_body=response_body,
            response_status_code=response_status_code,
            expected_status_code="200",
            test_result=test_result,
        )
    )
