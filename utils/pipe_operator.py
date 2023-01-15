class PipeOperator:
    def __init__(self, *args):
        self.args = args

    def __mul__(self, func):
        """パイプライン演算子として、*を定義

        Examples
        --------
        >>> p = PipeOperator(2)
        >>> p *= lambda x: x*2
        >>> p.eval()
        4
        >>> p *= lambda x: x+2
        >>> p.eval()
        6
        >>> p *= (lambda x: x**2)
        >>> p.eval()
        36

        >>> def f(x,y):
        ...   return x+y,x*y
        ...
        >>> p = PipeOperator(1,2)
        >>> p *= f
        >>> p.eval()
        (3,2)
        >>> p *= f
        >>> p.eval()
        (5,6)
        """
        return self.__class__(*self.__execute(func))

    def __rshift__(self, func):
        """
        最終評価
        >>> PipeOperator(2) * \
        ...   (lambda x: x*2) * \
        ...   (lambda x: x+2) >> \
        ...   (lambda x: x**2)
        36
        """
        return (self * func).eval()

    def eval(self):
        if len(self.args) == 1:
            return self.args[0]
        return self.args

    def __execute(self, func):
        e = func(*self.args)

        return e if isinstance(e, tuple) else [e]
