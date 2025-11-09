#include "include/windoughs.hpp"


namespace win {

    Screen::Screen(unsigned int width, unsigned int height, std::string wallpaper_image):
        window(sf::VideoMode({width, height}), "Windoughs", sf::Style::Default, sf::State::Windowed, get_context_settings()),
        wallpaper_texture(wallpaper_image),
        wallpaper(wallpaper_texture) {

        window.setVerticalSyncEnabled(true);
        wallpaper_texture.setSmooth(true);
        resize_wallpaper(width, height);
    }

    sf::ContextSettings Screen::get_context_settings() {
        sf::ContextSettings settings;
        return settings;
    }

    void Screen::resize_wallpaper(unsigned int width, unsigned int height) {
        sf::View view(sf::FloatRect({0, 0}, {static_cast<float>(width), static_cast<float>(height)}));
        window.setView(view);

        float scale_x = static_cast<float>(width) / wallpaper_texture.getSize().x;
        float scale_y = static_cast<float>(height) / wallpaper_texture.getSize().y;
        float scale = std::max(scale_x, scale_y);
        wallpaper.setScale({scale, scale});

        float offset_x = (static_cast<int>(width) - scale * wallpaper_texture.getSize().x) / 2;
        float offset_y = (static_cast<int>(height) - scale * wallpaper_texture.getSize().y) / 2;
        wallpaper.setPosition({offset_x, offset_y});
    }

    void Screen::refresh() {
        while (const std::optional<sf::Event> event = window.pollEvent()) {
            if (event->is<sf::Event::Closed>()) {
                window.close();
                execute = false;
                return;
            } else if (event->is<sf::Event::Resized>()) {
                resize_wallpaper(event->getIf<sf::Event::Resized>()->size.x, event->getIf<sf::Event::Resized>()->size.y);
            }
        }
        window.clear();
        window.draw(wallpaper);
        window.display();
    }

}