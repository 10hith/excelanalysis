import requests
import pandas as pd
# import databricks.koalas as ks
import json

import plotly.express as px

session = requests.Session()
session.trust_env = False

x=session.get("http://11.15.93.81:8000/notes/");

hist = pd.read_csv("histogram.csv").fillna("unknown")

# ks_df=ks.from_pandas(hist)

# Creating Json in the format expected by fastapi
hist_json=hist.to_json(orient='records')

# print(hist_json)


# # Testing POST
# x=session.post("http://11.15.93.81:8000/htgrm/", data=hist_json);
# print(x.status_code)
# print(x.text)


''' Setting Cookies
'''
x=session.post(f"http://11.15.93.81:8000/set-cookie/basal123");
print(x.status_code)
print(x.text)





''' Getting json data and converting to pandas df
'''
# x=session.get("http://11.15.93.81:8000/htgrm/");
# print(x.status_code)
# htgrm_json = x.text
#
# print(f"{x.text=='[]'}")
# print(f"the length is {len(x.text)}")
#
# new_pdf=pd.read_json(htgrm_json)
# print(new_pdf.head(15))

'''
spark example
'''

# json_rdd = sc.parallelize([response.text])
# spark.read.json(json_rdd)

'''
Notes example
'''
# session = requests.Session()
# session.trust_env = False
#
# x=session.get("http://11.15.93.81:8000/notd es/");
#
# payload = [{
#   "text": "payload_part01",
#   "completed": False
# },
#     {
#         "text": "payload_part02",
#         "completed": False
#     }
# ]
#
# data = {'text': ['3', '2', '1', '0'], 'completed': [True, True, True, True]}
# pdf = pd.DataFrame.from_dict(data)
#
# pdf_json= pdf.to_json(orient='records')
#
# print(pdf_json)
#
#
# # #
# x=session.post("http://11.15.93.81:8000/multiple-notes/", data=pdf_json);
# print(x.status_code)
# print(x.text)