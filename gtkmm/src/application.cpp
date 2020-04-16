#include "application.h"
#include <iostream>


myApplication::myApplication(const char* const filename)
{
    Glib::RefPtr<Gtk::Builder> builder = Gtk::Builder::create();
    builder->add_from_file(filename);

    builder->get_widget("main_window", main_window);

    // main window CONFIG (color, title and etc.)
    // ==========================================
    main_window->set_title("Just title");
    Gdk::RGBA color, color2;
    color.set_rgba(0.1, 0.1, 0.3); // grey
    color2.set_rgba(0.9, 0.15, 0.3); // blue
    main_window->override_background_color(color);
    // ==========================================

    // get all widgets
    builder->get_widget_derived("main_ebox", image_box);
    builder->get_widget("color_button", color_button);
    builder->get_widget("update_color_button", upd_color_btn);
    Gtk::Image *tmp_image;
    builder->get_widget("main_image", tmp_image);

    // image routine
    image_box->set_image(tmp_image);
    image_box->create_surface_for_image();
    image_box->clear_image();

    // connect color chooser button
    upd_color_btn->signal_clicked().connect(sigc::mem_fun(*this, &myApplication::update_draw_color));

}


Gtk::Window * myApplication::get_window()
{
    return main_window;
}

void myApplication::update_draw_color()
{
    Gdk::RGBA color = color_button->get_rgba();
    image_box->update_draw_color(color);
}
