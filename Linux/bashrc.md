### `~/.bashrc` common setting

```shell
################# Acui setting #################
echo 'Acui .bashrc'
export ven3='source /home/acui/ven3/bin/activate'

# python
export PYTHONPATH=$PYTHONPATH:/home/acui/Proj/models/research/slim/ 

# $PATH是运行可执行文件时的搜索路径
export PATH=$PATH:'/home/acui/Test/cmake-3.15.1-rc/bin/'

# C header, include头文件的搜索路径
export C_INCLUDE_PATH="/home/acui/MyLibs/include/opencv4":$C_INCLUDE_PATH

# CPP header, include头文件的搜索路径
export CPLUS_INCLUDE_PATH="/home/acui/MyLibs/include/ncnn/":$CPLUS_INCLUDE_PATH

# So, LD_LIBRARY_PATH指定动态库搜索路径
# 动态链接库搜索路径
export LD_LIBRARY_PATH='/home/acui/MyLibs/opencv/opencv-4.1.0/build/lib':$LD_LIBRARY_PATH
# 静态链接库搜索路径：
export LIBRARY_PATH=XXX:$LIBRARY_PATH
```


