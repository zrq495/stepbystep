#########################################################################
# File Name: gunicorn.sh
# Author: zrq495
# mail: zrq495@gmail.com
# Created Time: 2013年11月23日 星期六 13时33分15秒
#########################################################################
#!/bin/bash

sudo pkill gunicorn
sudo gunicorn code:application -D --pid /var/run/gunicorn.pid -b 0.0.0.0:1111
