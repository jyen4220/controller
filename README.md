wget http://download.virtualbox.org/virtualbox/5.0.32/VBoxGuestAdditions_5.0.32.iso

sudo mkdir /mnt/tmp

sudo mount VBoxGuestAdditions_5.0.32.iso /mnt/tmp/

cd /mnt/tmp

./VBoxLinuxAdditions.run

sudo reboot

done!

