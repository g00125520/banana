'use numpy'

import numpy as np
import pylab as pl 
from numpy import random as nr

def t_array():
    print(np.arange(0,1,0.1))
    print(np.linspace(0,1,10))
    print(np.linspace(0,1,10, endpoint=False))
    print(np.logspace(0,2,5))
    print(np.logspace(0,1,12, base=2, endpoint=False))

    x = np.arange(5,0,-1)
    # TypeError: unsupported operand type(s) for -: 'list' and 'int'
    #print(x[np.arange([True, False, True, False, False])])
    print(x[[True, False, True, False, False]])

def t_narray():
    a = np.arange(0,60,10).reshape(-1,1) + np.arange(0,6)
    print(a)
    print(a[np.s_[::2,2::]])
    print(a[(0,1,2,3),(1,2,3,4)])
    print(a[[1,2]])
    print(a[[[0,1],[2,3]],[[-1,-2],[-3,-4]]])
    x = np.array([[0,1],[2,3]])
    print(x)
    print(a[x])

def q_sqrt():
    """
    """
    number = np.linspace(0.1, 10, 100)
    y = number.astype(np.float32)
    x2 = y * 0.5
    i = y.view(np.int32)
    i[:] = 0x5f3759df - (i >> 1)
    y = y * (1.5 - x2 * y * y)
    np.max(np.abs(1/np.sqrt(number) - y))


def t_strides():
    from numpy.lib.stride_tricks import as_strided
    a = np.arange(6)
    b = as_strided(a, shape=(4,3), strides=(4,4))
    print(b)

    
def triangle_w(x, c, c0, hc):
    x = x - int(x)
    if x >= c: r = 0.0
    elif x < c0: r = x / c0 * hc 
    else: r = (c-x) / (c-c0) * hc
    return r

def triangle_w2(x, c, c0, hc):
    x = x - x.astype(np.int)
    return np.where(x >= c, 
                    0, 
                    np.where(x < c0, 
                             x / c0 * hc, 
                             (c-x) / (c - c0) * hc))

def triangle_w3(x, c, c0, hc):
    x = x - x.astype(np.int)
    return np.select([x >= c, x < c0, True],
                     [0, x / c0 * hc, (c-x) / (c -c0) * hc])

def triangle_w4(x, c, c0, hc):
    x = x - x.astype(np.int)
    return np.piecewise(x,
                        [x >= c, x < c0], 
                        [0, 
                         lambda x: x / c0 *hc,
                         lambda x: (c-x) / (c-c0) * hc])

def t_triangle():
    x = np.linspace(0, 2, 1000)
    y1 = np.array([triangle_w(t, 0.6, 0.4, 1.0) for t in x])
    print(y1.dtype)
    #triangle_unif = np.fromfunction(triangle_w, 4, 1)
    triangle_unif = np.frompyfunc(triangle_w, 4, 1)
    y2 = triangle_unif(x, 0.6, 0.4, 1.0)
    print(y2.dtype)
    print(y2.astype(np.float).dtype)
    triangle_unif2 = np.vectorize(triangle_w, otypes=[np.float])
    y3 = triangle_unif2(x, 0.6, 0.4, 1.0)
    print(np.all(y1 == y2))
    print(np.all(y2 == y3))

def t_grid():
    #x, y = np.ogrid[:5,:5]
    #a, b = np.mgrid[:5,:5]

    a = np.arange(4)
    print(a[None, :])
    print(a[: , None])

    x = np.array([0, 1, 4, 10])
    y = np.array([2, 3, 8])

    np.ix_(x, y)
    #print(gx, gy, gx + gy)

    print(np.add.reduce([1, 2, 3]))
    #print(np.add.reduce([[1,2,3], [4,5,6]], axis=1))
    print(np.add.outer(np.array([1,2,3]), np.array([4,5,6])))

    print(np.add.accumulate([1, 2, 3]))
    print(np.add.accumulate([[1,2,3], [4,5,6]], axis=1))
    # if(indice[i] < indice[i+1]): op.reduce(indice[i]:indice[i+1])
    # else: a[indice[i]]
    # for indice[len(indice)]: op.reduce(all)
    print(np.arange(4)[0:1])
    print(np.add.reduceat(np.array([1,2,3,4]), indices=[0, 1, 0, 2, 0, 3, 0]))
    print(np.add.reduceat(np.array([1,2,3,4]), indices=[3, 3, 0, 2, 0, 3, 0]))

def t_ndarray():
    a = np.arange(3 * 4 * 5).reshape(3, 4, 5)
    print(a)
    lidx = [[0], [1]]
    aidx = np.array(lidx)

    #print(a[lidx])
    #print(a[aidx])

    i0 = np.array([[1,2,1], [0,1,0]]) #(2,3)
    i1 = np.array([[[0]], [[1]]]) #(2,1,1)
    i2 = np.array([[[2,3,2]]]) # (1,1,3)
    b = a[i0, i1, i2]
    print(b)
    c = a[1:3, i0, i1] #(2,2,2,3)
    print(c)
    i,j,k = 1,1,2
    ind0, ind1 = np.broadcast_arrays(i0, i1)
    print(a[1:3, ind0[i,j,k], ind1[i,j,k]])
    print(c[:, i, j, k])

    d = a[i0, :, i1] #(2,2,3,4)
    print(d)
    print(d[i,j,k,1:3])
    print(a[ind0[i,j,k], : , ind1[i,j,k]])

def t_ndarray_84():
    i,j,k,l = 6,7,8,3
    _, _, v = np.mgrid[:i, :j, :k]
    idx = np.random.randint(0, k-l, size=(i,j))
    idx_k = idx[:, :, None] + np.arange(3)
    idx_i, idx_j, _ = np.ogrid[:i, :j, :k]
    r = v[idx_i, idx_j, idx_k]
    return r

def t_bool():
    b1 = np.array([True, False, True, False, False])
    print(np.nonzero(b1))

    b2 = np.array([[True, False, True, False, False],[True, False, True, False, False]])
    print(np.nonzero(b2))

    a = np.arange(3 * 4 * 5).reshape(3, 4, 5)
    #print(a[b2])
    print(a)
    print(a[np.nonzero(b2)])
    print(a[1:3, np.nonzero(b2)])
    print(a[1:3, np.nonzero(b2)[0], np.nonzero(b2)[1]])

def t_rand():
    from numpy import random as rd
    np.set_printoptions(precision=2)
    r1 = rd.rand(4,3)
    r2 = rd.randn(4,3)
    r3 = rd.randint(0, 10, (4,3))
    r4 = rd.normal(100, 10, (4,3))
    r5 = rd.uniform(10, 20, (4,3))
    r6 = rd.poisson(2.0, (4,3))

    a = np.array([1, 10, 20, 30, 40])
    print(rd.permutation(a))
    print(rd.shuffle(a))

    b = np.arange(10, 25, dtype=float)
    c1 = rd.choice(b, size=(4,3))
    c2 = rd.choice(b, size=(4,3), replace=False)
    c3 = rd.choice(b, size=(4,3), p=b / np.sum(b))
    print(c3)

    w1 = rd.randint(0, 100, 3)
    print(w1)
    
    w2 = rd.randint(0, 100, 3)
    print(w2)

    rd.seed(50)
    w3 = rd.randint(0, 100, 3)
    print(w3)

    rd.seed(50)
    w4 = rd.randint(0, 100, 3)
    print(w4)

    
def t_sum():
    print(np.ones((2,3,4)))

    a = np.sum(np.ones((2, 3, 4)), axis=(0, 1))
    b = np.sum(np.ones((2, 3, 4)), axis=(0, 2))
    print(a)

    a = np.random.randint(0, 10, size=(4,5))
    print(a)
    print(np.mean(a, axis=1))
    pa = a / np.sum(a, 1, dtype=float, keepdims=True)
    print(pa)
    print(pa.sum(1, keepdims=True))

    score = np.array([83, 72, 79])
    number = np.array([20, 15, 30])
    print(np.average(score, weights=number))

def normal_pdf(mean, var, x):
    return 1 / np.sqrt(2 * np.pi * var) * np.exp(-(x - mean) ** 2 / 2 * var)

def t_91():
    nr.seed(42)
    data = nr.normal(0, 2.0, size=10)
    mean, var = np.mean(data), np.var(data)
    var_range = np.linspace(max(var - 4, 0.1), var + 4, 100)

    p = normal_pdf(mean, var_range[:, None], data)
    p = np.product(p, axis=1)
    
    pl.plot(var_range, p)
    pl.axvline(var, 0, 1, c="r")
    pl.show()


def t_var():
    a = nr.normal(0, 2.0, (10000, 10))
    v1 = np.var(a, axis=1, ddof=0)
    v2 = np.var(a, axis=1, ddof=1)
    print(np.mean(v1))
    print(np.mean(v2))
    
def t_max():
    a = np.array([1,3,5,7])
    b = np.array([2,4,6])

    print(np.maximum(a[None, :], b[:, None]))

    np.random.seed(42)
    c = np.random.randint(0, 10, size=(4,5))

    max_pos = np.argmax(c)
    d = c.ravel()
    print(d[max_pos])
    print(np.max(c))

    idx = np.argmax(c, axis=1)
    print(idx)

    print(c[np.arange(c.shape[0]),idx])

    np.sort(c, axis=0)
    
    st1 = np.argsort(c)
    st0 = np.argsort(c, axis=0)
    ax0, ax1 = np.ogrid[:c.shape[0], :c.shape[1]]
    print(c[ax0, st1])
    print(c[st0, ax1])

    d = np.random.randint(0, 10, (5,3))
    print(d[np.lexsort(d[:, ::-1].T)])

    print(np.median(d, axis=1))
    
    x = np.array([3,5,7,1,9,8,6,10])
    y = np.array([2,1,5,10,100,6])

    print(get_index_sort(x,y))

def get_index_sort(x, y):
    index = np.argsort(x)
    s_x = x[index]
    s_index = np.searchsorted(s_x, y)
    yindex = np.take(index, s_index, mode="clip")
    mask = x[yindex] != y
    yindex[mask] = -1
    return yindex

def get_index_dict(x, y):
    idx_map = {v:i for i, v in enumerate(x)}
    yindex = [idx_map.get(v, -1) for v in y]
    return yindex
    
def t_hist():
    a = np.random.rand(100)
    c, d = np.histogram(a, bins=5, range=(0, 1))
    e, f = np.histogram(a, bins=[0, 0.4, 0.8, 1.0])
    return

def t_where():
    x = np.arange(10)
    y = np.where(x<5, 9-x, x)
    return y

def t_ndarr():
    a = np.arange(3)
    b = np.arange(10, 13)
    v = np.vstack((a, b))
    h = np.hstack((a, b))
    c = np.column_stack((a, b))
    d = np.c_[a, b, a+b]
    return 

def t_ployld():
    a = np.array([1.0, 0, -2, 1])
    p = np.poly1d(a)
    print(p(2))
    p1 = p + [-2, 1]
    p2 = p * p
    p3 = p /[1, 1]
    z = p.deriv().integ == p
    r = np.roots(p)
    w = p(r)

    x = np.linspace(- np.pi / 2 , np.pi / 2, 1000)
    y = np.sinc(x)

    for deg in [3,5,7]:
        aa = np.polyfit(x, y ,deg)
        error = np.abs(np.polyval(aa, x) - y)
        print("degree {}: {}".format(deg, aa))
        print("max error of order %d " % deg, np.max(error))
    return
    
def t_poly_111():
    from numpy.polynomial import Polynomial, Chebyshev
    p = Polynomial([1, -2, 0, 1])
    print(p(2.0))
    print(p.deriv())

    def f(x):
        return 1.0 / ( 1 + 25 * x **2)
    
    n = 11
    x1 = np.linspace(-1, 1, n)
    x2 = Chebyshev.basis(n).roots()
    xd = np.linspace(-1, 1, 200)
    c1 = Chebyshev.fit(x1, f(x1), n-1, domain=[-1,1])
    c2 = Chebyshev.fit(x2, f(x2), n-1, domain=[-1,1])

    np.abs(c1(xd) - f(xd)).max()
    np.abs(c2(xd) - f(xd)).max()
    
def t_dot_116():
    a = np.arange(12).reshape(2,3,2)       
    b = np.arange(12,24).reshape(2,2,3)       
    c = np.dot(a,b)

    for i,j in np.ndindex(2,2):
        assert np.alltrue( c[i, :, j, :] == np.dot(a[i], b[j]) )
    
    b = b.reshape(2,3,2)
    d = np.inner(a, b) 
    for i,j,k,l in np.ndindex(2,3,2,3):
        assert d[i,j,k,l] == np.inner(a[i,j], b[k,l])

    e = np.array([1,2,3])
    f = np.array([4,5,6,7])
    print(np.outer(e,f))
    print(np.dot(e[:, None], f[None, :]))

    a1 = nr.randn(3,4)
    b1 = nr.randn(4,5)

    c1 = np.tensordot(a,b, axes=[[1],[0]])
    c2 = np.tensordot(a,b, axes=1)
    c3 = np.dot(a1, b1)
    assert np.allclose(c1, c3)
    assert np.allclose(c2, c3)

    a2 = np.arange(12).reshape(2,3,2)
    b2 = np.arange(12,24).reshape(2,2,3)

    d1 = np.tensordot(a2,b2, axes=[[-1],[-2]])
    d2 = np.dot(a2,b2)
    assert np.alltrue(d1 == d2)

    return

def t_linalg():
    a = nr.randn(10,20, 3,3)
    ainv = np.linalg.inv(a)

    i, j = 3, 4
    assert np.allclose(np.dot(a[i, j], ainv[i, j]), np.eye(3))

    adet = np.linalg.det(a)
    print(adet.shape)

def t_buf():
    from array import array
    a = array("d")
    for i in range(10):
        a.append(i)
        if i == 2 :
            na = np.frombuffer(a, dtype=float)
            print(na.ctypes.data)
        print(a.buffer_info())
    return
    
def t_buf2():
    import struct,math
    buf = bytearray()
    for i in range(5):
        buf += struct.pack("=hdd", i, math.sin(i * 0.1), math.cos(i * 0.1))
    dtype = np.dtype({"names": ["id", "sin", "cos"], "format": ["h", "d", "d"]})

    data = np.frombuffer(buf, dtype=dtype)
    print(data)

def t_buf_123():
    from qtpy.QtGui import QImage
    img = QImage("a.png")
    
if __name__ == "__main__":
    t_buf2()