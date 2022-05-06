"""
Module for containing the Singleton Metaclass.
"""

class Singleton(type):
    """
    The 'Singleton' Metaclass.
    """

    _instancias = {}

    def __call__(cls, *args, **kwargs):
        """
        Calls this object as if it were a function.
        """

        if cls not in cls._instancias:
            cls._instancias[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instancias[cls]
