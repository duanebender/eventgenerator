R sequence mining on centos 6.5
================================

# Introduction

Vagrant project to create a virtual machine with R environment for event generator evaluation.
After provisioning, you will see:

1. a virtual machine (VM) named "rnode1" in virtualbox
2. VM OS is centos 6.5
3. log-on vitual machine using a telnent/ssh client such as PuTTY from your desktop
4. VM hostname is "rnode1", IP address is "10.211.51.101", log-on account is "root/vagrant"
4. R is installed in VM
5. Association and sequence mining packages (arules, arulesSequences) for R are installed in VM
6. R IDE "RStudio" is installed in VM

# Getting Started

1. [Download and install VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Download and install Vagrant](http://www.vagrantup.com/downloads.html).
3. Run ```vagrant box add centos65 https://github.com/2creatives/vagrant-centos/releases/download/v6.5.3/centos65-x86_64-20140116.box```
4. Git clone this project, and change directory (cd) into this directory (eventgenerator-master\R-sequence-mining-env).
5. Run ```vagrant up``` to create the VM.
6. You could run ```ssh``` directly with ip of VM and username/password of root/vagrant.
7. Run ```vagrant destroy``` when you want to destroy and get rid of the VM.
8. The directory of /vagrant is mounted in VM by vagrant if you want to access host machine from VM.

# Reference
How to use R for sequence mining refer to following link:
http://en.wikibooks.org/wiki/Data_Mining_Algorithms_In_R/Sequence_Mining/SPADE

