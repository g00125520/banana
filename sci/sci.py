import scipy.special as S
import scipy.constants as C
import pylab as pl
from scipy import interpolate
from scipy import linalg
import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy import stats
from scipy import sparse



def t_spec():
    print(S.gamma(4))
    print(1 + 1e-20)
    print(np.log(1 + 1e-20))
    #print(S.log1p(1e-20))
    #S.ellip

def make_data(m, n, noise_scale):
    np.random.seed(42)
    x = np.random.standard_normal(m)
    h = np.random.standard_normal(n)

    y = np.convolve(x, h)
    yn = y + np.random.standard_normal(len(y)) * noise_scale * np.max(y)

    return x, yn, h

def solve_h(x, y, n):
    X = as_strided(x, shape=(len(x)-n+1, n), strides=(x.itemsize, x.itemsize))
    Y = y[n-1:len(x)]
    h = linalg.lstsq(X, Y)
    return h[0][::-1]

def t_solve_h():
    x, yn, h = make_data(1000, 100, 0.4)
    H1 = solve_h(x, yn, 120)
    H2 = solve_h(x, yn, 80)

    print(np.mean(np.abs(H1[:100] - h)))
    print(np.mean(np.abs(h[:80] - H2)))
    
    
def t_stats():
    print(stats.norm(loc=1.0, scale=2.0).stats())
    
def t_bus():
    t = 100000
    ac = t / 5
    bc = t / 10
    
    at = np.random.uniform(0, t, ac)
    bt = np.random.uniform(0, t, bc)

    bust = np.concatenate(at, bt)
    bust.sort()
    
    n = 200000
    ptime = np.random.uniform(bust[0], bust[-1], n)
    idx = np.searchsorted(bust, ptime)
    print(np.mean(bust[idx] - ptime) * 60)

    from scipy import integrate
    t = 10.0 / 3
    bus_interval = stats.gamma(1, scale=t)
    n, _ = integrate.quad(lambda x: 0.5 * x * x * bus_interval.pdf(x), 0, 1000)
    d, _ = integrate.quad(lambda x: x * bus_interval.pdf(x), 0, 1000)
    print(n / d * 60)
    
def lorenz():
    from scipy.integrate import odeint
    def f(w, t, p, r, b):
        x, y, z = w.tolist()
        return p*(y-x), x*(r-z)-y, x*y-b*z
    t = np.arange(0, 30, 0.02)
    t1 = odeint(f, (0.0, 1.0, 0.0), t, args=(10.0, 28.0, 3.0))
       
class pid(object):
    def __init__(self, kp, ki, kd, kt):
        self.kp, self.ki, self.kd, self.kt = kp, ki, kd, kt
        self.last_error = None
        self.status = 0.0
        
    def update(self, error):
        p = self.kp * error
        i = self.ki * self.status
        
        if self.last_error is None:
            d = 0.0
        else:
            d = self.kd * (error - self.last_error) / self.dt

        self.status += error * self.kt
        self.last_error = error
        
        return p + i + d

def t_iner():
    import math
    
    x = np.linspace(0, 10, 11)
    y = math.sin(x)
    xnew = np.linspace(0, 10, 101)

def t_spl():
    x = [4.913, 4.913, 4.918, 4.938, 4.955, 4.949, 4.911,
         4.848, 4.864, 4.893, 4.935, 4.981, 5.01, 5.021]
    y = [5.2785, 5.2875, 5.291, 5.289, 5.28, 5.26, 5.245,
         5.245, 5.2615, 5.278, 5.2775, 5.261, 5.245, 5.241]
    
    pl.plot(x, y, "o")

    for s in (0, 1e-4):
        tck, t = interpolate.splprep([x,y], s=s)
        xi, yi = interpolate.splev(np.linspace(t[0], t[-1], 200), tck)
        pl.plot(xi, yi, lw=2, label=u"s=%g" % s)

    pl.legend()
    pl.show()

def t_spare():
    a = sparse.dok_matrix((10,5))
    a[2:5,3] = 1.0, 2.0, 3.0

if __name__ == '__main__':
    t_spl()
    
    