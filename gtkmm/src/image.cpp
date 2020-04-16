#include "image.h"
#define LEFT_CLICK 1
#define RIGHT_CLICK 3


void MyImageBox::put_pixel(const int x, const int y)
{
    unsigned char *pixel_arr = surface->get_data(); 
    for (int i = 0; i < 4; i++)
        pixel_arr[(y * image_width + x) * 4 + i] = color_arr[i];
}


bool MyImageBox::on_button_press_event(GdkEventButton* event)
{
    static int start_p[2] = { -1, -1 };
    static int prev_p[2] = { -1, -1 };
    int x = (int) event->x, y = (int) event->y;

    if (event->button == LEFT_CLICK)
    {
        if (prev_p[0] != -1)
        {
            image->set(surface);
            draw_section(this, Point(prev_p[0], prev_p[1]), Point(x, y));
            prev_p[0] = x, prev_p[1] = y;
        }
        else
            start_p[0] = prev_p[0] = x, start_p[1] = prev_p[1] = y;
    }

    else if (event->button == RIGHT_CLICK)
    {
        if (prev_p[0] != -1 && (prev_p[0] != start_p[0] || prev_p[1] != start_p[1]))
        {
            image->set(surface);
            draw_section(this, Point(prev_p[0], prev_p[1]), Point(start_p[0], start_p[1]));
            prev_p[0] = -1; 
        }
    }
    return true;
}


void MyImageBox::create_surface_for_image()
{
    if (!image)
        return;

    surface = Cairo::ImageSurface::create(Cairo::FORMAT_ARGB32, image_width, image_height);
    image->set(surface);
    pixel_arr = surface->get_data();
}


void MyImageBox::set_image(Gtk::Image *&image_arg)
{
    image = image_arg;
    image->get_size_request(image_width, image_height);
}


void MyImageBox::update_draw_color(Gdk::RGBA color)
{
    color_arr[0] = color.get_blue() * DOUBLE_TO_255, color_arr[1] = color.get_green() * DOUBLE_TO_255,
        color_arr[2] = color.get_red() * DOUBLE_TO_255, color_arr[3] = color.get_alpha() * DOUBLE_TO_255;
}


void MyImageBox::clear_image()
{
    Cairo::RefPtr<Cairo::Context> cr = Cairo::Context::create(surface);

    cr->set_source_rgb(1, 1, 1);
    cr->paint(); // fill image with the color
}
