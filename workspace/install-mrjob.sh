#!/bin/bash
# Dentro de la terminal del Resource Manager

curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
sudo python get-pip.py
pip install --trusted-host pypi.org --trusted-host

files.pythonhosted.org pip setuptools
pip install mrjob

rm get-pip.py
