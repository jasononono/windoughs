#include <iostream>
#include <algorithm>
#include <SFML/Graphics.hpp>


struct Screen {
    sf::RenderWindow window;
    sf::Texture wallpaper_texture;
    sf::Sprite wallpaper;
    bool execute = true;

    Screen(unsigned int width = 800, unsigned int height = 600, std::string wallpaper_image = "wallpaper_default.jpg"):
        window(sf::VideoMode({width, height}), "Windoughs"),
        wallpaper_texture(wallpaper_image),
        wallpaper(wallpaper_texture) {

        window.setVerticalSyncEnabled(true);
        wallpaper_texture.setSmooth(true);
        resize_wallpaper(width, height);
    }

    sf::ContextSettings get_context_settings() {
        sf::ContextSettings settings;
        settings.antiAliasingLevel = 8;
        return settings;
    }

    void resize_wallpaper(unsigned int width, unsigned int height) {
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

    void refresh() {
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
};


int main() {
    Screen screen(800, 600);

    while (screen.execute) {
        screen.refresh();
    }
}