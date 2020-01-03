#### Text files   

reading and writing data with the extraction and insertion operators (`<<` and `>>`) and functions like `getline` is enough

#### Binary files 

File streams include two member functions specifically designed to read and write binary data sequentially: `write` and `read`. 

write ( memory_block, size ); 将memory_block指向的内存内容写到文件里
read ( memory_block, size ); 将文件里的内容读到memory_block指向的内存

Where `memory_block` is of type `char*` (pointer to `char`), and represents the address of an array of bytes where the read data elements are stored or from where the data elements to be written are taken. The `size` parameter is an integer value that specifies the number of characters to be read or written from/to the memory block.

#### simple examples

[把内容写进普通文本文件](./file1.cc)

[把内容保存为二进制文件](./file2.cc)

[把普通文本文件读出来](./file３.cc)

[把二进制文件读出来](./file４.cc)

reference: 

- [c++ file tutorial](http://www.cplusplus.com/doc/tutorial/files/)
- [std::ostream::write](http://www.cplusplus.com/reference/ostream/ostream/write/)

