#pragma once

#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <SFML/Graphics.hpp>


namespace win {

    std::map<sf::Mouse::Button, int> MOUSE = {{sf::Mouse::Button::Left, 0},
                                              {sf::Mouse::Button::Middle, 1},
                                              {sf::Mouse::Button::Right, 2}};

    struct Event;
    struct Window;

    struct Screen {
        sf::RenderWindow surface;
        sf::Texture wallpaper_texture;
        sf::Sprite wallpaper;
        bool execute = true;
        Event event;
        std::vector<Window> windows;

        Screen(sf::Vector2f size, const std::string &wallpaper_image = "assets/wallpaper_default.jpg");

        sf::ContextSettings get_context_settings();
        void resize_wallpaper(sf::Vector2f size);
        void handle_events();
        void refresh();
        sf::Sprite draw_texture(sf::RenderTexture &render_texture, sf::Vector2f position);
    };

    struct Event {
        bool mouse[3];
        bool mouse_pressed, mouse_released;
        sf::Vector2f mouse_position;
    };

    struct Window {
        sf::RenderTexture surface;
        sf::Sprite sprite;
        sf::Vector2f size;
        sf::Vector2f position;

        Window(Screen &parent, sf::Vector2f size, sf::Vector2f position);

        void refresh(Screen &parent);
        bool contains(sf::Vector2f pos);
    };

}