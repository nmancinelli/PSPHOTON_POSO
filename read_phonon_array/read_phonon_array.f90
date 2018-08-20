subroutine read_phonon_array(arrayfile,rbin,x1,x2,nxdim,t1,t2,ntdim)
	implicit none   
	real, dimension(10000,10000)   :: rbin
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

        call apply_spatial_filter(rbin, nxdim, ntdim, 10, 1)

	rbin=sqrt(rbin)

	return

end subroutine

subroutine apply_spatial_filter(A, nxdim, ntdim, itbuf, ixbuf)
        implicit none
        real, dimension(10000) :: tmp1
        real, dimension(10000,10000) :: A, B
        integer :: nxdim, ntdim, ii, jj, itbuf, ixbuf
        integer :: npts

        B=0.

        npts=(2*ixbuf+1) * (2*itbuf+1)

        do ii=1+itbuf,ntdim-itbuf
                do jj=1+ixbuf,nxdim-ixbuf
                        !tmp(1:(itbuf*ixbuf)) = reshape(A(ii-itbuf:ii+itbuf,jj-ixbuf:jj+ixbuf),(/itbuf*ixbuf/))
                  tmp1(1:npts) = reshape(A(ii-itbuf:ii+itbuf,jj-ixbuf:jj+ixbuf), (/npts/))
                  B(ii,jj)=sum(A(ii-itbuf:ii+itbuf,jj-ixbuf:jj+ixbuf))/npts
                  !call  SelectionSort(tmp1(1:npts))
                  !B(ii,jj) = tmp1((npts+1)/2)
                end do
        end do

        A=B

        return

contains

!-SelectionSort----------------------------------------------
! Subroutine to sort an array Item into ascending order using 
! the simple selection sort algorithm.  For descending order 
! change MINVAL to MAXVAL and MINLOC to MAXLOC.  Local 
! variables used are:
!   NumItems         : number of elements in array Item
!   LargestItem      : largest item in current sublist
!   MAXLOC_array     : one-element array returned by MINLOC
!   LocationLmallest : location of LargestItem
!   I                : subscript
!
! Accepts:  Array Item
! Returns:  Array Item (modified) with elements in ascending 
!           order
!
! Note:  Item is an assumed-shape array so a program unit that 
!        calls this subroutine must:
!        1. contain this subroutine as an internal subprogram,
!        2. import this subroutine from a module, or
!        3. contain an interface block for this subroutine. 
!--------------------------------------------------------------

SUBROUTINE SelectionSort(Item)

  REAL, DIMENSION(:), INTENT(INOUT) :: Item
  REAL :: LargestItem
  INTEGER :: NumItems, I, LocationLargest
  INTEGER, DIMENSION(1) :: MAXLOC_array

  NumItems = SIZE(Item)
  DO I = 1, NumItems - 1

     ! Find smallest item in the sublist 
     ! Item(I), ..., Item(NumItems)

     LargestItem = MAXVAL(Item(I:NumItems))
     MAXLOC_array = MAXLOC(Item(I:NumItems))
     LocationLargest = (I - 1) + MAXLOC_array(1)

     ! Interchange largest item with Item(I) at
     ! beginning of sublist

     Item(LocationLargest) = Item(I)
     Item(I) = LargestItem

  END DO


END SUBROUTINE SelectionSort

end subroutine

