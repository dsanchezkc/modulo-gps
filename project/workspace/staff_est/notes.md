# Runserver
```sh
# /usr/sbin/setsebool httpd_can_network_connect 1
# apachectl restart
```
# /etc/httpd/conf.d
```
<VirtualHost *:80>
  ProxyPreserveHost On
  ProxyRequests Off
  ServerName www.staff.estchile.cl
  ServerAlias staff.estchile.cl
  ProxyPass / http://172.31.7.147:8081
  ProxyPassReverse / http://172.31.7.147:8081
</VirtualHost>
```
