__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-25"
__altered__ = "2018-4-25"

class MoveFiles(object):
    """Moves files. Typically moves the output of one module to the input of another module"""

    __slots__ = ["source","destination"]

    def __init__(self, source: str, destination:str) -> None:
