#!/usr/bin/env python
#  This program reads in binary array from psphoton, makes corrections,
#    and converts to amplitude.
#  N. Mancinelli - 18 OCT 2013
#

import matplotlib
matplotlib.use('agg')
from matplotlib import pylab as plt
import numpy as np

def main():
	plt.figure(figsize=(11,8.5))
	ax1=plt.subplot(1,2,1)
	plot_traces(ax1,'TRIALS/TEST0/out.photon_rad','TRIALS/TEST0/out.photon_tran','Z', title='Radial Transverse')
	ax2=plt.subplot(1,2,2)
	plot_traces(ax2,'TRIALS/TEST4/out.photon_rad','TRIALS/TEST0/out.photon_tran','Z', title='Radial Transverse')

	plt.tight_layout()
	plt.savefig('wavefield.eps')

def plot_traces(ax0,fname1,fname2,component_label, title='', xlabel='T - X/8.2 (s)', ylabel='Range (km)'):

	A,t,x = loadMCarray_only(fname1)
	B,t,x = loadMCarray_only(fname2)
	#C = np.arctan2(B,A)
	C = np.log10(B) - np.log10(A)

	img=ax0.imshow(C,origin='lower',aspect='auto',extent=[np.min(x),np.max(x),np.min(t),np.max(t)])
	plt.colorbar(img)
	ax0.set_xlabel('Range (deg)')
	ax0.set_ylabel('Time  (s)')
	ax0.set_title(title)

	return

def runningMean(x, N):
	y = np.zeros((len(x),))
	for ctr in range(len(x)):
		 y[ctr] = np.sum(x[ctr:(ctr+N)])
	return y/N

def loadMCarray_only(arrayfile):
	"""
	1) loads array from binary file
	2) corrects for spherical surface area within each distance bin
	3) converts from power to amplitude

	"""
	import numpy
	import read_phonon_array as rpa
	
	model,x1,x2,nxdim,t1,t2,ntdim = rpa.read_phonon_array(arrayfile)
	model=model[:ntdim,:nxdim]
	print(x1,x2,nxdim,t1,t2,ntdim)
	rax=numpy.linspace(x1,x2,nxdim)
	tax=numpy.linspace(t1,t2,ntdim)

	#print 'correcting for spherical surface area within each distance bin...' 

	#for j in range(len(rax)):
	#	denom = numpy.sin(rax[j]*numpy.pi/180.0)
	#	if (abs(denom) > 0):
	#		model[:,j] = model[:,j]/denom
	#	else:
	#		model[:,j] = model[:,j]*0.0
#
#	print  'taking sqrt to get amplitude...'
#	model = model**0.5

	return model, tax, rax

main()

