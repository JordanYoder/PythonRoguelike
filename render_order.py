# In render_order.py
from enum import auto, Enum


class RenderOrder(Enum):
    CORPSE = auto()  # Value 1
    ITEM = auto()    # Value 2
    ACTOR = auto()   # Value 3 (Enemies)
    PLAYER = auto()  # Value 4 (Highest priority)
