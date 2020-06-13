copy *.service and *.timer to /etc/systemd/system

then 
sudo systemctl enable xxxx.service
sudo systemctl start xxxx.service

sudo systemctl enable xxxx.timer
sudo systemctl start xxxx.timer
