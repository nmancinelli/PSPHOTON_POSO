from os import mkdir, chdir, getcwd, symlink
from subprocess import Popen

class ModelSuite():
    def __init__(self, name='TRIALS', param_to_test='freq', base_file='BASE_DOFILES/do.photon', values_to_test=[], SLURM = True):

        root = getcwd()

        mkdir(name)

        procs = []

        for _i, value in enumerate(values_to_test):
            newdir = '{}/TEST{}'.format(name, _i)
            mkdir(newdir)
            chdir(newdir)
            tmp = '%s/%s' % (root, base_file)

	    #Test 
            write_dofile(tmp, freq=value)

            #create sym links
            symlink('%s/bin/psphoton' % root,'psphoton')
            symlink('%s/BACKGROUND_VELOCITY_MODELS/sereno_orcutt' % root,'sereno_orcutt')

            #launch program
            cmd = 'do.photon'
            if SLURM:
                cmd = 'sbatch -n 1 -t 24:00:00 --mem=2G %s' % cmd
            else:
                cmd = 'bash %s' % cmd
            proc = Popen(cmd, shell=True)
            procs.append(proc)
            chdir(root)

def write_dofile(base_file, freq=1.0, source_depth_in_km=35.0, rms_crust=0.025, Qalpha_at_3_Hz=7200, Qalpha_in_the_water=999999, Qalpha_in_the_crust=180, radiate=5):
	"""For frequency only"""
	lines = open(base_file,'r').readlines()

	fout = open('do.photon','w')

	for _i, line in enumerate(lines):
		if _i == 4:
			nfo = line.split()
			tmp = '%.5f' % freq
			assert( len(tmp) >= len(nfo[0]) )
			line  = tmp + line[len(tmp):]

		elif _i == 5:
			nfo = line.split()
			tmp = '%5.1f' % source_depth_in_km
			assert( len(tmp) >= len(nfo[0]) )
			line  = tmp + line[len(tmp):] 

		elif _i == 22:
			nfo = line.split()
			rms = rms_crust
			tmp = '%5.3f' % rms
			assert( len(tmp) >= len(nfo[0]) )
			line  = tmp + line[len(tmp):] 

		elif _i == 50:
			nfo = line.split()
			Q = Qalpha_in_the_crust
			tmp = '%8d' % Q
			assert( len(tmp) >= len(nfo[0]) )
			line  = tmp + line[len(tmp):] 

		elif _i == 48:
			nfo = line.split()
			Q = Qalpha_in_the_water
			tmp = '%8d' % Q
			assert( len(tmp) >= len(nfo[0]) )
			line  = tmp + line[len(tmp):] 

		elif _i == 52:
			nfo = line.split()
			Q = Qalpha_at_3_Hz * (freq/3.)**0.3
			tmp = '%8d' % Q

			assert( len(tmp) >= len(nfo[0]) )

			line  = tmp + line[len(tmp):]

		elif _i == 6:
			nfo = line.split()
			tmp = '%1d' % radiate
			assert( len(tmp) >= len(nfo[0]) )
			line  = tmp + line[len(tmp):]

		fout.write(line)

	return

def test():
    ModelSuite(values_to_test=[1., 2., 4., 8., 16.])
    #ModelSuite(values_to_test=[10, 25, 50, 75, 100])
