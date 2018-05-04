"""tinypandas.py: 

A pure python DataFrame based on https://github.com/lexual/babypandas

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

from operator import itemgetter

# returns Series, not a list
# mainly useful, so we can do chaining.
# e.g. s.map(foo).map(bar), etc.
def return_series(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return Series(result)
    return wrapper


class Series(list):
    @return_series
    def map(self, fn):
        return map(fn, self)
        return self.__class__(map(fn, self))

    def sum(self):
        return sum(self)

    @return_series
    def __eq__(self, other):
        if isinstance(other, str):
            return [x == other for x in self]
        elif hasattr(other, '__iter__'):
            return [x == y for x, y in zip(self, other)]
        raise NotImplementedError( "Unsupported key %s, type %s" % (other, type(other)))

    @return_series
    def __ne__(self, other):
        return [not x for x in self == other]

    @return_series
    def __lt__(self, other):
        if isinstance(other, str):
            result = [x < other for x in self]
        elif hasattr(other, '__iter__'):
            return [x < y for x, y in zip(self, other)]
            return result
        raise NotImplementedError( "Unsupported key %s, type %s" % (other, type(other)))


    @return_series
    def __gt__(self, other):
        if isinstance(other, 'str'):
            result = [x > other for x in self]
        elif hasattr(other, '__iter__'):
            return [x > y for x, y in zip(self, other)]
            return result
        return [not x for x in self < other]

    @return_series
    def __le__(self, other):
        return [not x for x in self > other]

    @return_series
    def __ge__(self, other):
        return [not x for x in self < other]

    @return_series
    def __add__(self, other):
        if isinstance(other, str):
            return [x + other for x in self]
        elif hasattr(other, '__iter__'):
            return [x + y for x, y in zip(self, other)]
        raise NotImplementedError( "Unsupported key %s, type %s" % (other, type(other)))

    @return_series
    def __mul__(self, other):
        if isinstance(other, str):
            return [x * other for x in self]
        elif hasattr(other, '__iter__'):
            return [x * y for x, y in zip(self, other)]
        raise NotImplementedError( "Unsupported key %s, type %s" % (other, type(other)))
            

    def __rmul__(self, other):
        return self.__mul__(other)

    @return_series
    def __div__(self, other):
        if isinstance(other, str):
            return [x / other for x in self]
        elif hasattr(other, '__iter__'):
            return [x / y for x, y in zip(self, other)]
        raise NotImplementedError( "Unsupported key %s, type %s" % (other, type(other)))

class DataFrame():

    def __init__(self, dict_list=None):
        if dict_list is None:
            self._data = []
            self.columns = []
        else:
            self._data = dict_list
            self.columns = list(dict_list[0].keys())

    def __setitem__(self, key, item):
        if isinstance(key,str):
            self._data = [dict(row, **{key: item}) for row in self._data]
        elif hasattr(item, '__iter__'):
            self._data = [dict(row, **{key: x})
                          for row, x in zip(self._data, item)]
        if key not in self.columns:
            self.columns.append(key)

    def __getitem__(self, key):
        if isinstance(key, str):
            return Series([row[key] for row in self._data])
        elif hasattr(key, '__iter__'):
            if isinstance(key[0], bool):
                result = [x for x, y in zip(self._data, key) if y]
                return self.__class__(result)
            else:
                result = self.copy()
                for col in result:
                    if col not in key:
                        del result[col]
                return result
        else:
            raise NotImplementedError( "Unsupported key %s of type %s" % (key, type(key)))

    def __repr__(self):
        result = ['\t'.join(self.columns)]
        for row in self._data:
            line = '\t'.join(str(row[col]) for col in self.columns)
            result.append(line)
        return '\n'.join(result)

    def copy(self):
        return self.__class__(self._data)

    def __delitem__(self, key):
        getter = itemgetter(*[col for col in self.columns if col != key])
        self._data = [getter(row) for row in self._data]
        self.columns.remove(key)

    def __contains__(self, key):
        return key in self.columns

    def __iter__(self):
        for column in self.columns:
            yield column

    def __len__(self):
        return len(self._data)
