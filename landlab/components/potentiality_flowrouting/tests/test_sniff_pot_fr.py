"""Test potentiality flowrouter.

This tester turns over the potentiality flowrouter to ensure basic
functionality is working.

Probably doesn't account for cell area yet.
"""
import os

import numpy as np
from numpy.testing import assert_array_equal, assert_allclose

from landlab import RasterModelGrid, ModelParameterDictionary
from landlab.components import PotentialityFlowRouter

NROWS = 10
NCOLS = 10
DX = 1000.


def test_sheetflow():
    flux = np.array(
        [1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
         1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
         1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
         1.00000000e+00,   1.00000000e+00,   1.00000000e+06,
         1.87867966e+06,   2.72182541e+06,   3.54415588e+06,
         4.35303038e+06,   5.15223689e+06,   5.94408409e+06,
         6.73016503e+06,   6.51166745e+06,   1.00000000e+00,
         1.00000000e+06,   2.12132034e+06,   3.24264069e+06,
         4.35965005e+06,   5.47056275e+06,   6.57568517e+06,
         7.67583899e+06,   8.77188984e+06,   8.86460677e+06,
         1.00000000e+00,   1.00000000e+06,   2.00000000e+06,
         3.03553391e+06,   4.08578644e+06,   5.14392129e+06,
         6.20695360e+06,   7.27341175e+06,   8.34244102e+06,
         8.41347211e+06,   1.00000000e+00,   1.00000000e+06,
         2.00000000e+06,   3.00000000e+06,   4.01040764e+06,
         5.03248558e+06,   6.06512434e+06,   7.10666517e+06,
         8.15550411e+06,   8.21025766e+06,   1.00000000e+00,
         1.00000000e+06,   2.00000000e+06,   3.00000000e+06,
         4.01040764e+06,   5.03248558e+06,   6.06512434e+06,
         7.10666517e+06,   8.15550411e+06,   8.21025766e+06,
         1.00000000e+00,   1.00000000e+06,   2.00000000e+06,
         3.03553391e+06,   4.08578644e+06,   5.14392129e+06,
         6.20695360e+06,   7.27341175e+06,   8.34244102e+06,
         8.41347211e+06,   1.00000000e+00,   1.00000000e+06,
         2.12132034e+06,   3.24264069e+06,   4.35965005e+06,
         5.47056275e+06,   6.57568517e+06,   7.67583899e+06,
         8.77188984e+06,   8.86460677e+06,   1.00000000e+00,
         1.00000000e+06,   1.87867966e+06,   2.72182541e+06,
         3.54415588e+06,   4.35303038e+06,   5.15223689e+06,
         5.94408409e+06,   6.73016503e+06,   6.51166745e+06,
         1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
         1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
         1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
         1.00000000e+00])

    mg = RasterModelGrid((NROWS, NCOLS), (DX, DX))
    z = (3000. - mg.node_x) * 0.5
    mg.at_node['topographic__elevation'] = z

    mg.set_closed_boundaries_at_grid_edges(False, True, True, True)
    mg.add_ones('node', 'water__unit_flux_in')

    pfr = PotentialityFlowRouter(mg)
    pfr.route_flow()

    assert_allclose(mg.at_node['surface_water__discharge'], flux)


def test_in_network():
    # a valley network produced by stream power:
    z = np.array([3.12900830e-04,   3.66462671e-04,   9.44438515e-04,
                  1.45006772e-04,   1.91406099e-04,   4.42053204e-04,
                  2.99818052e-04,   5.45267467e-04,   4.12129514e-04,
                  7.43816953e-04,   1.59251681e-04,   7.39577249e+01,
                  6.68718419e+01,   2.95535987e+01,   7.69715256e+01,
                  4.61083179e+01,   5.70611522e+01,   6.99664564e+01,
                  8.29355817e+01,   5.85563532e-04,   2.60300016e-04,
                  8.99636726e+01,   1.11946320e+02,   5.16553709e+01,
                  1.38432251e+02,   1.02903579e+02,   1.27601424e+02,
                  8.59469601e+01,   4.77495429e+01,   8.00781223e-04,
                  4.13095981e-04,   7.41309307e+01,   1.31747968e+02,
                  1.11724617e+02,   1.71687943e+02,   1.93482716e+02,
                  1.61044205e+02,   1.34775824e+02,   7.63077925e+01,
                  8.85837646e-04,   6.94907676e-04,   5.53654246e+01,
                  9.95405009e+01,   1.81345288e+02,   1.88975196e+02,
                  1.78104180e+02,   1.75231160e+02,   1.14932425e+02,
                  5.12018382e+01,   1.26501797e-04,   8.34527300e-04,
                  8.80562940e+01,   1.24009142e+02,   1.55635807e+02,
                  1.56683637e+02,   1.62398410e+02,   1.04070282e+02,
                  6.99665030e+01,   6.41256897e+01,   5.50951003e-04,
                  2.02545919e-04,   3.05799760e+01,   5.02285119e+01,
                  8.31442034e+01,   1.75898080e+02,   1.80095770e+02,
                  1.23416767e+02,   6.97604901e+01,   3.04864568e+01,
                  4.42047775e-04,   5.75778629e-04,   8.13990441e+01,
                  1.17362500e+02,   1.35317452e+02,   1.78842796e+02,
                  9.65391990e+01,   1.16520146e+02,   1.59289373e+02,
                  8.29784784e+01,   4.21911459e-04,   7.83145812e-04,
                  8.44510235e+01,   6.85512072e+01,   3.99258990e+01,
                  9.07740020e+01,   4.47116751e+01,   1.05333999e+02,
                  1.04965376e+02,   6.42615041e+01,   8.48184002e-04,
                  9.92952214e-04,   5.44805365e-04,   6.83657298e-04,
                  4.27967811e-04,   4.40101095e-04,   5.47248461e-04,
                  5.77178429e-06,   4.39642103e-04,   4.80194778e-04,
                  9.24014550e-04])

    flux = np.array(
       [ 0.71259633,   1.8368437 ,   7.98879652,   9.29556375,
        10.55574455,   7.24717392,   7.35872882,   4.50198662,
         1.97243346,   0.54930274,   1.71629518,   4.0949232 ,
         4.50641349,  19.45300944,   5.73451891,  10.2200909 ,
         8.84475793,   5.62433494,   3.63816461,   3.2288009 ,
         3.64720491,   4.08050742,   3.55208345,  12.80703452,
         4.51455295,   7.22640241,   4.82518478,   6.0364361 ,
         8.21399889,   4.89790743,   6.37085345,   7.20139071,
         3.66063349,   6.65749537,   4.5201495 ,   3.16880878,
         4.56500213,   4.47976874,   5.91287906,   7.65823897,
         6.75481467,  10.33585975,   7.95868492,   3.44967745,
         3.30272455,   3.79822256,   3.72583825,   5.35268783,
        11.33346169,   7.61218948,  13.23332132,   5.52663873,
         4.71401637,   5.25380598,   6.32221242,   5.21692832,
         9.95021529,  12.12012981,   9.62887235,  12.51966215,
        12.20119879,  28.07778172,  21.69415422,  13.44016311,
         3.42523128,   3.16880878,   5.79132165,  11.8326263 ,
        20.62850507,  10.58826741,  10.25347039,   3.76593706,
         3.58815683,   4.10381596,   3.23987285,   7.32040184,
         4.62625103,   3.16880878,   4.05801502,   8.29763076,
         1.42053684,   3.54385495,   4.9815377 ,   7.32862308,
         5.884002  ,  12.71539344,   4.14640372,   4.17838374,
         4.74896355,   1.84587995,   0.57901706,   1.94727505,
         4.37381493,   5.18582678,   7.70532408,   6.86738548,
         6.04728603,   2.94714791,   2.00238741,   0.88296836])

    potnt = np.array(
        [7.12596329e+23,   1.83684370e+24,   7.98879652e+24,
         9.29556375e+24,   1.05557446e+25,   7.24717392e+24,
         7.35872882e+24,   4.50198662e+24,   1.97243346e+24,
         5.49302741e+23,   1.71629518e+24,   3.11607783e+00,
         4.55006629e+00,   4.21948454e+01,   4.51089464e+00,
         1.77476721e+01,   1.18679201e+01,   5.93094410e+00,
         2.26828834e+00,   3.22880090e+24,   3.64720491e+24,
         3.44492074e+00,   2.99141371e+00,   8.61459830e+01,
         3.22150654e+00,   1.30493764e+01,   4.51470413e+00,
         1.01713137e+01,   1.40167801e+01,   4.89790743e+24,
         6.37085345e+24,   8.30460195e+00,   2.72370114e+00,
         1.97019871e+01,   4.81322624e+00,   2.37203116e+00,
         4.76156755e+00,   3.84190281e+00,   5.53509619e+00,
         7.65823897e+24,   6.75481467e+24,   1.63796499e+01,
         1.83238435e+01,   2.62626616e+00,   3.21546392e+00,
         5.36483147e+00,   3.18817285e+00,   5.90189403e+00,
         1.86765515e+01,   7.61218948e+24,   1.32333213e+25,
         4.00510836e+00,   3.72650975e+00,   5.71530086e+00,
         2.42783091e+01,   1.07981219e+01,   2.92283301e+01,
         3.24892464e+01,   9.86359779e+00,   1.25196622e+25,
         1.22011988e+25,   5.98718495e+01,   1.54766737e+02,
         7.40803538e+01,   3.21059221e+00,   2.38746227e+00,
         7.36767180e+00,   4.52838697e+01,   4.40547155e+01,
         1.05882674e+25,   1.02534704e+25,   3.05098779e+00,
         2.45849055e+00,   3.12955438e+00,   1.87486164e+00,
         2.51124463e+01,   6.21239889e+00,   1.64106832e+00,
         3.28554137e+00,   8.29763076e+24,   1.42053684e+24,
         2.36944471e+00,   5.71708702e+00,   1.36764251e+01,
         4.71435055e+00,   2.24231064e+01,   3.41364652e+00,
         3.49569086e+00,   4.14217801e+00,   1.84587995e+24,
         5.79017064e+23,   1.94727505e+24,   4.37381493e+24,
         5.18582678e+24,   7.70532408e+24,   6.86738548e+24,
         6.04728603e+24,   2.94714791e+24,   2.00238741e+24,
         8.82968356e+23])

    mg = RasterModelGrid((NROWS, NCOLS), (DX, DX))

    mg.add_field('node', 'topographic__elevation', z)

    Qin = np.ones_like(z) * 100. / (60. * 60. * 24. * 365.25)
    # ^remember, flux is /s, so this is a small number!
    mg.add_field('node', 'water__unit_flux_in', Qin)

    pfr = PotentialityFlowRouter(mg, flow_equation='Manning')
    pfr.route_flow()

    assert_allclose(mg.at_node['surface_water__discharge'], flux)
    assert_allclose(mg.at_node['flow__potential'][mg.core_nodes],
                    potnt[mg.core_nodes])
