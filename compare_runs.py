#!/usr/bin/env python
#
def main():
	from matplotlib import pylab as plt
	plt.style.use('ggplot')
	plt.figure(figsize=(5,10))
	ax=plt.subplot(1,1,1)
	plot_model(ax,'TEST0/out.photon_rad','blue',label='0.05')
	#plot_model(ax,'TEST1/out.photon_rad','yellow',label='0.25')
	#plot_model(ax,'TEST2/out.photon_rad','orange',label='0.5')
	plot_model(ax,'TEST3/out.photon_rad','red',label='1')
	
	ax.set_title('Radial Amplitude')
	ax.set_ylabel('Range (km)')
	ax.set_xlabel('T - X/8.2 (s)')
	plt.legend(fontsize=8, title='Aspect Ratio', fancybox=True, loc='upper left')
	plt.xlim(-100,300)
	plt.ylim(200,2300)
	plt.tight_layout()
	plt.savefig('mypost.eps')

def plot_model(ax,fname,color,label=''):
	from matplotlib import pylab
	import numpy as np
	A,t,x = loadMCarray_only(fname)

	#pylab.subplot(nrow,2,iplt+1)
	for ii,eachx in enumerate(x):
		if np.mod(ii,20) != 0.0 or ii == 0:
			continue
		range=eachx*111.1 #approx
		seis=A[:,ii]
		seis=runningMean(seis,40)
		#norm
		seis=seis/max(seis)
		tred=t-range/8.2
		ax.plot(tred[:len(seis)],seis*200.0+range,color=color,linewidth=0.6)
	ax.plot([],[],color=color,linewidth=0.6,label=label)

def runningMean(x, N):
	import numpy as np
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

	return model, tax, rax
		
main()
