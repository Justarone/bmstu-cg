#ifndef _SECTION_ALGORYTHM_
#define _SECTION_ALGORYTHM_

class Point
{
    private:
        int x, y;
    public:
        Point(int x_value = -1, int y_value = -1): x(x_value), y(y_value) {};
        int get_y() const { return y; };
        int get_x() const { return x; };
        void set_x(const int value) { x = value; };
        void set_y(const int value) { y = value; };
};

template <typename T>
void draw_section(T* const &canvas, const Point from, const Point to);

#include "section_algorythm.hpp"

#endif
