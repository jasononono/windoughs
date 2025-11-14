#include "include/windoughs.hpp"


namespace win {

    Screen::Screen(sf::Vector2f size, const std::string &wallpaper_image):
    surface(sf::VideoMode(static_cast<sf::Vector2u>(size)), "Windoughs", sf::Style::Default, sf::State::Windowed, get_context_settings()),
    wallpaper_texture(wallpaper_image),
    wallpaper(wallpaper_texture) {

        surface.setVerticalSyncEnabled(true);
        wallpaper_texture.setSmooth(true);
        resize_wallpaper(size);

        windows.push_back(Window(*this, {100, 100}, {10, 10}));
    }

    sf::ContextSettings Screen::get_context_settings() {
        sf::ContextSettings settings;
        return settings;
    }

    void Screen::resize_wallpaper(sf::Vector2f size) {
        sf::View view(sf::FloatRect({0, 0}, {static_cast<float>(size.x), static_cast<float>(size.y)}));
        surface.setView(view);

        float scale_x = static_cast<float>(size.x) / wallpaper_texture.getSize().x;
        float scale_y = static_cast<float>(size.y) / wallpaper_texture.getSize().y;
        float scale = std::max(scale_x, scale_y);
        wallpaper.setScale({scale, scale});

        float offset_x = (size.x - scale * wallpaper_texture.getSize().x) / 2;
        float offset_y = (size.y - scale * wallpaper_texture.getSize().y) / 2;
        wallpaper.setPosition({offset_x, offset_y});
    }

    void Screen::handle_events() {
        for (int i = 0; i < MOUSE_COUNT; i++) {
            event.mouse_pressed[i] = false;
            event.mouse_released[i] = false;
        }

        while (const std::optional<sf::Event> e = surface.pollEvent()) {
            if (e->is<sf::Event::Closed>()) {
                surface.close();
                execute = false;
                return;
            } else if (e->is<sf::Event::Resized>()) {
                resize_wallpaper(static_cast<sf::Vector2f>(e->getIf<sf::Event::Resized>()->size));
            } else if (e->is<sf::Event::MouseButtonPressed>()) {
                event.mouse[MOUSE.at(e->getIf<sf::Event::MouseButtonPressed>()->button)] = true;
                event.mouse_pressed[MOUSE.at(e->getIf<sf::Event::MouseButtonPressed>()->button)] = true;
            } else if (e->is<sf::Event::MouseButtonReleased>()) {
                event.mouse[MOUSE.at(e->getIf<sf::Event::MouseButtonReleased>()->button)] = false;
                event.mouse_released[MOUSE.at(e->getIf<sf::Event::MouseButtonReleased>()->button)] = true;
            } else if (e->is<sf::Event::MouseMoved>()) {
                event.mouse_position = static_cast<sf::Vector2f>(e->getIf<sf::Event::MouseMoved>()->position);
            }
        }
    }

    void Screen::refresh() {
        handle_events();
        surface.clear();
        surface.draw(wallpaper);

        for (int i = 0; i < windows.size(); i++) {
            if (event.mouse_pressed[0] && windows[i].contains(event.mouse_position)) {
                selected_window = i;
                selected_window_offset = event.mouse_position - windows[i].position;
            }
            windows[i].refresh(*this);
        }
        if (event.mouse_released[0]) {selected_window = -1;}
        if (selected_window != -1) {
            windows[selected_window].position = event.mouse_position - selected_window_offset;
        }

        surface.display();
    }

    sf::Sprite Screen::draw_texture(sf::RenderTexture &render_texture, sf::Vector2f position) {
        const sf::Texture &texture = render_texture.getTexture();
        sf::Sprite sprite(texture);
        sprite.setPosition(position);
        surface.draw(sprite);
        return sprite;
    }

    Window::Window(Screen &parent, sf::Vector2f size, sf::Vector2f position):
    size(size), position(position),
    surface(static_cast<sf::Vector2u>(size), parent.get_context_settings()),
    sprite(surface.getTexture()) {
        
    }

    void Window::refresh(Screen &parent) {
        surface.clear(sf::Color(0, 0, 0));

        surface.display();
        sprite = parent.draw_texture(surface, position);
    }

    bool Window::contains(sf::Vector2f pos) {
        return sprite.getGlobalBounds().contains(pos);
    }

}