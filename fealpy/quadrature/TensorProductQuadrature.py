
import numpy as np
from .Quadrature import Quadrature

class TensorProductQuadrature(Quadrature):
    def __init__(self, qfs, TD=None):
        """

        Notes
        -----

        qfs 是一组积分公式
        """

        if TD is None:
            TD = len(qfs) # 积分公式的个数
            self.quadpts = () # 空元组
            weights = ()
            for i, qf in enumerate(qfs):
                bcs, ws = qf.get_quadrature_points_and_weights()
                self.quadpts += (bcs, )
                weights += (ws, )
        else: # TD 是一个整数, qfs 是一个积分公式
            bcs, ws = qfs.get_quadrature_points_and_weights()
            self.quadpts = TD*(bcs, ) 
            weights = TD*(ws, )

        # 构造 einsum 运算字符串
        s0 = 'abcdef'
        s = ''
        for i in range(TD):
            s = s + s0[i]
            if i < TD-1:
                s = s + ', '
        s = s + '->' + s0[:TD]
        self.weights = np.einsum(s, *weights).reshape(-1)

    def number_of_quadrature_points(self):
        n = self.weights.shape[0]
        return n 
