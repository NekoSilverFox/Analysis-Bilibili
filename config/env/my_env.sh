#JAVA_HOME
export JAVA_HOME=/opt/module/jdk1.8.0_212
PATH=$PATH:$JAVA_HOME/bin

#HADOOP_HOME
export HADOOP_HOME=/opt/module/hadoop-3.1.3

PATH=$PATH:$HADOOP_HOME/bin
PATH=$PATH:$HADOOP_HOME/sbin

export SUPERSET_HOME=/opt/module/anaconda3/envs/superset/
PATH=$PATH:$SUPERSET_HOME/bin

export SUPERSET_CONFIG_PATH=/opt/module/anaconda3/envs/superset/lib/python3.9/site-packages/superset/superset_config.py

export FLASK_APP=superset
