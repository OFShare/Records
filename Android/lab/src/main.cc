/*
 * Author        : OFShare
 * E-mail        : OFShare@outlook.com
 * Created Time  : 2020-10-14 15:50:27 PM
 * File Name     : main.cc
 */

#include <string>
#include <iostream>
#include "hello.h"

int main() {
    std::string s = "hello";
    imba::print(s);
    std::cout << "after: " << s << std::endl;
    return 0;
}
