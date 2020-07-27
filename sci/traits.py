from traits.api import HasTraits,Color,Delegate,Instance,Int,Str
from tvtk.tools import tvtk_doc

class Parent(HasTraits):
    last_name = Str('zhang')


class Child(HasTraits):
    age = Int
    father = Instance(Parent)
    last_name = Delegate('father')

    def _age_changed(self, old, new):
        print('age change from %s to %s' % (old, new))

def t_traits():
    p = Parent()
    c = Child()
    c.configure_traits()
    print(p.last_name)
    print(c.last_name)


if __name__ == '__main__':
    t_traits()
    