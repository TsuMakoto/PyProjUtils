from .base import BaseOperator
from .func import Func


class PipeOperator(BaseOperator):
    """パイプライン演算を実行する
    以下を定義
    >>> import math
    >>> f1 = (lambda x: x*2)
    >>> f2 = (lambda x: x+2)
    >>> f3 = (lambda x: x**2)
    >>> def f(*X):
    ...   return sum(X), math.prod(X)
    ...
    """

    def __init__(self, *args):
        self.args = args
        self.f = Func(lambda *a: a)  # 恒等関数

    def __call__(self):
        """
        演算実行
        >>: 順次実行
         >: 最終評価(計算終了)
        >>> p = PipeOperator(1)
        >>> p = p >> f1 >> f2 >> f3
        >>> p()
        ... 16
        """
        return self.f(*self.args)

    def __step(self, args, g: Func):
        s = self.__class__(*args)
        s.f = Func(g) * self.f
        return s

    def __rshift__(self, func):
        """パイプライン演算子として、*を定義

        Examples
        --------
        >>> p = PipeOperator(2)
        >>> (p >> f1)() # f1(2)
        4
        >>> (p >> f1 >> f2)() # f2(f1(2))
        6
        >>> (p >> f1 >> f2 >> f3)() # f3(f2(f1(2)))
        36

        >>> p = PipeOperator(1,2)
        >>> (p >> f)() # f(1,2)
        (3,2)
        >>> (p >> f >> f)() # f(f(1,2))
        (5,6)
        """
        return self.__step(self.args, func)

    def __gt__(self, func):
        """
        関数を追加して評価

        Examples
        --------
        >>> p = PipeOperator(2)
        >>> p >> f1 >> f2 > f3
        36
        """
        return (self >> func)()
