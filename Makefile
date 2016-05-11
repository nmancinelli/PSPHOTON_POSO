OBJS5= ~/PROG/SHEARER/EFS/disk2.o\
        ~/PROG/SHEARER/EFS/efs_subs.o \
	~/PROG/SHEARER/TS/filter_f90.o \
	~/PROG/SHEARER/SUBS/get_tts.o \
	~/PROG/SHEARER/SUBS/sphere_subs.o \
	~/PROG/SHEARER/SUBS/datetime.o \
	~/PROG/SHEARER/SUBS/anycell.o \
	~/PROG/SHEARER/SUBS/pickseis.o

psphoton: Makefile psphoton.f90
	gfortran -O psphoton.f90 -o psphoton
	
read_phonon_array: Makefile read_phonon_array.f90
	f2py --overwrite-signature read_phonon_array.f90 -m read_phonon_array -h read_phonon_array.pyf
	f2py -c read_phonon_array.pyf read_phonon_array.f90
