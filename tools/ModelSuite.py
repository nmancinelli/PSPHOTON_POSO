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
            write_dofile(tmp, radiate=value)

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

def write_dofile(base_file, freq=16.0, Qalpha_at_3_Hz=7200, radiate=5):
    """For frequency only"""
    lines = open(base_file,'r').readlines()

    fout = open('do.photon','w')

    for _i, line in enumerate(lines):
        if _i == 4:
            nfo = line.split()
            tmp = '%.5f' % freq

            assert( len(tmp) >= len(nfo[0]) )

            line  = tmp + line[len(tmp):]

        elif _i == 50:
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

def test():
    #ModelSuite(values_to_test=[1., 2., 4., 8., 16.])
    ModelSuite(values_to_test=[2, 3, 5])
