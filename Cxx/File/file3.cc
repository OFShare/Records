//
// created by OFShare on 2019-08-21
//

// 读文本文件
#include <bits/stdc++.h>

int main() {
    std::ifstream fin("example.txt", std::ios::in);
    int number;
    char buffer[233];

    fin >> number >> buffer;
    std::cout << number << std::endl;
    std::cout << buffer << std::endl;

    fin.close();
    return 0;
}
