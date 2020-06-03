#!/bin/bash  
echo "-----optimizer rapsbian to machine-learning"  
ls -lah  
sudo apt-get remove minecraft-pi  --assume-yes
sudo apt-get remove wolfram-engine --assume-yes
sudo apt-get remove mathematica-fonts --assume-yes
apt-get remove --purge scratch*  --assume-yes
sudo apt-get remove sonic-pi  --assume-yes
sudo apt-get remove oracle-java8-jdk  --assume-yes
sudo apt-get remove python-sense-emu python3-sense-emu sense-emu-tools  --assume-yes

sudo apt-get update --assume-yes
sudo apt-get upgrade --assume-yes
sudo apt-get clean --assume-yes
sudo apt-get autoclean --assume-yes
sudo apt-get install libatlas-base-dev  --assume-yes
sudo shutdown -r now