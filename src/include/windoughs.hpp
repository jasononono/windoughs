#pragma once

#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <SFML/Graphics.hpp>


namespace win {

    constexpr inline std::size_t MOUSE_COUNT = 5;
    const inline std::map<sf::Mouse::Button, int> MOUSE = {{sf::Mouse::Button::Left, 0},
                                                           {sf::Mouse::Button::Middle, 1},
                                                           {sf::Mouse::Button::Right, 2},
                                                           {sf::Mouse::Button::Extra1, 3},
                                                           {sf::Mouse::Button::Extra2, 4}};

    struct Window;

    struct Event {
        bool mouse[MOUSE_COUNT];
        bool mouse_pressed[MOUSE_COUNT];
        bool mouse_released[MOUSE_COUNT];
        sf::Vector2f mouse_position;
    };

    struct Screen {
        sf::RenderWindow surface;
        sf::Texture wallpaper_texture;
        sf::Sprite wallpaper;
        bool execute = true;
        Event event;
        std::vector<Window> windows;
        int selected_window = -1;
        sf::Vector2f selected_window_offset;

        Screen(sf::Vector2f size, const std::string &wallpaper_image = "assets/wallpaper_default.jpg");

        sf::ContextSettings get_context_settings() const;
        void resize_wallpaper(sf::Vector2f size);
        void handle_events();
        void refresh();
        sf::Sprite draw_texture(sf::RenderTexture &render_texture, sf::Vector2f position);
    };

    struct TitleBar {
        sf::Vector2f size;
        sf::Vector2f global_position;
        sf::RenderTexture surface;
        sf::Sprite sprite;

        TitleBar(const Screen &screen, const Window &parent, float height);

        void refresh(Window &parent);
        bool contains(sf::Vector2f pos);
    };

    struct Window {
        sf::Vector2f size;
        sf::Vector2f position;
        sf::RenderTexture surface;
        sf::Sprite sprite;
        TitleBar titlebar;

        Window(const Screen &screen, sf::Vector2f size, sf::Vector2f position);

        void refresh(Screen &screen);
        bool contains(sf::Vector2f pos);
        sf::Sprite draw_texture(sf::RenderTexture &render_texture, sf::Vector2f position);
    };

}