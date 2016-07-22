import ad
import numpy as np
import smcpp.spline

EPS = 1e-8

def test_spline():
    for klass in (smcpp.spline.CubicSpline, smcpp.spline.AkimaSpline):
        _test_spline(klass)


def _test_spline(klass):
    y = ad.adnumber([1.18, 0.13, -0.01, -0.26, -0.02, 0.41, 0., 0., 0., 0., 0.])
    K = len(y)
    x = np.array([0.0025, 0.00572989, 0.01313264, 0.03009941, 0.06898648,
                  0.15811388, 0.36238983, 0.83058102, 1.90365394, 4.36308829, 10.])
    # y = ad.adnumber(np.random.normal(size=20))
    s = [0.0025, 0.00057604, 0.00070876, 0.00087207, 0.00107301, 0.00132025, 0.00162445, 0.00199875, 0.0024593, 0.00302595,
         0.00372318, 0.00458105, 0.00563659, 0.00693535, 0.00853335, 0.01049956, 0.01291881, 0.0158955, 0.01955805, 0.02406452, 0.02960933,
         0.03643176, 0.04482617, 0.05515478, 0.06786325, 0.08349993, 0.10273954, 0.12641224, 0.15553947, 0.19137805,
         0.23547436, 0.28973111, 0.3564894, 0.43862979, 0.53969653, 0.66405052, 0.8170575, 1.00531954, 1.23695991, 1.52197361, 1.87265866]
    sp = klass(x, y)
    pts = sp.eval(s)
    for i in [4, 5, 6]:
        y2 = np.array(y).astype('float')
        y2[i] += EPS
        sp2 = klass(x, y2)
        pts2 = sp2.eval(s)
        for p1, p2 in zip(pts, pts2):
            g1 = p1.d(y[i])
            g2 = (p2 - p1.x) / EPS
            print(i, g1, g2)