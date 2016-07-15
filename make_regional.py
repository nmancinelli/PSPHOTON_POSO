#!/usr/bin/env python
#
def main():
	from scipy.interpolate import interp1d
	from numpy import arange,concatenate
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
	
	#LVZ params
	LVZ=False
	LVZ_top = 10. #km
	LVZ_mid = 100. #km
	LVZ_bot = 400. #km
	#LVZ_reduction=0.94 #i.e., 1.0 for no reduction
	
	x = [LVZ_top,LVZ_mid,LVZ_bot]
	y = [4.7000,3.6000,4.7000]
	fun = interp1d(x, y)
	
	z1=0.0
	z2=558.0
	dz=1.0
	dd=0.0001
	erad=r[0]

	OCEAN_BOTTOM_Z=4.0 #km
	SEDS_CRUST1_Z=5.0 #km
	CRUST1_CRUST2_Z=7.0
	MOHO_Z=10.0

	VP_SED=1.6000
	VS_SED=0.4000
	RHO_SED=1.500

	disconts = []
	
	depths = concatenate([arange(0.,10.,0.1),arange(10.,z2,dz)])

	for depth in depths:
		if depth < OCEAN_BOTTOM_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 1.5000, 0.0000, 1.000)
		elif depth == OCEAN_BOTTOM_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 1.5000, 0.0000, 1.000)
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, VP_SED, VS_SED, RHO_SED)
		elif depth < SEDS_CRUST1_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, VP_SED, VS_SED, RHO_SED)
		elif depth == SEDS_CRUST1_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, VP_SED, VS_SED, RHO_SED)
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 4.4000, 2.2000, 1.920)
		elif depth < CRUST1_CRUST2_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 4.4000, 2.2000, 1.920)
		elif depth == CRUST1_CRUST2_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 4.4000, 2.2000, 1.920)
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 6.5000, 3.5000, 2.800)
		elif depth < MOHO_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 6.5000, 3.5000, 2.800)
		elif depth == MOHO_Z:
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 6.5000, 3.5000, 2.800)
			print '%f  %f  %f  %f  %f' % (depth, erad-depth, 8.2000, 4.7000, 3.320)
		else:
			if depth >= LVZ_top and depth <= LVZ_bot and LVZ==True:
				print '%f  %f  %f  %f  %f' % (depth, erad-depth, 8.2000, fun(depth), 3.320)
			else:
				print '%f  %f  %f  %f  %f' % (depth, erad-depth, 8.2000, 4.7000, 3.320)
			
	depth=erad		
	print '%f  %f  %f  %f  %f' % (depth, erad-depth, 8.2000, 4.7000, 3.320)
main()
