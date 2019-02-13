# Pillow 5.2.0 reads the jpeg image differently between two devices

This repo demos a Pillow bug that I recently noticed. Briefly speaking, I found the jpeg image is loaded differently between my two devices. To demo the difference, you may need a device with x86_64 CPU and another device with aarm64 CPU. 

Pillow version: 5.2.0

Platform: (1) Ubuntu OS + x86_64 CPU (2) Ubuntu OS + aarch64 CPU

Republicate the fact:

(1) Install Pillow 5.2.0 on both devices.

(2) Run $ python TestPillow.py

(3) Varify that the output on x86_64 CPU is same as what I got in Output_x86_64.txt

(4) Varify that the output on aarm64 CPU is same as what I got in Output_aarch64.txt

(5) The output on x86_64 CPU is different from the output on aarch64 CPU
