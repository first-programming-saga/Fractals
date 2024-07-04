import numpy as np
import numpy.typing as npt
import math
import matplotlib.patches as pt
from typing import NamedTuple

class Point(NamedTuple):
    x:float
    y:float

class AF:
    """
    Affine Transformation
    """
    def __init__(self, r:float, s:float, phi:float, psi:float,
    e:float, f:float):
        self.__m: npt.NDArray = np.array([
                [r * math.cos(phi), -s * math.sin(psi)],
                [r * math.sin(phi), s * math.cos(psi)]])
        self.__t: npt.NDArray = np.array([[e], [f]])

    def translate(self, v:Point)->Point:
        """
        Translate one point

        parameters
        ----------
        v: original two dimensional coordinate

        return
        ----------
        transformed two dimensional coordinate
        """
        vv: npt.NDArray = np.array([[v.x], [v.y]])
        r = self.__m @ vv + self.__t
        return Point(r[0][0], r[1][0])

    def translate_list(self, v_list:list[Point]) -> list[Point]:
        """
        Translate list of points

        parameters
        ----------
        list of original two dimensional coordinates

        return
        ----------
        list of transformed two dimensional coordinates
        """
        result:list[Point] = list()
        for v in v_list:
            result.append(self.translate(v))
        return result        

class Fractal:
    """
    Fractal class
    """
    default_xy: list[Point] =  [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
    def __init__(self,afList:list[AF], xy = default_xy):
        self.__afList: list[AF] = afList
        self.__shapes:list[list[Point]] = [xy]

    def iterate(self):
        """
        Iterate one step
        """
        sp = list()
        for xy in self.__shapes:
            for af in self.__afList:
                sp.append(af.translate_list(xy))
        self.__shapes.clear()
        self.__shapes = list(sp)

    def getShapes(self) -> list[pt.Polygon]:
        """
        Returns list of shapes as patch
        """
        sp = list()
        for xy in self.__shapes:
            sp.append(pt.Polygon(Fractal._p2a(xy), fill = True, color = 'b'))
        return sp

    @staticmethod
    def _p2a(data:list[Point]) -> list[list[float]]:
        result:list[list[float]] = list()
        for p in data:
            result.append([p.x, p.y])
        return result

    def getMap(self) -> list[pt.Polygon]:
        """
        Returns list of shapes for showing the map
        """
        sp = list()
        for af in self.__afList:
            sp.append(pt.Polygon(
                Fractal._p2a(af.translate_list(Fractal.default_xy)),
                fill =True, color='c', ec='black'))
            sp.append(pt.Polygon(
                Fractal._p2a(af.translate_list([Point(0.1,0.1), Point(0.2,0.1), Point(0.1,0.3)])), 
                fill = True, color='r'))
        return sp

    @property
    def shapes(self) -> list[list[Point]]:
        return self.__shapes