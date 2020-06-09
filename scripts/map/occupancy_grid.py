# encode: utf-8

from __future__ import division, print_function

import os
import math
import numpy as np

import yaml
import cv2
from PIL import Image as PilImage

class OccupancyGrid(object):
    """ Stores an occupancy grid map, which indicates the probability of occupancy.
        Attributes:
            map: the occupancy grid map to localize against (nav_msgs/OccupancyGrid)
    """
    def __init__(self, mapfilename):
        
        if isinstance(mapfilename, str):
            self._dir = os.path.dirname(os.path.abspath(mapfilename))
            mapfile = open(mapfilename, 'r')
            mapdata = yaml.load(mapfile)
            mapfile.close()
        else: raise TypeError("map must be a YAML filename")

        fname = mapdata['image']
        self._resolution = mapdata['resolution']
        self._origin = mapdata['origin']
        self._occupied_thresh = mapdata['occupied_thresh']
        self._free_thresh = mapdata['free_thresh']

        # Open image file relatively to the YAML file if path is relative 
        fname = fname if os.path.isabs(fname) else os.path.join(self._dir, (fname))
        self._mapimage = fname
        map = PilImage.open(fname, 'r')
        map = np.asarray(map).astype(np.uint8)
        
        # Convert to grayscale if it is the case
        map = map if len(map.shape) == 2 else np.mean(map, axis=2)
        map = map if mapdata['negate'] > 0 else 255 - map

        self.map = map   # save this for later
    

    def can_move(self, x0, y0, x1, y1) :
        """
            Check if a robot can move from (x0, y0) to (x1, y1)
            in a straight line
        """
        pos_ini = self.convert_to_grid((x0, y0))
        pos_fin = self.convert_to_grid((x1, y1))
        dx = pos_fin[0] - pos_ini[0]
        dy = pos_fin[1] - pos_ini[1]
        if abs(dx) >= abs(dy):
            m = dy/dx
            y = int(pos_ini[1])
            err = pos_ini[1] - y
            for x in range(int(pos_ini[0]), int(pos_fin[0])+1, int(math.copysign(1, dx))):
                if self.map[y, x] >= 255*self._occupied_thresh:
                    return False
                err += abs(m)
                if err > .5:
                    y += int(math.copysign(1, dy))
                    err -= 1.
        else:
            m = dx/dy
            x = int(pos_ini[0])
            err = pos_ini[0] - x
            for y in range(int(pos_ini[1]), int(pos_fin[1])+1, int(math.copysign(1, dy))):
                if self.map[y, x] >= 255*self._occupied_thresh:
                    return False
                err += abs(m)
                if err > 0.5:
                    x += int(math.copysign(1, dx))
                    err -= 1.
        return True

    
    def contains(self, x, y):
        """
            Check if position (x, y) belongs to the map
        """
        colrow = self.convert_to_grid((x, y))
        return colrow[0] >= 0 and colrow[0] < self.map.shape[1] and\
            colrow[1] >= 0 and colrow[1] < self.map.shape[0]
    
    def convert_to_grid(self, xy_theta):
        """
            Convert a xy_theta to grid coordinates
        """
        theta = xy_theta[2] if len(xy_theta) > 2 else .0
        x_grid = (xy_theta[0] - self._origin[0])/self._resolution
        y_grid = (xy_theta[1] - self._origin[1])/self._resolution
        return np.array([x_grid, y_grid, theta])[:len(xy_theta)]

    @property
    def origin_x(self):
        return self._origin[0]

    @property
    def origin_y(self):
        return self._origin[1]

    @property
    def width(self):
        return self.map.shape[1] * self._resolution

    @property
    def height(self):
        return self.map.shape[0] * self._resolution

    @property
    def grid(self):
        return self.map

    @property
    def color_image(self):
        ''' Flip image vertically '''
        return cv2.cvtColor(255 - self.map, cv2.COLOR_GRAY2RGB)[::-1,:,:]

if __name__ == '__main__':
    import cv2

    print (os.path.abspath(os.path.curdir))

    mapdir = os.path.dirname(os.path.abspath(__file__))
    mapfile = os.path.normpath(os.path.normpath(mapdir+'/../../maps/map.yaml'))
    occupancy_grid = OccupancyGrid(mapfile)
    occ_map = occupancy_grid.map
    cv2.imshow('Occupancy Grid', occ_map)
    cv2.waitKey(0)
