alias pycharm="nohup /opt/pycharm-community-2021.1.3/bin/pycharm.sh </dev/null &>/dev/null &"
alias intellij="nohup /opt/idea-IC-211.7628.21/bin/idea.sh </dev/null &>/dev/null &"

# Add this to the bashrc file
export DISPLAY=192.168.1.150:0.0
export SPARK_HOME=/opt/spark-3.0.3-bin-hadoop2.7

dash_leaflet
pip install jsbeautifier

# git ssh push

ssh-keygen -t ed25519 -C "lohith.uvce@gmail.com"
chmod 400 ~/.ssh/id_rsa
ssh-add id_rsa
If still asks for pwd, update .git/config to ssh url and not https

python3.8 -m venv dash2
source envs/dash2/activate
pip install -r /path/to/requirements.txt

'''leaflet - Adding custom marker'''
https://github.com/thedirtyfew/dash-leaflet/issues/26

export SPARK_HOME=/opt/spark-3.0.3-bin-hadoop2.7

export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH

# Creating spark project on intellij
https://sparkbyexamples.com/spark/spark-setup-run-with-scala-intellij/

# Restart WSL
Restart-Service LxssManager

'''Bootstrap cheatsheet'''
https://dashcheatsheet.pythonanywhere.com/

# Configuring Git for large files
 sudo apt-get install git-lfs
 git lfs install

uvicorn fast_upload:app --host "172.30.69.237" --reload

''' Docker commands '''
docker run -p 80:80 -d --name eapp eapp:latest
docker build -t excelanalysis .
docker login -u 10hith https://index.docker.io/v1/
docker push 10hith/excelanalysis
docker login -u 10hith -p "PSWD" https://index.docker.io/v1/
C:\Users\lohith\.docker; config.json - below
docker system prune when you have exit code 100, to reclaim space;
And then use No cache?? lets see if this works;
Restarting the machine - worked
alias runeapp="docker run -p 80:80 -p 4040:4040 eapp3"
alias buildeapp="cd /home/basal/excelanalysis && docker build -t eapp3 ."

'''
On Digital Ocean -
docker-compose -f docker-compose.yml up -d
Incase of certificate expiration, create a key on DO (Applications and API)
Copy the key to "DO_AUTH_TOKEN" in docker-compose.yml. Remove the acme.json within letsexcrypt folder
'''


{"auths":{"docker.io":{"auth":"asjkldflasjdfSomeThing","email":"lohith.uvce@gmail.com"}},"credsStore":"desktop","currentContext":"default"}

'''Installing Postgres12 on ubuntu'
https://www.tutlinks.com/install-postgresql-12-on-ubuntu/#connect-and-query-to-postgresql-database-from-python
sudo /etc/init.d/postgresql status [start, stop]
Tutorial
# https://www.tutlinks.com/install-postgresql-12-on-ubuntu/#connect-and-query-to-postgresql-database-from-python
Running docker images:
docker run --name postgres-docker -e POSTGRES_PASSWORD=example123 -p 5432:5432 -d postgres:latest
with this, username and dbname is postgres

git filter-branch --index-filter -f 'git rm --cached --ignore-unmatch resources/deutils.jar' HEAD
git filter-repo --invert-paths --path filename
# Removing a big file from git
git filter-branch -f --index-filter "git rm -rf --cached --ignore-unmatch resources/deutils.jar" HEAD

docker run -p 80:80 -e WORKERS_PER_CORE="0.5" eapp

# ToDo



# Reading json values returned from rest api call
val jsonDF = sqlContext.read.schema(schema).json(vals)


In the callback for output(s):
  dummyDivPreDef.children
Input 0 ({"index":MATCH,"type":"scrollTop"}.n_clicks)
has MATCH or ALLSMALLER on key(s) index
where Output 0 (dummyDivPreDef.children)
does not have a MATCH wildcard. Inputs and State do not
need every MATCH from the Output(s), but they cannot have
extras beyond the Output(s).