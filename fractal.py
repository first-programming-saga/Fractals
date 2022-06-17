import numpy as np
import math
import matplotlib.patches as pt

class AF:
    """
    Affine Transformation
    """
    def __init__(self, r:float, s:float, phi:float, psi:float,
    e:float, f:float):
        self.__m = np.array([
                [r * math.cos(phi), -s * math.sin(psi)],
                [r * math.sin(phi), s * math.cos(psi)]])
        self.__t = np.array([[e], [f]])

    def trans(self, v:tuple[float, float])->tuple[float,float]:
        """
        Translate one point

        parameters
        ----------
        v: original two dimensional coordinate

        return
        ----------
        transformed two dimensional coordinate
        """
        vv = np.array([[v[0]], [v[1]]])
        r = self.__m @ vv + self.__t
        return r[0][0], r[1][0]

    def transList(self,vl:list[tuple[float,float]]):
        """
        Translate list of points

        parameters
        ----------
        list of original two dimensional coordinates

        return
        ----------
        list of transformed two dimensional coordinates
        """
        result = list()
        for v in vl:
            result.append(self.trans(v))
        return result        

class Fractal:
    """
    Fractal class
    """
    def __init__(self,afList:list[AF], xy = [(0, 0), (0, 1), (1, 1), (1, 0)]
):
        self.__afList = afList
        self.__shapes = [xy]

    def iterate(self):
        """
        Iterate one step
        """
        sp = list()
        for xy in self.__shapes:
            for af in self.__afList:
                sp.append(af.transList(xy))
        self.__shapes.clear()
        self.__shapes = list(sp)

    def getShapes(self)->list[pt.Polygon]:
        """
        Returns list of shapes as patch
        """
        sp = list()
        for xy in self.__shapes:
            sp.append(pt.Polygon(xy, fill = True, color = 'b'))
        return sp

    def getMap(self)->list[pt.Polygon]:
        """
        Returns list of shapes for showing the map
        """
        sp = list()
        for af in self.__afList:
            sp.append(pt.Polygon(
                af.transList([(0, 0), (0, 1), (1, 1), (1, 0)]),fill =True, color='c',ec='black'))
            sp.append(pt.Polygon(
                af.transList([(0.1,0.1),(0.2,0.1),(0.1,0.3)]), fill = True, color='r'))
        return sp

    @property
    def shapes(self):
        pass
    @shapes.getter
    def shapes(self):
        return self.__shapes