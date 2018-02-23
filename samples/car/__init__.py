from diff import Differ
from diff import BaseDiffStrategy
from samples.car.car import BrandDiff
from samples.car.car import ModelDiff
from samples.car.car import MakeDiff
from samples.car.car import VariantDiff
from samples.constants import DiffConsts


@Differ.register_strategy
class CarDiffStrategy(BaseDiffStrategy):
    """
    collects DiffItems for diffing two cars
    """
    def __init__(self):
        super(CarDiffStrategy, self).__init__(diff_items=[
            BrandDiff,
            ModelDiff,
            MakeDiff,
            VariantDiff
        ])

    @classmethod
    def name(cls):
        return DiffConsts.DiffingStrategy.CarDiff
