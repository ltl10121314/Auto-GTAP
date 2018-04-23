__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-23"
__altered__ = "2018-4-23"

import os, subprocess


class SplitCommodities(object):
    """Uses MSplitCom to Split a Commodity in a HAR data file"""

    __slots__ = ["har_file_location", "MSplitCom_location"]

    def __init__(self) -> None:
        self.har_file_location =
        self.MSplitCom_location =
