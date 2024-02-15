#include <iostream>

int main() {

    int x = 1;
    int* pX = &x;

    std::cout << x << std::endl;
    std::cout << pX << std::endl;
    
    return 0;
}