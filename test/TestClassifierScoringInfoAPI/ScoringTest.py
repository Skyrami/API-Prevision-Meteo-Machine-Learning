import requests
import os

# définition de l'adresse de l'API
api_address = os.getenv("API_ADDRESS")
if api_address is None:
    raise Exception("Missing API_ADDRESS in environment variables")


# port de l'API
api_port = os.getenv("API_PORT")
if api_port is None:
    raise Exception("Missing API_PORT in environment variables")
    
# numéro du classifier souhaité
classifier_id = "kn3"

# TEST 1
# requête
r = requests.get(
    url="http://{address}:{port}/datascientest/rainproject/classifier/{id}".format(
        address=api_address, port=api_port, id=classifier_id
    ),
    headers={'auth-token': 'YWxpY2U6d29uZGVybGFuZA=='},
    params={
        'data_mode': 'FULL',
        'scaling_method': 'STANDARD',
        'sampling_method': 'NONE'
    }
)

output = """
============================
    Classifier Info Scoring Test
============================

request done at "/datascientest/rainproject/classifier/classifier_id"

expected result = 200
actual restult = {status_code}

==>  {test_status}

"""


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 200:
    test_status = "SUCCESS"
else:
    test_status = "FAILURE"
print(output.format(status_code=status_code, test_status=test_status))

# impression dans un fichier
if test_status == "SUCCESS":
    output = output.format(status_code=status_code, test_status=test_status)
    with open("/home/tester/log/api_test.log", "a") as file:
        file.write(output)


#--------------------------------------------------------------------------------------------------------


# numéro du classifier souhaité
classifier_id = "qda"

# TEST 2
# requête
r = requests.get(
    url="http://{address}:{port}/datascientest/rainproject/classifier/{id}".format(
        address=api_address, port=api_port, id=classifier_id
    ),
    headers={'auth-token': 'YWxpY2U6d29uZGVybGFuZA=='},
    params={
        'data_mode': 'FULL',
        'scaling_method': 'ROBUST',
        'sampling_method': 'OVER'
    }
)

output = """
============================
    Classifier Info Scoring Test
============================

request done at "/datascientest/rainproject/classifier/classifier_id"

expected result == 200
actual restult = {status_code}

==>  {test_status}

"""


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 200:
    test_status = "SUCCESS"
else:
    test_status = "FAILURE"
print(output.format(status_code=status_code, test_status=test_status))

# impression dans un fichier
if test_status == "SUCCESS":
    output = output.format(status_code=status_code, test_status=test_status)
    with open("/home/tester/log/api_test.log", "a") as file:
        file.write(output)




#------------------------------------------------------------------------------------------------

# numéro du classifier souhaité
classifier_id = "nn"

# TEST 3
# requête
r = requests.get(
    url="http://{address}:{port}/datascientest/rainproject/classifier/{id}".format(
        address=api_address, port=api_port, id=classifier_id
    ),
    headers={'auth-token': 'YWxpY2U6d29uZGVybGFuZA=='},
    params={
        'data_mode': 'REDUCED',
        'scaling_method': 'MINMAX',
        'sampling_method': 'UNDER'
    }
)

output = """
============================
    Classifier Info Scoring Test
============================

request done at "/datascientest/rainproject/classifier/classifier_id"

expected result == 200
actual restult = {status_code}

==>  {test_status}

"""


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 200:
    test_status = "SUCCESS"
else:
    test_status = "FAILURE"
print(output.format(status_code=status_code, test_status=test_status))

# impression dans un fichier
if test_status == "SUCCESS":
    output = output.format(status_code=status_code, test_status=test_status)
    with open("/home/tester/log/api_test.log", "a") as file:
        file.write(output)
