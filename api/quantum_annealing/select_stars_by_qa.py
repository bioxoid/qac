import sys

try:
    from dwave.system import DWaveSampler, EmbeddingComposite
    import dimod
except ImportError as e:
    print(e)
    sys.exit(1)

from typing import List
import numpy as np
from type_definitions import Star, QAArgs


def select_stars_by_qa(
    stars: List[Star],
    n_opaque: int,
    n_pixel: int = 10,
    n_mag: int = 1,
    qa_args: QAArgs = None,
) -> List[Star]:
    """Select stars covered by an image using QA.
    Args:
        stars(List[Star]):
            candidate stars. The elements must have the same keys as entries in stars.json.
        n_opaque(int):
            how many pixels are opaque in the image.
        n_pixel(int):
            how many pixels have one star.
        n_mag(int):
            regulates brilliance of selected stars.
        qa_args(QAArgs):
            arguments of quantum annealing.
    Returns:
        List[Star]: stars that compose the zodiac sign, seleceted by QA.
    """
    assert n_pixel > 0

    number_of_stars = len(stars)
    L = np.array([[star["x"], star["y"], star["z"]] for star in stars])
    M = np.array([star["mag"] for star in stars])

    cqm = dimod.ConstrainedQuadraticModel()

    # CQM variables
    x = [dimod.Binary(f"x_{i}") for i in range(number_of_stars)]

    # cost function
    distances = np.sqrt(np.sum((L[:, np.newaxis] - L) ** 2, axis=2)) + np.diag(
        [1e-10 for _ in range(number_of_stars)]
    )
    Q = (-1.0) * distances ** (-0.5) * (
        1 - np.diag([1 for _ in range(number_of_stars)])
    ) + 0.0  # the last `+ 0.` is to eliminate -0.0
    cqm.set_objective(
        sum(
            sum(Q[i][j] * x[i] * x[j] for j in range(number_of_stars))
            for i in range(number_of_stars)
        )
    )

    # constraint-1. the number of stars
    cqm.add_constraint(n_pixel * sum(x) - n_opaque >= 0, label="constraint-1")

    # constraint-2. brilliance of stars
    cqm.add_constraint(
        sum((M[i] ** 2 - n_mag) * x[i] for i in range(number_of_stars)) <= 0,
        label="constraint-2",
    )

    # solve
    if qa_args is not None:
        lagrange_multiplier = qa_args["lagrange_multiplier"]
        token = qa_args["token"]
        num_reads = qa_args["num_reads"]
    bqm, _ = dimod.cqm_to_bqm(cqm, lagrange_multiplier=lagrange_multiplier)
    dw_sampler = DWaveSampler(token=token)
    sampler = EmbeddingComposite(dw_sampler)
    sampleset = sampler.sample(bqm, num_reads=num_reads)
    result = sampleset.first.sample

    # select stars according to the result
    selected_stars = [stars[i] for i in range(number_of_stars) if result[f"x_{i}"] == 1]
    return selected_stars


if __name__ == "__main__":
    import json

    with open("stars.json", "r", encoding="utf-8") as file:
        star_list = json.load(file)
    example_stars = star_list[:10]
    print(
        select_stars_by_qa(
            example_stars,
            n_opaque=510,
            n_pixel=100,
            qa_args=QAArgs(
                lagrange_multiplier=10,
                token="T6nD-003e8847b163bdf7bb0adf388dc62fb50e697cb0",
                num_reads=1000,
            ),
        )
    )
