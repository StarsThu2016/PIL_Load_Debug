# Pillow 5.2.0 reads the jpeg image differently between two devices

This repo demos a Pillow bug that I recently noticed. Briefly speaking, I found the jpeg image is loaded differently between my two devices. To demo the difference, you may need a device with an x86_64 CPU and another device with an aarch64 CPU. 

Pillow version: 5.2.0  
Platform: (1) Ubuntu 16.04 OS + x86_64 CPU (2) Ubuntu OS + aarch64 CPU

Reproduce steps:  
(1) Install Python3, Pillow 5.2.0, numpy on both devices.  
(2) Run $ python TestPillow.py.  
(3) Verify that the output on an x86_64 CPU is same as what I got in Output_x86_64.txt.  
(4) Verify that the output on an aarch64 CPU is same as what I got in Output_aarch64.txt.  
(5) Verify that the output on an x86_64 CPU is different from that on an aarch64 CPU.  

# Snapshot of the checksum of the image on an x86_64 CPU
CheckSum:  100837709  
  Channel-wise CheckSum[0]:  47238115  
  Channel-wise CheckSum[1]:  25964663  
  Channel-wise CheckSum[2]:  27634931  

# Snapshot of the checksum of the image on an aarch64 CPU
CheckSum:  100836439  
  Channel-wise CheckSum[0]:  47237972  
  Channel-wise CheckSum[1]:  25964659  
  Channel-wise CheckSum[2]:  27633808  

# Snapshot of the checksum of the image on an aarch64 CPU (libjpeg9, same as that in x86_64 device)
('CheckSum: ', 100837709)  
('  Channel-wise CheckSum[0]: ', 47238115)  
('  Channel-wise CheckSum[1]: ', 25964663)  
('  Channel-wise CheckSum[2]: ', 27634931)  

# Personal analysis
Note: This is a subjective debugging analysis that may mislead you and distract you from the root cause. Please read with caution.  

Hypothesis: The Pillow 5.2.0 library is executed differently between two devices mainly due to the different CPU architecture.  

Evidence:  
I use two consecutive git commits to compare how the source code of PIL library differs between two devices.  
Commit 1 (earlier): The PIL directory on aarch64 machine.  
Commit 2 (later): The PIL directory on x86_64 machine (replace in a delete-all-and-copy-all way).  

I notice the change of commit 2 is as follows,  
    A PIL/.libs/libfreetype-6ed94974.so.6.16.1  
    A PIL/.libs/libjpeg-3fe7dfc0.so.9.3.0  
    A PIL/.libs/liblcms2-a6801db4.so.2.0.8  
    A PIL/.libs/liblzma-90de1f11.so.5.2.2  
    A PIL/.libs/libopenjp2-e366d6b0.so.2.1.0  
    A PIL/.libs/libpng16-8793a1b2.so.16.32.0  
    A PIL/.libs/libtiff-8a6d997d.so.5.3.0  
    A PIL/.libs/libwebp-8ccd29fd.so.7.0.2  
    A PIL/.libs/libwebpdemux-eba3dc32.so.2.0.4  
    A PIL/.libs/libwebpmux-1c63fe99.so.3.0.2  
    A PIL/.libs/libz-a147dcb0.so.1.2.3  
    R PIL/_imaging.cpython-35m-aarch64-linux-gnu.so  
    A PIL/_imaging.cpython-35m-x86_64-linux-gnu.so  
    A PIL/_imagingcms.cpython-35m-x86_64-linux-gnu.so  
    R PIL/_imagingft.cpython-35m-aarch64-linux-gnu.so  
    A PIL/_imagingft.cpython-35m-x86_64-linux-gnu.so  
    R PIL/_imagingmath.cpython-35m-aarch64-linux-gnu.so  
    A PIL/_imagingmath.cpython-35m-x86_64-linux-gnu.so  
    R PIL/_imagingmorph.cpython-35m-aarch64-linux-gnu.so  
    A PIL/_imagingmorph.cpython-35m-x86_64-linux-gnu.so  
    R PIL/_imagingtk.cpython-35m-aarch64-linux-gnu.so  
    A PIL/_imagingtk.cpython-35m-x86_64-linux-gnu.so  
    A PIL/_webp.cpython-35m-x86_64-linux-gnu.so  

From aarch64 directory to x86_64 directory, we see 3 types of changes,  
(1) "_imaging*.cpython-35m-aarch64-linux-gnu.so" is replaced with "_imaging*.cpython-35m-x86_64-linux-gnu.so".  
(2) a subdirectory ".lib/" is added.  
(3) "_imagingcms.cpython-35m-x86_64-linux-gnu.so" and "PIL/_webp.cpython-35m-x86_64-linux-gnu.so" are added.  

For (1), this might be the root cause since the dynamic libraries are changed to the x86_64 version and these dynamic libraries may be implemented differently.   
For (2), this may because the installation process of Pillow library. For example, on the aarch64 machine, these libs are already installed somewhere else and linked correctly by the OS and thus no local .lib/ is needed. However, on the x86_64 machine, these libs are not installed and thus Pillow place these libs locally inside its directory when Pillow is installed.  
For (3), I have no idea.
