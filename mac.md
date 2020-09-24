1.查看可执行程序(ELF)或动态库所依赖动态库

- `brew install binutils`

- ldd `which gdb`
- readelf -d `which gdb`
- ldd xxx.so
- readelf -d xxx.so

