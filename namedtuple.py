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
    
    args_len = len(all_args)
    fields_len = len(cls._fields)
    if args_len != fields_len:
        msg = '__new__() takes exactly {0} aguments ({1} given)'
        msg = msg.format(args_len, fields_len)
        raise TypeError(msg)
    
    obj = tuple.__new__(cls, all_args)

    for attr, val in zip(obj._fields, args):
        obj.__dict__[attr] = val

    for key, val in o.iteritems():
        if key in obj.__dict__:
            msg = "__new__ got multiple values for keyword argument '{arg}'"
            msg = msg.format(arg=key)
            raise TypeError(msg)
        obj.__dict__[key] = val
    return obj
                    

def __getnewargs__(self):
    return tuple(self.__dict__.values())

                    
def __repr__(self):
    items = self.__dict__.iteritems()
    values = ', '.join('{0}={1}'.format(key, val) for key,val in items)
    cls = self.__class__.__name__
    return '{cls}({values})'.format(cls=cls, values=values)


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
    cls_dict = {name: property(lambda self, name=name:self.__dict__[name]) 
                               for name in _fields}
    rest = {'__dict__': OrderedDict(),
            '__getnewargs__': __getnewargs__,
            '__new__': __new__,
            '__repr__': __repr__,
            '__slots__': (),
            '_asdict': _asdict,
            '_fields': _fields,
           }
           
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

