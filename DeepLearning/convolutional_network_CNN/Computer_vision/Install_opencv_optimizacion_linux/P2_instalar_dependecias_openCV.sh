#!/bin/bash  
echo "-----install dependencias para OpenCV by python3-------"  
ls -lah  
echo "P1: Instalando herramientas de desarrollador, incluido CMake"
sudo apt-get install build-essential cmake pkg-config --assume-yes
echo "P2: Instalando paquetes de E/S para manejar imagenes JPEG, PNG, TIFF, etc"
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev  --assume-yes
echo "P3: Instalando paquetes de E/S de video"
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev  --assume-yes
sudo apt-get install libxvidcore-dev libx264-dev  --assume-yes
echo "P4: Instalando la biblioteca de desarrollo GTK, necesaria para OpenCV"
sudo apt-get install libfontconfig1-dev libcairo2-dev  --assume-yes
sudo apt-get install libgdk-pixbuf2.0-dev libpango1.0-dev  --assume-yes
sudo apt-get install libgtk2.0-dev libgtk-3-dev  --assume-yes
echo "P5:Instalando dependencias adicionales para trabajar matrices en OpenCV"
sudo apt-get install libatlas-base-dev gfortran  --assume-yes
echo "P6: Instalando librerias para manejar datos HDF5 y GUI Qt"
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103  --assume-yes
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5  --assume-yes
echo "P7: Instalando archivos de encabezado de Python 3 " 
sudo apt-get install python3-dev --assume-yes
sudo shutdown -r now