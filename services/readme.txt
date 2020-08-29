#instructions on how to deploy services

> copy *.service and *.timer to /etc/systemd/system

#then 

> sudo systemctl enable linear-actuator.service
> sudo systemctl start linear-actuator.service

> sudo systemctl enable am2302-sensor.timer
> sudo systemctl start am2302-sensor.timer
