
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/pythonprojeckdjango/nginx/nginx.conf /etc/nginx/sites-available/pythonprojeckdjango
sudo ln -s /etc/nginx/sites-available/pythonprojeckdjango /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx