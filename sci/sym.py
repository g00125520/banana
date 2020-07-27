from sympy import E, I, pi
from sympy.core import symbol
from sympy.physics.vector.frame import ReferenceFrame
from sympy.physics.vector.point import Point

def t_pi():
    print(E ** (I * pi))


def t_phy():
    I = ReferenceFrame('I')
    O = Point('O')
    O.set_vel(I, 0)
    g = symbol('g')

