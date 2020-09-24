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

##### 修改某次 commit 日志和内容

```c
1、将当前分支无关的工作状态进行暂存
git stash
2、将 HEAD 移动到需要修改的 commit 的前一个上
commit d87dbd5c076
commit1
commit a37c03214ad
commit2
commit a37c034543d
commit3
我要修改commit2的内容和日志
git rebase a37c034543d --interactive
3、找到要改的commit，将pick改成edit
4、修改内容，然后git add
5、git commit --amend
6、git rebase --continue
7、git stash pop
```

##### Others

- `git remote -v`

[Create a git BitBucket/ Github repository from already locally existing project](http://samranga.blogspot.com/2015/07/create-git-bitbucket-repository-from.html?view=sidebar)