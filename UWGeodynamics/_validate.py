from scaling import u
import six
try:
    import collections.abc as abc
except ImportError:
    # python 2
    import collections as abc

def validate_gravity(s):
    return u.check('[length]')(s)

def _listify_validator(scalar_validator, allow_stringlist=False):
    def f(s):
        if isinstance(s, six.string_types):
            try:
                return [scalar_validator(v.strip()) for v in s.split(',')
                        if v.strip()]
            except Exception:
                if allow_stringlist:
                    # Sometimes, a list of colors might be a single string
                    # of single-letter colornames. So give that a shot.
                    return [scalar_validator(v.strip()) for v in s if v.strip()]
                else:
                    raise
        # We should allow any generic sequence type, including generators,
        # Numpy ndarrays, and pandas data structures.  However, unordered
        # sequences, such as sets, should be allowed but discouraged unless the
        # user desires pseudorandom behavior.
        elif isinstance(s, abc.Iterable) and not isinstance(s, abc.Mapping):
            # The condition on this list comprehension will preserve the
            # behavior of filtering out any empty strings (behavior was
            # from the original validate_stringlist()), while allowing
            # any non-string/text scalar values such as numbers and arrays.
            return [scalar_validator(v) for v in s
                    if not isinstance(v, six.string_types) or v]
        else:
            msg = "{0!r} must be of type: string or non-dictionary iterable.".format(s)
            raise ValueError(msg)
    f.__doc__ = scalar_validator.__doc__
    return f

def validate_quantity(s):
    # Convert to quantity
    s = u.Quantity(s)
    if s.dimensionless:
        return s.magnitude
    return s

def validate_float(s):
    try:
        return float(s)
    except:
        raise ValueError("Could not convert value to float") 

def validate_solver(s):
    if s in ["mg"]:
        return s
    else:
        raise ValueError("Wrong solver option")

def validate_int(s):
    try:
        return int(s)
    except:
        raise ValueError("Could not convert value to int") 

def validate_path(s):
    return s

def validate_bool(b):
    """Convert b to a boolean or raise"""
    if isinstance(b, six.string_types):
        b = b.lower()
    if b in ('t', 'y', 'yes', 'on', 'true', '1', 1, True):
        return True
    elif b in ('f', 'n', 'no', 'off', 'false', '0', 0, False):
        return False
    else:
        raise ValueError('Could not convert "%s" to boolean' % b)

def validate_string(s):
    return s

def validate_any(s):
    return s

def validate_viscosity(s):
    try:
        s = u.Quantity(s)
    except:
        try:
            from UWGeodynamics import rheologies
            s = s.replace(" ", "_")
            s = s.replace(",", "")
            s = s.replace(".", "")
            
            if s in rheologies._dir:
                return rheologies._dir[s]
        except:
            raise ValueError("Can not find {0} rheology in databases".format(s))

validate_stringlist = _listify_validator(six.text_type)
validate_stringlist.__doc__ = 'return a list'