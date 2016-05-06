#!/usr/bin/env python
#
def main():
	from scipy.interpolate import interp1d
	from numpy import arange
	fin=open('iasp91.smo')
	z,r,vp,vs,rho=[],[],[],[],[]
	for line in fin.readlines():
		nfo=line.strip('\n').split()
		tmp0=float(nfo[0])
		tmp1=float(nfo[1])
		tmp2=float(nfo[2])
		tmp3=float(nfo[3])
		tmp4=float(nfo[4])
		z.append(tmp0)
		r.append(tmp1)
		vp.append(tmp2)
		vs.append(tmp3)
		rho.append(tmp4)

	fvp=interp1d(z,vp)
	fvs=interp1d(z,vs)
	frho=interp1d(z,rho)

	z1=0.0
	z2=650.0
	dz=1.0
	dd=0.0001
	erad=r[0]

	OCEAN_BOTTOM_Z=4.0 #km
	MOHO_Z=10.0


	disconts = []

	for depth in arange(z1,z2,dz):
		if depth < OCEAN_BOTTOM_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 1.5000, 0.0000, 1.000)
		elif depth == OCEAN_BOTTOM_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 1.5000, 0.0000, 1.000)
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, fvp(depth+dd), fvs(depth+dd), frho(depth+dd))
		elif depth < MOHO_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 6.5000, 3.5000, 2.800)
		elif depth == MOHO_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 6.5000, 3.5000, 2.800)
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 8.2000, 4.7000, 3.320)
		elif depth in disconts:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, fvp(depth-dd), fvs(depth-dd), frho(depth-dd))
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, fvp(depth+dd), fvs(depth+dd), frho(depth+dd))
		else:
			#print '%f  %f  %f  %f  %f' % (depth, erad-depth, fvp(depth), fvs(depth), frho(depth))
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 8.2000, 4.7000, 3.320)
	
	depth=erad		
	print '%f  %f  %f  %f  %f' % (depth, erad-depth, 8.2000, 4.7000, 3.320)
main()
