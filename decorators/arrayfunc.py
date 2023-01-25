from typing import List


def arrayfunc(f):
    class ArrayFunc:
        __call__ = f

        def applymap(self, args_list: List, except_none=False, **kwargs):
            rs = [self(*args, **kwargs)
                  if isinstance(args, tuple)
                  else self(args, **kwargs)
                  for args in args_list]

            return rs if not except_none else [r for r in rs if r]
    return ArrayFunc()
