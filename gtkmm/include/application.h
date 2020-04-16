#ifndef _APPLICATION_H_
#define _APPLICATION_H_

#include <gtkmm-3.0/gtkmm.h>
#include <cstdio>
#include <iostream>

#include "image.h"

class myApplication
{
    public:
        myApplication(const char *const filename);
        Gtk::Window *get_window();
    protected:
        Gtk::ColorButton *color_button;
        Gtk::Button *upd_color_btn;
        Gtk::Window *main_window;
        MyImageBox *image_box;
        void update_draw_color();
};

#endif


