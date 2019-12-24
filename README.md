# Installation


## Start Vagrant

```
vagrant up
vagrant ssh
```

## Set up .bashrc

Add the following lines to the end of `/home/vagrant/.bashrc`

```
export PATH="/vagrant/spark-2.4.4-bin-hadoop2.7/bin:/home/vagrant/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## Install dependencies (Docker, JDK, PyEnv)

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


## Start docker containers (Kafka, Zookeeper)

```
cd /vagrant
sudo docker-compose.yml up -d
```
