This example runs IMPACT-T to L0AFEND and saves the particles in a specified directory.  These particles are read by Bmad and tracked the rest of the way.  A few notes:

1) the initial distribution is defined by the VCC for the two spatial dimensions, a 1-D truncated gaussian for the time dimension, and by the MTE for the 3 momenta.  These are specified in distgen.yaml.  If one wants to see an example of a radial spatial profile, one can use the commented r_dist in distgen.yaml.  Additional distgen distributions are listed here: https://colwyngulliford.github.io/distgen/examples/example_dists/

2) With large particle numbers i.e. more than 250k macroparticles, Bmad can run really slowly due to the short-range wakefield calculation.  If suitable for the simulations, commenting lines 62-64 in $FACET2_LATTICE/bmad/models/f2_elec/f2_elec.lat.bmad will turn off this calculation.

3)  Outputs from these scripts, including sample handoff beams (L0AFEND.h5) are included for 1.6nC and 2nC with 200k macroparticles. 