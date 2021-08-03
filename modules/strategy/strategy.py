from typing import Union, Tuple, Any, Callable, Iterator, Set, Optional, overload, TypeVar, Mapping, Dict, List
import inspect



__all__  = ["Strategy"]

def _unimplemented(self, *input: Any) -> None:
    r"""
    """
    raise NotImplementedError


class Strategy():
    def __init__(self):
        #print(inspect.signature(self.__init__)    )
        # for i in args:
        #     print ("    %s = %s" % (i, values[i]) )   
        # for config in configs:
        # #     setattr(self, )
        pass
    
    eval: Callable[..., Any] = _unimplemented
