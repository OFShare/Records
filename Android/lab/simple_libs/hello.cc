#include "hello.h"

namespace imba {
    void print(std::string &s) {
        std::string name = "-Acui";
        for (const auto &ch: name) {
            s.push_back(ch);
        }
    }
}
