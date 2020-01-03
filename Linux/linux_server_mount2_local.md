```sh
sudo apt-get install sshfs
```

```sh
sshfs $USER@xx.xx.xx.xx:$REMOTE_PATH $LOCAL_PATH

sshfs -p 80 $USER@xx.xx.xx.xx:$REMOTE_PATH $LOCAL_PATH
```

```sh
fusermount -u $LOCAL_PATH
```