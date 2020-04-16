#include "section_algorythm.h"
#include <math.h>

template <typename T>
void draw_section(T* const &canvas, const Point from, const Point to)
{
    int xb = from.get_x();
    int yb = from.get_y();
    int xe = to.get_x();
    int ye = to.get_y();

    canvas->put_pixel(xb, yb);

    int limit = MAX(ABS(ye - yb), ABS(xe - xb));

    double dy = (double) (ye - yb) / limit, dx = (double) (xe - xb) / limit;
    double x = xb, y = yb;

    for (int i = 0; i < limit; i++)
    {
        x += dx;
        y += dy;
        
        canvas->put_pixel(round(x), round(y));
    }
}
