### Mac OSX

在Mac系统上预装了Opencl SDK, 所以不需要自己再装.

### Mac OSX OpenCL C API

```c
// demo1.cc
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <OpenCL/cl.h>

int main() {

  /* Host/device data structures */
  cl_platform_id platform;
  cl_device_id device;
  cl_context context;
  cl_int err;

  /* Access the first installed platform */
  err = clGetPlatformIDs(1, &platform, NULL);
  if(err < 0) {
    perror("Couldn't find any platforms");
    exit(1);
  }

  printf("hello, opencl\n");
  return 0;
}
```

`clang++ -std=c++11 -framework OpenCL demo1.cc`

### Mac OSX OpenCL C++ Bindings

```cpp
// demo2.cc
#define CL_HPP_TARGET_OPENCL_VERSION 120
#define CL_HPP_MINIMUM_OPENCL_VERSION 120

#include "./opencl.hpp"

int main(void) {

  std::vector<cl::Platform> platforms;
  cl::Platform::get(&platforms);

  printf("hello, opencl c++ bindings\n");
  return 0;
}
```

`clang++ -std=c++11 -framework OpenCL demo2.cc`, 特别注意开头2行需要定义的宏.

为了运行[`OpenCL C++ bindings API`](http://github.khronos.org/OpenCL-CLHPP/), 我们需要去[OpenCL-CLHPP](https://github.com/KhronosGroup/OpenCL-CLHPP)先手动下载`opencl.hpp`这个头文件, 然后放到`includePath`可以搜索到的地方, 如当前目录. 

只需要这个头文件即可.

[cl2.hpp with OSX?](https://github.com/KhronosGroup/OpenCL-CLHPP/issues/40)

[Can't setup OpenCL on Mac OSX](https://stackoverflow.com/questions/23072367/cant-setup-opencl-on-mac-osx)

### OpenCL推荐资料

[Matthew Scarpino — OpenCL in Action英文原版](https://github.com/DevNulPavel/OpenCL_Examples/tree/master/OpenCL_Books)

[Opencl in Action 在线中文版](http://reader.epubee.com/books/mobile/e5/e58a7de5d56cdda0ba09d83064083cc1/text00001.html)

[opencl_in_action书上源码](https://github.com/OFShare/opencl_in_action)

[零基础学习OpenCL，有哪些好的建议？](https://www.zhihu.com/question/48984738)

[Khronos OpenCL Registry](https://www.khronos.org/registry/OpenCL/)

