from .base import BaseOperator


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
        self.fs = []

    def __call__(self):
        """
        演算実行
         *: 順次実行
        >>: stack(fs)へ追加
         >: 最終評価(計算終了)
        >>> p = PipeOperator(1)
        >>> p * f1 >> f2
        >>> p  *= f1  # r = f1(1), r=2
        >>> p >>= f2  # f2はstack, fs=[f2]
        >>> p  *= f1  # r = f1(2), r=4
        >>> p  *= f3  # r = f3(4), r=16
        >>> p >>= f3  # f3はstack, fs=[f2,f3]
        >>> p   > f2  # f2で最終評価, fs=[f2,f3,f2]
        ... 326       # f2(16) => f3(18) => f2(324) => 326
        """
        rst = self.args
        for f in self.fs:
            rst = self.__execute(f, *rst)

        return rst[0] if len(rst) == 1 else rst

    def __step(self, args, fs):
        s = self.__class__(*args)
        s.fs = fs
        return s

    def __mul__(self, func):
        """パイプライン演算子として、*を定義

        Examples
        --------
        >>> p = PipeOperator(2)
        >>> (p * f1)() # f1(2)
        4
        >>> (p * f1 * f2)() # f2(f1(2))
        6
        >>> (p * f1 * f2 * f3)() # f3(f2(f1(2)))
        36

        >>> p = PipeOperator(1,2)
        >>> (p * f)() # f(1,2)
        (3,2)
        >>> (p * f * f)() # f(f(1,2))
        (5,6)
        """
        return self.__step(
            args=self.__execute(func, *self.args),
            fs=self.fs
        )

    def __gt__(self, func, i=None):
        """
        関数を追加して評価

        Examples
        --------
        >>> p = PipeOperator(2)
        >>> p * f1 * f2 > f3
        36
        """
        return self.__rshift__(func, i=i)()

    def __lt__(self, arg, i=None):
        """
        引数を追加して評価

        Examples
        --------
        >>> p = PipeOperator(1)
        >>> p >>= f
        >>> p < 2
        ... (3,2)
        >>> P < 4
        ... (5,4)
        """
        return self.__lshift__(arg, i=i)()

    def __rshift__(self, func, i=None):
        """
        関数を追加

        Examples
        --------
        >>> p = PipeOperator(2)
        >>> p >>= f1
        >>> p >>= f2
        >>> p >>= f3
        >>> p.args
        2
        >>> p() # f3(f2(f1(2)))
        36
        >>> p = PipeOperator(2)
        >>> p >> f1 >> f2 >> f3 * operate

        """
        if i is None:
            fs = self.fs + [func]
        else:
            fs = self.fs[:i] + [func] + self.fs[i:]

        return self.__step(self.args, fs)

    def __lshift__(self, arg, i=None):
        """
        引数の追加
        >>> p = PipeOperator(1)
        >>> p <<= 2
        >>> p.args
        (1,2)
        >>> p > f
        (3,2)
        >>> p <<= 3
        >>> p.args
        (1,2,3)
        >>> p > f
        (6,6)
        """
        args = list(self.args)

        if i is None:
            args = args + [arg]
        else:
            args = args[:i] + [arg] + args[i:]

        return self.__step(args, self.fs)

    def __execute(self, f, *a):
        return (lambda r: r if isinstance(r, tuple) else [r])(f(*a))
