#include "include/windoughs.hpp"


int main() {
    win::Screen screen({800, 600});

    while (screen.execute) {
        screen.refresh();
    }
}