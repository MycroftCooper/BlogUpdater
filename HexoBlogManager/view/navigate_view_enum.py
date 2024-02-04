from enum import Enum, Flag, auto


class SortBy(Enum):
    NONE = 0
    Title = 1
    Size = 2
    CreationTime = 3
    LastUpdateTime = 4


class GroupBy(Enum):
    NONE = 0
    Category = 1
    Tag = 2
    CreationTime = 3
    LastUpdateTime = 4


class InfoShowRule(Flag):
    NONE = 0
    Categories = auto()
    Tags = auto()
    Size = auto()
    CreationTime = auto()
    LastUpdateTime = auto()
    All = Categories | Tags | Size | CreationTime | LastUpdateTime
