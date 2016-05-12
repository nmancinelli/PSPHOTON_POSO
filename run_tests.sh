#!/bin/bash
function write_do_file {
cat << EOF > do.photon
./psphoton << !
sereno_orcutt
$1              !assumed freq. (Hz), affects attenuation and scattering
35.0             !assumed source depth (km)
5                !radiate: (1) P,  (2) SH, (3) SV, (4) SH/SV, (5) P+S, (6) custom Es/Ep, (7) custom pmax
50000            !number of ray parameters for tables (max=50000)
0 0 0 0          !xwind1,xwind2,twind1,twind2 for ray info dump
0                !0=normal, 1=force equal refl/trans
4                !number of interface depths (to follow) (max=6)
   0.0            !interface 1 (free-surface)
   4.0            !interface 2 (ocean-seds)
   7.0            !interface 2 (seds-crust)
   10.0           !interface 4 (moho)
4                !number of scattering volumes (to follow) (max=6)
  4              !min scat depth (km)
  10             !max scat depth (km)
  999999          !max scat range from source (km)
  5.80 3.36       !reference P & S velocity for layer
  0.8             !relative size of density perturbation (0.8 often assumed)
  0.0             !rms perturbation
  0.25 20.0        !scale length (km), aspect ratio (az/ax)
    10              !min scat depth (km)
    100             !max scat depth (km)
    999999          !max scat range from source (km)
    8.08 4.47       !reference P & S velocity for layer
    0.8             !relative size of density perturbation (0.8 often assumed)
    2.0              !rms perturbation
    10.0 0.05        !scale length (km), aspect ratio (az/ax)
  100             !min scat depth (km)
  300             !max scat depth (km)
  999999          !max scat range from source (km)
  8.08 4.47       !reference P & S velocity for layer
  0.8             !relative size of density perturbation (0.8 often assumed)
  2.0              !rms perturbation
  5.0 0.2        !scale length (km), aspect ratio (az/ax)
	300              !min scat depth (km)
	9999             !max scat depth (km)
	999999          !max scat range from source (km)
	8.08 4.47       !reference P & S velocity for layer
	0.8             !relative size of density perturbation (0.8 often assumed)
	0.0              !rms perturbation
	10.0 0.1        !scale length (km), aspect ratio (az/ax)
0 99999          !min,max number of scattering events for output
5                !number of intrinsic Q layers (to follow) (max=6)
  4 10            !min,max depth of Q layer
  300             !Qalpha
    10 100        !min,max depth of Q layer
    1000          !Qalpha
  100 250         !min,max depth of Q layer
  144             !Qalpha
    250 410       !min,max depth of Q layer
    358           !Qalpha
  410 9999        !min,max depth of Q layer
  6250            !Qalpha
200000           !write output at multiples of this number of rays
0                !out.debug: 0=none, 1=full, 2=scat
EOF
}
#
cd TEST0
rm out.debug
write_do_file 2.00
bash do.photon > tmp &
cd -
#
cd TEST1
rm out.debug
write_do_file 4.00
bash do.photon > tmp &
cd -
#
cd TEST2
rm out.debug
write_do_file 8.00
bash do.photon > tmp &
cd -
#
cd TEST3
rm out.debug
write_do_file 16.00
bash do.photon > tmp &
cd -
echo "  "
echo " Jobs launched. "
echo "  "

