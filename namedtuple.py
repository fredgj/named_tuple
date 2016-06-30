
def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
  
        
def __new__(cls, *args, **kwargs):
    obj = tuple.__new__(cls)
    for attr, val in zip(obj._fields, args):
        obj.__dict__[attr] = val
    for key, val in kwargs.iteritems():
        if key in obj.__dict__:
            raise TypeError("__new__ got multiple values for keyword" + 
                            "argument '{arg}'".format(arg=key))
        obj.__dict__[key] = val
    return obj
 
    
def __setattr__(self, name, _):
    raise AttributeError("'{cls}' object has no attribute '{name}'".format(
                    cls=self.__class__.__name__,
                    name=name))

                    
def __repr__(self):
    sorted_pairs = sorted(self.__dict__.iteritems(), key=lambda p: p[0])
    values = ', '.join('{0}={1}'.format(key, val) for key,val in sorted_pairs)
    return '{cls}({values})'.format(cls=self.__class__.__name__, values=values)


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
            '__setattr__': __setattr__,
            '__repr__':__repr__,
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
    
    Cube = named_tuple('Cube', ('x', 'y', 'z'))
    c = Cube(1,2,3)
    print 'c.x =', c.x
    print 'c.y =', c.y
    print 'c.z =', c.z
        




