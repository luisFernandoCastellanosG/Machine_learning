#!/bin/bash  
echo "-----Creando entorno virtual de Python3 e instalar libreria NumPy-------"  
ls -lah  
echo "----------P1: Instalando herramienta PIP en python3-------------------"
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py 
sudo rm -rf ~/.cache/pip
echo "----------P1: Instalando entorno virtual llamado virtualenvwrapper-------------------"
sudo pip install virtualenv virtualenvwrapper 
