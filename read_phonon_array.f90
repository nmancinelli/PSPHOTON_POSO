subroutine read_phonon_array(arrayfile,rbin,x1,x2,nxdim,t1,t2,ntdim)
	implicit none   
	real, dimension(3000,3000)   :: rbin
	real, dimension(10)          :: dummy
	character (len=200)          :: arrayfile
	integer                      :: it,ix

	real :: x1,x2,t1,t2,stnmin,stnmax,zsource
	integer :: ntdim,nxdim,iwstart,nray,nsurf

	real :: deldeg,delrad,degrad,sang,xbinwidth

	!f2py intent(in) arrayfile
	!f2py intent(out) rbin,x1,x2,nxdim,t1,t2,ntdim

	rbin=0.
	degrad=180./3.1415927

	open (11, file=arrayfile,form='unformatted')
	read (11) x1,x2,nxdim,t1,t2,ntdim,iwstart,stnmin,stnmax,zsource,zsource,nray,nsurf
	print *, x1,x2,nxdim,t1,t2,ntdim,iwstart,stnmin,stnmax,zsource,zsource,nray,nsurf
	read (11) dummy
	read (11) ((rbin(it,ix),it=1,ntdim),ix=1,nxdim)
	close (11)

	do ix=1,nxdim
		xbinwidth = (x2-x1)/real(nxdim-1)
		deldeg=(real(ix)-0.5)*xbinwidth + x1
		delrad=deldeg/degrad
		sang=sin(delrad)
		rbin(:,ix)=rbin(:,ix)/sang
		print *,'ix,deldeg,sang = ',ix,deldeg,sang
	end do

	rbin=sqrt(rbin)

	return

end subroutine

!subroutine window_around_pdiff(dt,del_deg,qdep,tstart,wt1,wt2,iw1,iw2)
!	implicit none
!	real :: dt, del_deg, qdep, t1, t2, wt1, wt2
!	real :: tt, tstart
!	integer, parameter :: npts = 3001
!	integer :: iflag,iw1,iw2
!	
!!f2py intent(in) dt,del_deg,qdep,tstart,wt1,wt2
!!f2py intent(out) iw1,iw2
!	
!	if (del_deg < 98) then
!	 call GET_TTS('/Users/njmancinelli/PROG/TT/tt91.p',1,del_deg,qdep,tt,iflag)
!	else
!	 call GET_TTS('/Users/njmancinelli/PROG/TT/tt91.Pdif',2,del_deg,qdep,tt,iflag)
!	endif
!	
!	tt=tt*60.0 !convert to seconds
!	
!	iw1 = nint((wt1+tt-tstart)/dt)
!	iw2 = nint((wt2+tt-tstart)/dt)
!	
!	if (iw1 <= 0)    iw1=1
!	if (iw2 >= npts) iw2=npts
!	return
!	
!end subroutine

!subroutine get_filter_wavelet(dt,f1,f2,npp,e)
!	implicit none
!	integer,parameter :: npts = 3001
!	real, dimension(npts) :: a,b,e
!	real :: f1,f2,dt
!	integer :: npp,ierr
!
!!f2py intent(in) dt,f1,f2,npp
!!f2py intent(out) e
!
!	a=0.0
!	a(1501)=1.0
!
!	call FILTER(a, b, npts, dt, f1, f2, npp, ierr)
!	if (ierr /= 0) then
!	   print *, '***Error in 1 FILTER, ierr = ', ierr
!	   stop
!	endif
!	call TILBERT(b,dt,npts,npp,e)
!	return
!	
!end subroutine
!	
!	
