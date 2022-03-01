import requests

url = "https://dg-sandbox.setu.co/api/verify/ban/async/02c2dc4c-1015-4ea0-8ec4-987829fc70cc"

payload={}
headers = {
  'x-client-id': 'test-client',
  'x-client-secret': '891707ee-d6cd-4744-a28d-058829e30f12'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)