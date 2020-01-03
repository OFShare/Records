##### add submodule to track master branch

- `git submodule add -b master [URL to Git repo]`
- then `git commit -m 'add submodule'`

##### add ssh key
- `ssh-keygen -t rsa -C "your.email@example.com" -b 4096`


##### delete remote/local branch or tag

- `git push origin --delete <branchName>` remote
- `git push origin --delete tag <tagname>` remote
- `git branch -D <branch-name>` local

##### add one repoA to another branch of repoB

- `git remote add pose repoB.git`
- `git pull pose dev-branch` 
- fix conflicts and merge then,
- `git push pose HEAD:dev-branch` if dev-branch is not exist at remote repo,it'll create new one.

##### add large files to remote repo

- `curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash`
- `sudo apt-get install git-lfs` First install on linux
- `git lfs install` at one repo
- `git lfs track "*.h5"`
- `git add .gitattributes`
- `git add model.h5`
- `git commit -m 'add keras model'`
- `git push`

##### add/modify git author and email

- set global
- `git config --global user.name "Author Name"`
- `git config --global user.email "Author Email"`
- set local 
- `git config user.name "Author Name"`
- `git config user.email "Author Email"`
- locate and delete global
- `git config --list`
- `git config --global --unset user.name`

##### push local tags to remote

- `git push origin --tags`

[Create a git BitBucket/ Github repository from already locally existing project](http://samranga.blogspot.com/2015/07/create-git-bitbucket-repository-from.html?view=sidebar)