#include <cstdio>
#include <gtkmm-3.0/gtkmm.h>
#include "../include/application.h"


int main(int argc, char *argv[])
{
    setbuf(stdout, NULL);
    auto app = Gtk::Application::create(argc, argv);

    const char *forms_filename;
    forms_filename= "meta/viewer.glade";

    myApplication application(forms_filename);  
    return app->run(*application.get_window());
}

