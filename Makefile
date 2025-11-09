COMPILER = g++
COMPFLAG = -std=c++23

INCLUDE = -I/Users/jason/Documents/CS/lib/sfml/include \
		  -I./include
LIB = -L/Users/jason/Documents/CS/lib/sfml/lib
LINKED = -lsfml-system -lsfml-window -lsfml-graphics -lsfml-audio -lsfml-network

SRC = src/main.cpp src/windoughs.cpp
OUT = main


all: $(SRC)
	$(COMPILER) $(COMPFLAG) $(SRC) $(INCLUDE) $(LIB) $(LINKED) -o $(OUT)
	./$(OUT)

run: $(OUT)
	./$(OUT)

clean:
	rm -f $(OUT)