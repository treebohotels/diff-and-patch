from diff import BaseDiffItem
from samples.constants import DiffConsts
from samples.car.car import Car


class VariantDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return DiffConsts.DiffingStrategy.CarDiff

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.VariantDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Car
        assert type(rhs) is Car

        return lhs.variant != rhs.variant