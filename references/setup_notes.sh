alias pycharm="nohup /opt/pycharm-community-2021.1.3/bin/pycharm.sh </dev/null &>/dev/null &"
alias intellij="nohup /opt/idea-IC-211.7628.21/bin/idea.sh </dev/null &>/dev/null &"

# Add this to the bashrc file
export DISPLAY=192.168.1.150:0.0
export SPARK_HOME=/opt/spark-3.0.3-bin-hadoop2.7

python3.8 -m venv .env3.8

pip install -r /path/to/requirements.txt


pip install -U dash-labs
pip install -U dash-bootstrap-components spectra colormath requests tinycss2
pip install diskcache
# PYSPARK_HADOOP_VERSION=2.7 pip install pyspark -v
pip install koalas
pip install pyspark
pip install openpyxl # To read xlsx file in the dash upload component
pip install jupyterlab
pip install findspark

export SPARK_HOME=/opt/spark-3.0.3-bin-hadoop2.7

export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH

# Creating spark project on intellij
https://sparkbyexamples.com/spark/spark-setup-run-with-scala-intellij/

# Restart WSL
Restart-Service LxssManager
