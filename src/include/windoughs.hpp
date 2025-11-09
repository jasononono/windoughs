#pragma once

#include <iostream>
#include <algorithm>
#include <SFML/Graphics.hpp>


namespace win {

    struct Screen {
        sf::RenderWindow window;
        sf::Texture wallpaper_texture;
        sf::Sprite wallpaper;
        bool execute = true;

        Screen(unsigned int width = 800, unsigned int height = 600, std::string wallpaper_image = "assets/wallpaper_default.jpg");

        sf::ContextSettings get_context_settings();
        void resize_wallpaper(unsigned int width, unsigned int height);
        void refresh();
    };

}