#!/usr/bin/bash
pkill gunicorn
gunicorn -c config/gunicorn/iksaan.py 2>&1
sudo systemctl restart nginx
