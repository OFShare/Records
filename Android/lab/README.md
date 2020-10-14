### 目的

在这个目录下, 做了一个实验: 

- main <------ libc++_shared.so
- main <------ libhello.so
- libhello.so <------ libgnustl_shared.so

先在simple_libs目录下, 编译出libhello.so 

然后在src目录下, 使用libhello.so里提供的函数

---

结论:

可以看到上面可执行文件, main(直接/间接)依赖了两个STL运行时库, 在编译链接阶段会发生链接错误.

所以我们应该遵从[每个应用一个 STL](https://developer.android.google.cn/ndk/guides/cpp-support?hl=zh-cn#one_stl_per_app) 

当然如果我们的main只是链接libhello.so但是没有使用libhello.so里提供的东西如函数, 则会通过编译链接, 但是这没有意义, 因为我们链接它, 当然是想要使用它里面提供的东西(如函数)嘛.

---

因为我们想把可执行文件放在android手机上执行, 需要注意一些地方:

- Linux可执行程序不能放在sdcard上,会导致没有权限，强烈建议放在`/data/local/tmp`目录下
- export `LD_LIBRARY_PATH`=./:$LD_LIBRARY_PATH