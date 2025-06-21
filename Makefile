all: run clean
run:
	python3 main.py main.c 
	gcc -o output generated.s
	
clean: 
	rm -rf generated.s