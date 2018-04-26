# ANY 25.04.2018
# Classes for geometry is defined here.
import ANYstructure.example_data as ex

class AllGeo:
    ''' Class that collects all defined geomtry '''

    def __init__(self):
        super(AllGeo, self).__init__()
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

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

class Line:
    ''' Line class
        Based on point names. '''

    def __init__(self, *args, **kwargs):
        super(Line, self).__init__()
        self._line_pt_a = kwargs['line_pt_a']
        self._line_pt_b = kwargs['line_pt_b']

    @property
    def line_pt_a(self):
        return self._line_pt_a

    @property
    def line_pt_b(self):
        return self.line_pt_b

if __name__ == '__main__':

    my_class = AllGeo()
