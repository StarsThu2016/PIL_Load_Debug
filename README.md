# Pillow 5.2.0 loads the jpeg image differently between two machines
This repo demos a Pillow issue that I recently noticed. Briefly speaking, I found the jpeg image is loaded differently between my two devices.  
Pillow version: 5.2.0  
Platform: Ubuntu 16.04 OS  
By running "python TestPillow.py", one machine outputs as in "Output_aarch64.txt", and another machine outputs as in "Output_x86_64.txt". Note: this issue is not relevant to the CPU architecture, although I was considering so.  

# Snapshot of the checksum of the image on machine 1
CheckSum:  100836439  
  Channel-wise CheckSum[0]:  47237972  
  Channel-wise CheckSum[1]:  25964659  
  Channel-wise CheckSum[2]:  27633808  

# Snapshot of the checksum of the image on machine 2
CheckSum:  100837709  
  Channel-wise CheckSum[0]:  47238115  
  Channel-wise CheckSum[1]:  25964663  
  Channel-wise CheckSum[2]:  27634931  

# Issue fixed
The root cause of this issue is the inconsistency of libjpeg library that Pillow depends on. On machine 1, Pillow 5.2.0 is built with libjpeg 8, while on machine 2, Pillow 5.2.0 is built with libjpeg 9. To decode the jpeg image, Pillow calls dynamic linked library libjpeg in which it decodes differently from version 8 to version 9. This issue can be fixed by upgrading the libjpeg library in machine 1 to version 9 and reinstalling Pillow.  

# Step-by-step solution
Note: the solution is just for reference. The command on your machine may be different.  

* Uninstall libjpeg 8  
Note: this step is necessary for my machine because otherwise I cannot install libjpeg9-dev.  
$ sudo apt-get purge libjpeg-turbo8-dev  

* Install libjpeg 9  
$ sudo apt-get install libjpeg9-dev  

* Uninstall Pillow (optional)  
Note: depending on how Pillow is installed, the command may be different.  
$ pip uninstall Pillow   
$ sudo pip uninstall Pillow  

* Reinstall Pillow as a system-wide package  
Note: you may also install as a user's package without "sudo", but "--no-cache-dir" option is a must according to "If Pillow has been previously built without the required prerequisites, it may be necessary to manually clear the pip cache or build without cache using the --no-cache-dir option to force a build with newly installed external libraries." in https://pillow.readthedocs.io/en/stable/installation.html  
$ sudo pip install --no-cache-dir Pillow==5.2.0  

# Useful debugging commands
* Check all jpeg libraries installed on the machine  
$ dpkg -l | grep -In libjpeg  

* Check the linked .so files of libjpeg library  
$ ldconfig -p | grep -In libjpeg   

* Further check the .so files in the file system to make sure the default libjpeg.so is linked to libjpeg.so.9.2.0  
$ ls -lh /usr/lib/\*/libjpeg\*  

* Check the python version  
$ python -V  

* Check the Pillow version  
$ python -c "import PIL; print(PIL.\_\_version\_\_)"  

* Check where Pillow installs  
$ python -c "import PIL; print(PIL.\_\_file\_\_)"  

* Check the libjpeg version that Pillow uses  
$ python -c "from PIL import Image; print(Image.core.jpeglib_version)"  

# Python and pip basics
pip/pip3 are python package management tools, however they can only see some directories. For example,  
(1) /home/nvidia/c4aarch64_installer/envs/tf114/lib/python3.5/site-packages  
(2) /home/nvidia/c4aarch64_installer/lib/python3.7/site-packages/  
(3) /home/nvidia/.local/lib/python2.7/site-packages  
(4) /usr/local/lib/python3.5/dist-packages  
(1) is installed in speciallized virtual environment, (2) is installed in base virtual environment, (3) is install by ```pip install --user```, (4) is installed by ```sudo pip install```.  
Thus, ```/usr/local/bin/pip```(system-wide pip) can not see local packages in ```/home/nvidia/.local/lib/python2.7/site-packages```.  
Thus, python in base virtual environment (```/home/nvidia/c4aarch64_installer/bin/python```) cannot see python packages in speciallized virtual environment (```/home/nvidia/c4aarch64_installer/envs/tf114/lib/python3.5/site-packages/PIL```).  

## Make sure which pip/pip3 we are using
```
which pip
which pip3
sudo which pip
sudo which pip3
```

## Make sure which python we are using
```
python -V
```

## Make sure which python package we import
```
python -c "import PIL; print(PIL.__file__)"  
```

## Make sure which jpeg lib the python package links
```
python -c "from PIL import Image; print(Image.core.jpeglib_version)" 
```

# Snapshot of the checksum of the image on machine 1 after the issue is fixed (libjpeg 9, same as that on machine 2, Output_aarch64_libjpeg9.txt)
CheckSum:  100837709  
  Channel-wise CheckSum[0]:  47238115  
  Channel-wise CheckSum[1]:  25964663  
  Channel-wise CheckSum[2]:  27634931  


