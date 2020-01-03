//
// created by OFShare on 2019-08-21
//

// 写文本文件
#include <bits/stdc++.h>

int main() {
    std::ofstream fout("example.txt", std::ios::out);
    int number = -20;
    std::string str = "#hello,file#";
    fout << number << str <<std::endl;
    fout.close();
    return 0;
}
