##### 1. wget resume from break-point

- wget -c -t 0 -O "xxx.zip" "https://xxx.zip"

##### ２. output redirect to a file, 重定向, 在bash终端, 而不是在mac里的fish终端

 - python main.py 1> log.txt 2> log.txt &
 
 - 语法：>& 将命令执行时屏幕上所产生的任何信息写入指定的文件中。
 
 - cc file1.c >& log.txt 将编译file1.c 文件时所产生的任何信息写入文件log.txt 中。
 
 - tail -f -n 15 log.txt

