from typing import TypedDict


class Star(TypedDict):
    """Type definition of stars used in stars.json."""

    id: int
    mag: float
    size: int
    x: float
    y: float
    z: float
    r: int
    g: int
    b: int


class QAArgs(TypedDict):
    """Type definition of quantum annealing arguments."""

    token: str
    lagrange_multiplier: float
    num_reads: int
