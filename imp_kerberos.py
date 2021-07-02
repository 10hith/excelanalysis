import requests
r = requests.get("http://ldapsf5europapt.web.rbsgrp.net")
print(r.status_code)
print(r.content)
# 401


import requests
from requests_kerberos import HTTPKerberosAuth, REQUIRED


kerberos_auth = HTTPKerberosAuth(principal="basal@EUROPA.RBSGRP.NET")
requests.get("http://ldapsf5europapt.web.rbsgrp.net", auth=kerberos_auth)