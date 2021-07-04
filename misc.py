import requests
import json


r = requests.get(MXRDR_PATH)
print(r)

# pobiera informacje na temat konkretnego datasetu
# r = requests.get(MXRDR_PATH + '/api/datasets/:persistentId/?persistentId=doi:10.21989/FK2/ISK06P')
# print(r.json())

# tworzy dataset - nie dziala
data = {
    'upload-file': json.loads(open('dataset-finch1.json').read()),
}
headers = {
    'X-Dataverse-key': API_TOKEN,
}
r = requests.post(MXRDR_PATH + '/api/dataverses/root/datasets', data=data, headers=headers)
print(r)

# tworzy dataverse
# r = requests.post(MXRDR_PATH + '/api/dataverses/root?key=' + API_TOKEN, json=json.loads(open('test.json').read()))
# print(r)