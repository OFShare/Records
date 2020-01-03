**grep**: 

    1 grep  searches  for  PATTERN in each FILE
    
    2 .(小数点)：代表『一定有一个任意字节』的意思；
    
    3 * (星号)：代表『重复前一个字符， 0 到无穷多次』的意思，为组合形态, 不是任意一个字符
    
    2 examples: grep -rni "t[ae]st2*" Tensorflow/ Tensorflow/

**find**:

    1 find searches for files
    
    2 * stands for any character
    
    3 examples: find './' -iname "*read*" 

**Others:**

```cmake
# 链接静态库或动态库
# 静态，动态的区别就是前者编译时加载，后者运行时加载
target_link_libraries( # Specifies the target library.
        face -Wl,--whole-archive ${tensorflow_LIBS} -Wl,--no-whole-archive, -DCMAKE_SYSTEM_NAME=Android,-std=c++11,
        ${OpenCV_LIBS}
        ${ncnn_LIBS}
        ${ndk-native_LIBS}
)

sourceSets {
        main {
            // 加载动态链接库
            jniLibs.srcDirs = ['src/main/libs']
        }
    }
    
System.loadLibrary("tensorflowlite");    
```
