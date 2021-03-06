"""
Grid class
"""

import numpy as np

class Grid:
    """
    Implementation of 2D grid of cells
    Includes boundary handling
    """


    def __init__(self, grid_height, grid_width):
        """
        Initializes grid to be empty, take height and width of grid as parameters
        Indexed by rows (left to right), then by columns (top to bottom)
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._cells = np.zeros((self._grid_height,self._grid_width))
        self.empty, self.full, self.barrier, self.corner = 0, 1, -1, -2

    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        ans = ""
        for row in range(self._grid_height):
            ans += str(self._cells[row])
            ans += "\n"
        return ans

    def make_empty_grid(self):
        '''
        Making a grid of all 0.
        :return:
        '''
        return np.zeros((self._grid_height,self._grid_width))

    def get_grid_height(self):
        """
        Return the height of the grid for use in the GUI
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Return the width of the grid for use in the GUI
        """
        return self._grid_width

    def get_matrix(self):
        """
        Return the complete matrix in numpy list form.
        """
        return self._cells

    def get_highest_number_in_grid(self):
        '''
        Retruns the highes number in the grid.
        :return:
        '''

        return np.amax(self._cells)

    def clear(self):
        """
        Clears grid to be empty
        """
        self._cells = np.zeros((self._grid_height,self._grid_width))

    def set_empty(self, row, col):
        """
        Set cell with index (row, col) to be empty
        """
        self._cells[row][col] = self.empty

    def set_full(self, row, col):
        """
        Set cell with index (row, col) to be full
        """
        self._cells[row][col] = self.full

    def set_value(self, row, col, value):
        """
        Set cell with index (row, col) to be a specified integer
        """
        self._cells[row][col] = value

    def set_barrier(self, row, col):
        """
        Set cell with index (row, col) to be full
        """
        self._cells[row][col] = self.barrier

    def is_empty(self, row, col):
        """
        Checks whether cell with index (row, col) is empty
        """
        return self._cells[row][col] == self.empty

    def is_full(self, row, col):
        """
        Checks whether cell with index (row, col) is empty
        """
        return self._cells[row][col] == self.full

    def is_barrier(self, row, col):
        """
        Checks whether cell with index (row, col) is empty
        """
        return self._cells[row][col] == self.barrier

    def is_corner(self,point):
        '''
        Identifying corners.
        :param point:
        :return:
        '''
        return [self.get_value(item[0],item[1]) for item in
                self.eight_neighbors(point[0],point[1])].count(self.barrier) > 4

    def four_neighbors(self, row, col):
        """
        Returns horiz/vert neighbors of cell (row, col)
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        return ans

    def eight_neighbors(self, row, col):
        """
        Returns horiz/vert neighbors of cell (row, col) as well as
        diagonal neighbors
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        if (row > 0) and (col > 0):
            ans.append((row - 1, col - 1))
        if (row > 0) and (col < self._grid_width - 1):
            ans.append((row - 1, col + 1))
        if (row < self._grid_height - 1) and (col > 0):
            ans.append((row + 1, col - 1))
        if (row < self._grid_height - 1) and (col < self._grid_width - 1):
            ans.append((row + 1, col + 1))
        return ans

    def get_index(self, point, cell_size):
        """
        Takes point in screen coordinates and returns index of
        containing cell
        """
        return (point[1] / cell_size, point[0] / cell_size)

    def get_value(self, row, col):
        #print('ROW COL: ', row, col)
        #print('CURRENT CELL LEN: ',len(self._cells))
        #print(self._cells[row])
        return self._cells[row][col]

    def get_points_along_line(self,start, end):
        """Bresenham's Line Algorithm
        Produces a list of tuples from start and end
            points1 = get_line((0, 0), (3, 4))
            points2 = get_line((3, 4), (0, 0))
            assert(set(points1) == set(points2))
            print points1
            [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
            [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
        """
        # Setup initial conditions
        x1 = int(start[0])
        y1 = int(start[1])
        x2 = int(end[0])
        y2 = int(end[1])

        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points

    def get_mid_point(self, cell1, cell2):
        '''
        Get the point that is in the middle between two points.
        :param point1:
        :param point2:
        :return:
        '''
        idx = int(round(len(self.get_points_along_line(cell1,cell2))/2,0))
        return self.get_points_along_line(cell1,cell2)[idx]

    def get_adjacent_values(self,cell):
        '''
        Find the labels in the grid adjacent to the specified point.
        :param point:
        :return:
        '''

        return tuple(set([int(self.get_value(neighbor[0], neighbor[1]))
                          for neighbor in self.four_neighbors(cell[0], cell[1])]))

    def get_adjacent_values_duplicates(self,cell):
        '''
        Find the labels in the grid adjacent to the specified point.
        :param point:
        :return:
        '''

        return_tuple = tuple(list([int(self.get_value(neighbor[0], neighbor[1]))
                                   for neighbor in self.four_neighbors(cell[0], cell[1])]))

        len(tuple(set(return_tuple)))

        if len(tuple(set(return_tuple))) > 1:
            return set(return_tuple)
        else:
            return (tuple(set(return_tuple))[0],tuple(set(return_tuple))[0])

    def get_highest_cell(self, value):
        '''
        Get the cell closes to (0,0) with a given value.
        :param value:
        :return:
        '''
        # TODO this is not very numpy-like
        highest = (self.get_grid_height(),0)
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if self.get_value(row,col) == value and row < highest[0]:
                    highest = (row,col)
        return highest

    def get_lowest_cell(self,value):
        '''
        Get the cell closest to (height,0) with a given value.
        :param value:
        :return:
        '''
        # TODO this is not very numpy-like
        lowest = (0,0)

        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if self.get_value(row,col) == value and row > lowest[0]:
                    lowest = (row,col)
        return lowest

    def get_number_of_cells_with_value(self,value):
        '''
        Get the number of cells with a certain value.
        :param value:
        :return:
        '''
        # TODO this is not very numpy-like
        counter = 0
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if self.get_value(row,col) == value:
                    counter += 1
        return counter

    def import_grid(self,grid):
        '''
        Import a grid to replace created grid. Converting to numpy array.
        :param grid:
        :return:
        '''
        self._cells = np.asarray(grid)

    def export_grid(self):
        '''
        Converting from array to list of list. Exporting the grid.
        :return:
        '''
        return self._cells.tolist()
