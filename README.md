# Installation

## Download Spark (2.4.4 with Hadoop 2.7)

- https://www.apache.org/dyn/closer.lua/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz

## Download Kafka (2.3.0 with Scala 2.11)

- https://kafka.apache.org/downloads

## Start Vagrant

```
vagrant up
vagrant ssh
```

## Set up .bashrc

Add the following lines to the end of `/home/vagrant/.bashrc`

```
export PATH="/vagrant/dev/spark-2.4.4-bin-hadoop2.7/bin:/home/vagrant/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## Install dependencies (JDK, Scala, PyEnv)

```
cd /vagrant
./set_up_workspace.sh
```

## Install pip requirements

Make sure that `which python` points to the python 3.7.2 installation.

If not, exit vagrant and ssh in again. This should update the path.

```
cd /vagrant
pip install -r src/requirements.txt
```
