//
// created by OFShare on 2019-08-21
//

// 读二进制文件

#include <bits/stdc++.h>

int main() {
    std::ifstream fin("example.bin", std::ios::in | std::ios::binary);

    // get size of file
    fin.seekg(0, fin.end);
    long size = fin.tellg();
    fin.seekg(0);

    // allocate memory for file content
    char* buffer = new char[size+1];
    buffer[size] = '\0';
    fin.read(buffer, size);
    std::cout << size << buffer << std::endl;

    // release dynamically-allocated memory
    delete[] buffer;
    fin.close();
    return 0;
}
