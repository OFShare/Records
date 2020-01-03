//
// created by OFShare on 2019-08-21
//

// 写二进制文件

#include <bits/stdc++.h>

int main() {
    std::ofstream fout("example.bin", std::ios::out | std::ios::binary);
    int number = -20;
    std::string str = "#hello,file#";
    fout.write((char*)&number, sizeof(int));
    fout.write(str.c_str(), sizeof(char) * (str.size()));
    fout.close();
    return 0;
}
