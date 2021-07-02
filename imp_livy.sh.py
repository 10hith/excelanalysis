import json, pprint, requests, textwrap



host = 'http://11.15.93.81:8998'
data = {'kind': 'pyspark'}
headers = {'Content-Type': 'application/json'}

data = {'kind': 'pyspark'}
r = requests.post(host + '/sessions', data=json.dumps(data), headers=headers)
print(r.text)