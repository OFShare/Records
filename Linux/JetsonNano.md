1. ssh username@192.168.55.1, (username is you own name, ip is static)

2. sudo apt-get update

3. sudo apt-get install python3-dev

4. sudo apt-get install libffi-dev
5. pip install gunicorn # do not like this: sudo apt-get install gunicorn

6. pip install flask_restful

7. sudo netstat -tunlp |grep 8080 (watch port)