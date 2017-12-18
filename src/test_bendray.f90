program test_bendray
      implicit none
      real    :: a1(3),a2(3),a3(3),b1(3),b2(3),b3(3),c1(3),c2(3),c3(3)
      real    :: psi,zeta,spol,s_psi,s_zeta
      integer :: i, iter
      real :: gpp,gps,gsp,gss

      do iter = 1,4000

      a1(1) = 1.
      a1(2) = 0.
      a1(3) = 0.
      
      a2(1) = 0.
      a2(2) = 1.
      a2(3) = 0.

      a3(1) = 0.
      a3(2) = 0.
      a3(3) = 1.

      b1=a1
      b2=a2
      b3=a3

      do i = 1,2000 
        print *, 'Enter psi, zeta'
        read *, psi, zeta
        print *,'psi, zeta = ', psi, zeta 
        call GSATO(psi,zeta,1000,0.8,1.7,0.025,1,gpp,gps,gsp,gss,spol)
        print *, 'gpp,gps,gsp,gss,spol = ', gpp,gps,gsp,gss,spol
        a1=b1
        a2=b2
        a3=b3
        print *, a1, a2, a3      
        call BENDRAY(a1,a2,a3,psi,zeta,spol)
        print *, a1, a2, a3
        print *, '-------------------'
      end do

        print *, a1, a2, a3 

      end do
end program

! XSATO computes (4.50) from Sato and Fehler
!   Inputs:  psi  =  spherical coor. angle (radians)
!            zeta =  sph. coor angle from x3 (radians)
!            nu   =  density vs. velocity pert. scaling (see 4.48)
!            gam0 =  Pvel/Svel (often assumed = sqrt(3) )
!   Returns: xpp, xps, xsp, xss_psi, xss_zeta  =  from eqn. (4.50)
!
      subroutine XSATO(psi,zeta,nu,gam0, &
                       xpp,xps,xsp,xss_psi,xss_zeta)
      implicit none
      real :: psi,zeta,nu,gam0,xpp,xps,xsp,xss_psi,xss_zeta
      real :: gam2,cpsi,c2psi,spsi,czeta,szeta

      gam2=gam0**2

      cpsi=cos(psi)
      c2psi=cos(2.*psi)
      spsi=sin(psi)
      czeta=cos(zeta)
      szeta=sin(zeta)

      xpp = (1./gam2) * (nu * (-1. + cpsi   &
           + (2./gam2)*spsi**2) -2. + (4./gam2)*spsi**2)

      xps = -spsi*(nu*(1.-(2./gam0)*cpsi)-(4./gam0)*cpsi)

      xsp = (1./gam2) * spsi*czeta*(nu*(1.-(2./gam0)*cpsi)  &
                  -(4./gam0)*cpsi)

      xss_psi = czeta*(nu*(cpsi-c2psi)-2.*c2psi)

      xss_zeta = szeta*(nu*(cpsi-1.)+2.*cpsi)

      return
      end


! function EXPSATO computes (2.10) from Sato and Fehler
!    Inputs:  eps  =  RMS velocity perturbation
!             a    =  correlation distance
!             m    =  wavenumber
!    Returns: P(m) =  PSDF (Power Spectral Density Function)
!
      real function EXPSATO(eps,a,m)
      implicit none
      real :: eps,a,m,pi
      pi=3.141592654
      expsato=(8.*pi*eps**2*a**3)/(1.+a**2*m**2)**2
      return
      end

! GSATO computes (4.52) from Sato and Fehler (exponential autocor)
!   Inputs:  psi  =  spherical coor. angle (radians)
!            zeta =  sph. coor angle from x3 (radians)
!            el   =  S-wave wavenumber (=om/beta0)
!            nu   =  density vs. velocity pert. scaling (see 4.48)
!            gam0 =  Pvel/Svel (often assumed = sqrt(3) )
!            eps  =  RMS velocity perturbation
!            a    =  correlation distance
!   Returns: gpp,gps,gsp,gss  =  from eqn. (4.52)
!            spol =  S-to-S scattered S polarization (radians)
!                 =  0 for pure psi direction
!
       subroutine GSATO(psi,zeta,el,nu,gam0,eps,a, &
             gpp,gps,gsp,gss,spol)
      implicit none
      real :: psi,zeta,el,nu,gam0,eps,a,gpp,gps,gsp,gss,spol
      real :: pi4,el4,gam2,arg
      real :: xpp,xps,xsp,xss_psi,xss_zeta
      real :: EXPSATO
      pi4=4.*3.141592754
      el4=el**4
      gam2=gam0**2

      call XSATO(psi,zeta,nu,gam0, &
                       xpp,xps,xsp,xss_psi,xss_zeta)

      arg=(2.*el/gam0)*sin(psi/2.)
      gpp = (el4/pi4)*xpp**2*EXPSATO(eps,a,arg)
      if (gpp.lt.1.e-30) gpp=0.

      arg=(el/gam0)*sqrt(1.+gam2-2.*gam0*cos(psi))
      gps = (1./gam0)*(el4/pi4) * xps**2 * EXPSATO(eps,a,arg)
      if (gps.lt.1.e-30) gps=0.

      gsp = gam0*(el4/pi4) * xsp**2 * EXPSATO(eps,a,arg)
      if (gsp.lt.1.e-30) gsp=0.

      arg=2.*el*sin(psi/2.)
      gss = (el4/pi4)*(xss_psi**2+xss_zeta**2)*EXPSATO(eps,a,arg)
      if (gss.lt.1.e-30) gss=0.
      spol=atan2(xss_zeta,xss_psi)

      print *, 'zeta, psi, spol, xss_zeta, xss_psi = ', zeta, psi, spol, xss_zeta, xss_psi

      return
      end


! BENDRAY updates the ray and polarization direction vectors for
! the scattered ray.  The a1,a2,a3 vectors are overwritten with
! their new values.
! Inputs:
!     a1 = x1 axis in Sato and Fehler (S polarization direction)
!     a2 = x2 axis in S&F
!     a3 = x3 axis in S&F (ray direction)
!     psi = scattering angle from a3 (radians)
!     zeta = scattering angle from a1 (radians)
!     spol = scattered S polarization (radians) 
!            (=0 for pure psi polarization)
!            Note that this polarization is w.r.t the plane defined
!            by the incident and scattered ray vectors.  It is not
!            w.r.t the initial S polarization direction.
!
      subroutine BENDRAY(a1,a2,a3,psi,zeta,spol)
      implicit none
      real    :: a1(3),a2(3),a3(3),b1(3),b2(3),b3(3),c1(3),c2(3),c3(3)
      real    :: psi,zeta,spol,s_psi,s_zeta
      integer :: i
      do i=1,3
         b1(i)=0.
         b2(i)=0.
         b3(i)=0.
         c1(i)=0.
         c2(i)=0.
         c3(i)=0.
      enddo
      s_psi=0.
      s_zeta=0.
      i=0

! define b vectors to be cartesian coor. of e_r, e_psi, e_zeta (S&F Fig.
! 4.1)
      b3(3)=cos(psi)             !new ray direction
      b3(1)=sin(psi)*cos(zeta)
      b3(2)=sin(psi)*sin(zeta)
      b1(3)=-sin(psi)            !sets psi direction to b1
      b1(1)= cos(psi)*cos(zeta)
      b1(2)= cos(psi)*sin(zeta)
      call CROSS(b3,b1,b2)       !sets zeta direction to b2

! define c vectors in terms of S polarization coordinates
      s_psi=cos(spol)
      s_zeta=sin(spol)
      c1(1) = b1(1)*s_psi + b2(1)*s_zeta
      c1(2) = b1(2)*s_psi + b2(2)*s_zeta
      c1(3) = b1(3)*s_psi + b2(3)*s_zeta
      call VECVEC(b3,c3)
      call CROSS(c3,c1,c2)

! now set b vectors to new ray based vectors using a and c vectors
      do i=1,3
         b1(i) = c1(1)*a1(i) + c1(2)*a2(i) + c1(3)*a3(i)
         b2(i) = c2(1)*a1(i) + c2(2)*a2(i) + c2(3)*a3(i)
         b3(i) = c3(1)*a1(i) + c3(2)*a2(i) + c3(3)*a3(i)
      enddo

! now set a vectors to b vectors
      call VECVEC(b1,a1)
      call VECVEC(b2,a2)
      call VECVEC(b3,a3)

      return
      end


      subroutine VDOT(v1,v2,dot)
      implicit none
      real :: v1(3),v2(3),dot
      dot=v1(1)*v2(1)+v1(2)*v2(2)+v1(3)*v2(3)
      return
      end

      subroutine CROSS(v1,v2,v3)
      implicit none
      real :: v1(3),v2(3),v3(3)
      v3(1)=v1(2)*v2(3)-v1(3)*v2(2)   !set v3 to v1 cross v2
      v3(2)=v1(3)*v2(1)-v1(1)*v2(3)
      v3(3)=v1(1)*v2(2)-v1(2)*v2(1)
      return
      end

      subroutine VECVEC(v1,v2)
      implicit none
      real :: v1(3),v2(3)
      v2(1)=v1(1)          !set v2 to v1
      v2(2)=v1(2)
      v2(3)=v1(3)
      return
      end
