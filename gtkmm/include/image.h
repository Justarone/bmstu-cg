#ifndef _IMAGE_H_
#define _IMAGE_H_

#include <cstdio>
#include <gdkmm-3.0/gdkmm.h>
#include <gtkmm-3.0/gtkmm.h>
#include "section_algorythm.h"

#define DOUBLE_TO_255 255

class MyImageBox: public Gtk::EventBox
{
    public:
        MyImageBox()
        {
            add_events(Gdk::BUTTON_PRESS_MASK | Gdk::BUTTON_RELEASE_MASK);
        }
        MyImageBox(BaseObjectType* cobject, const Glib::RefPtr<Gtk::Builder> &builder) : Gtk::EventBox(cobject) {
            add_events(Gdk::BUTTON_PRESS_MASK | Gdk::BUTTON_RELEASE_MASK);
        };

        void set_image(Gtk::Image *&image);
        void create_surface_for_image();
        void update_draw_color(Gdk::RGBA color);
        void clear_image();
        void put_pixel(const int x, const int y);
        virtual ~MyImageBox() {};

        Cairo::RefPtr<Cairo::ImageSurface> surface;
        unsigned char *pixel_arr;

    protected:
        Gtk::Image *image;
        int image_width;
        int image_height;
        unsigned char color_arr[4] = { 0, 0, 0, 255 };
        bool on_button_press_event(GdkEventButton* event) override;
};

#endif
