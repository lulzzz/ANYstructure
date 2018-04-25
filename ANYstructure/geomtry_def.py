# ANY 25.04.2018
# Classes for geometry is defined here.

class AllGeomtry:
    ''' Class that collects all defined geomtry '''

    def __init__(self):
        super(AllGeomtry, self).__init__()
        self._points = dict()
        self._lines = dict()

    @property
    def points(self):
        return self._points

    @property
    def lines(self):
        return self._lines


class Point:
    ''' Point class
        Based on coordinates '''

    def __init__(self, *args, **kwargs):
        super(Point, self).__init__()
        self._x = kwargs['x']
        self._y = kwargs['y']


class Line:
    ''' Line class
        Based on point names. '''

    def __init__(self, *args, **kwargs):
        super(Line, self).__init__()
        self._pt_firt = kwargs['first']
        self._pt_second = kwargs['second']


if __name__ == '__main__':

    my_class = AllGeomtry()
