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

	plot_row(ax1,ax2,'out.photon_p','p')
	plot_row(ax3,ax4,'out.photon_sv','sv')
	plot_row(ax5,ax6,'out.photon_sh','sh')
	plt.tight_layout()
	plt.savefig('wavefield.eps')

def plot_row(ax1,ax2,fname,component_label):
	A,t,x = loadMCarray_only(fname)
	B = np.log10(A)
	#fig = pylab.figure()
	#ax1=pylab.subplot(nrow,2,iplt)
	img=ax1.imshow(B,origin='lower',aspect='auto',
		extent=[np.min(x),np.max(x),np.min(t),np.max(t)])
		
	ax1.set_xlabel('Range (deg)')
	ax1.set_ylabel('Time  (s)')
	ax1.text(18.,50.,component_label,color='white')
	# Now adding the colorbar
	#cbaxes = fig.add_axes([0.25, 0.2, 0.2, 0.015]) 
	#cb = pylab.colorbar(img, cax = cbaxes,orientation='horizontal')
	#cb.set_label(r'log$_{10}$[A]')
	
	#pylab.subplot(nrow,2,iplt+1)
	for ii,eachx in enumerate(x):
		if np.mod(ii,10) != 0.0:
			continue
		range=eachx*111.1 #approx
		seis=A[:,ii]
		seis=runningMean(seis,20)
		tred=t-range/8.2
		ax2.plot(tred[:len(seis)], np.log10(seis), linewidth=0.3)
	ax2.set_xlim([-50,350])
	ax2.set_ylim([0.0,6.5])
	ax2.set_ylabel('log10[Amplitude]')
	ax2.set_xlabel('T - X/8.2 (s)')
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

