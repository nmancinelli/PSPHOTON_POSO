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
	ax1=plt.subplot(3,2,1)
	ax2=plt.subplot(3,2,2)
	ax3=plt.subplot(3,2,3)
	ax4=plt.subplot(3,2,4)
	ax5=plt.subplot(3,2,5)
	ax6=plt.subplot(3,2,6)

	plot_traces(ax1,'TRIALS/TEST0/out.photon_z','Z', title='1 Hz')
	plot_traces(ax3,'TRIALS/TEST0/out.photon_rad','R')
	plot_traces(ax5,'TRIALS/TEST0/out.photon_tran','T')
	plot_traces(ax2,'TRIALS/TEST4/out.photon_z','Z', title='16 Hz')
	plot_traces(ax4,'TRIALS/TEST4/out.photon_rad','R')
	plot_traces(ax6,'TRIALS/TEST4/out.photon_tran','T')

	#cleanup
	for ax in [ax1,ax2,ax3,ax4]:
		ax.set_xlabel('')

	for ax in [ax2,ax4,ax6]:
		ax.set_ylabel('')

	plt.tight_layout()
	plt.savefig('wavefield.eps')

def plot_traces(ax0,fname,component_label, title='', xlabel='T - X/8.2 (s)', ylabel='Range (km)'):
	A,t,x = loadMCarray_only(fname)
	B = np.log10(A)

	ax0.text(-30.,50.,component_label,color='red')
	
	#pylab.subplot(nrow,2,iplt+1)
	for ii,eachx in enumerate(x):
		if np.mod(ii,10) != 0.0:
			continue
		range=eachx*111.1 #approx
		seis=A[:,ii]
		seis=runningMean(seis,20)
		#norm
		seis=seis/max(seis)
		tred=t-range/8.2
		ax0.fill_between(tred[:len(seis)],range,seis*100.0+range,color='black',linewidth=0.1)
	ax0.set_xlim([-50,250])
	ax0.set_ylim([-10.0,max(seis)*100.0+range])
	ax0.set_ylabel(ylabel)
	ax0.set_xlabel(xlabel)
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

