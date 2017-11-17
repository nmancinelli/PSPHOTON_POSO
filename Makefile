all:
	make bin/psphoton
	make lib

clean:
	rm psphoton

bin/psphoton: Makefile psphoton.f90
	mkdir -p bin
	gfortran -O psphoton.f90 -o bin/psphoton
	
.phony:
	clean

lib:
	+$(MAKE) -C read_phonon_array
