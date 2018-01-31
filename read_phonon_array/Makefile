read_phonon_array: Makefile read_phonon_array.f90
	f2py3 --overwrite-signature read_phonon_array.f90 -m read_phonon_array -h read_phonon_array.pyf
	f2py3 -c read_phonon_array.pyf read_phonon_array.f90

clean:
	rm -rf *.so* *.pyf

.phony:
	clean
