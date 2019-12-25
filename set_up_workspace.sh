#!/bin/bash

# Install JDK and Scala
sudo apt-get update;
sudo apt-get install openjdk-8-jdk;
sudo apt-get install scala;


# Install PyEnv dependencies
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl;


# Install PyEnv
curl https://pyenv.run | bash;
source ~/.bashrc;
pyenv install 3.7.2;
pyenv global 3.7.2;
pyenv rehash;
