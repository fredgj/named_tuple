from collections import OrderedDict

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
  
        
def __new__(cls, *args, **kwargs):
    o = OrderedDict()
    # place kwargs in the same order as fields, if any kwargs
    for f in cls._fields:
        if f in kwargs:
            o[f] = kwargs[f]
    
    all_args = args + tuple(o.values())
    obj = tuple.__new__(cls, all_args)

    for attr, val in zip(obj._fields, args):
        obj.__dict__[attr] = val

    for key, val in o.iteritems():
        if key in obj.__dict__:
            raise TypeError("__new__ got multiple values for keyword" + 
                            "argument '{arg}'".format(arg=key))
        obj.__dict__[key] = val
    return obj
                    

def __getnewargs__(self):
    return tuple(self.__dict__.values())

                    
def __repr__(self):
    items = self.__dict__.iteritems()
    values = ', '.join('{0}={1}'.format(key, val) for key,val in items)
    return '{cls}({values})'.format(cls=self.__class__.__name__, values=values)

def _asdict(self):
    return self.__dict__

def named_tuple(typename, field_names, rename=False):
    """Factory function for creating named_tuble classes"""
    if isinstance(field_names, str):
        _fields = field_names.split()
    elif is_iterable(field_names):
        _fields = field_names
    else:
        raise TypeError('Argument 2 must support iteration')
        
    # name=name to avoid late binding in closures
    props = {name: property(lambda self, name=name:self.__dict__[name]) 
                               for name in _fields}
    rest = {'_fields': _fields,
            '__new__': __new__,
            '__repr__': __repr__,
            '__getnewargs__': __getnewargs__,
            '__dict__': OrderedDict(),
            '__slots__': (),
            '_asdict': _asdict,
           }
    cls_dict = props.copy()
    cls_dict.update(rest)
    new_cls = type(typename, (tuple,), cls_dict)
    return new_cls


if __name__ == '__main__':
    Point = named_tuple('Point', 'x y')
    p = Point(y=2, x=1)
    print 'p.x =', p.x
    print 'p.y =', p.y
    print p
    print p._asdict()
    print p[0]
    print p[1]
    print
    
    Cube = named_tuple('Cube', ('x', 'y', 'z'))
    c = Cube(1,2,3)
    print 'c.x =', c.x
    print 'c.y =', c.y
    print 'c.z =', c.z
    print c
    print c._asdict()

        




