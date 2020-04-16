CC = g++
INCLUDE_DIR = include/
BINARIES = $(patsubst src/%.cpp,bin/%.o, $(wildcard src/*.cpp))
# Remove -g if not in debug mode
GTK_FLAGS = `pkg-config gtkmm-3.0 --libs --cflags`
COMPILE_FLAGS = -Wall -g -Werror -Iinclude

.PHONY: all test clean
all: app.exe

app.exe: $(BINARIES)
	$(CC) $^ -o $@ -I $(INCLUDE_DIR) $(GTK_FLAGS) 

bin/%.o: src/%.cpp
	mkdir -p bin
	$(CC) -c -o $@ $(GTK_FLAGS) $(COMPILE_FLAGS) $^

clean:
	rm -rf bin/ app.exe

# g++ main.cpp -o app.exe `pkg-config gtkmm-3.0 --cflags --libs`
