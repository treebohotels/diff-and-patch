from diff import BaseDiffItem
from diff import Differ
from samples.constants import DiffConsts


class Car:
    def __init__(self, brand, model, make, variants):
        self.brand = brand
        self.model = model
        self.make = make
        self.variants = variants


class BrandDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return DiffConsts.DiffingStrategy.CarDiff

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.BrandDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Car
        assert type(rhs) is Car

        return lhs.brand != rhs.brand


class MakeDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return DiffConsts.DiffingStrategy.CarDiff

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.MakeDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Car
        assert type(rhs) is Car

        return lhs.make != rhs.make


class ModelDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return DiffConsts.DiffingStrategy.CarDiff

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.ModelDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Car
        assert type(rhs) is Car

        return lhs.model != rhs.model


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


class CarDiff:
    @classmethod
    def diff_car(cls, c1, c2):
        """
        diffs two cars
        returns a DiffSet containing DiffItems that tell what's missing in c1
        as compared to c2

        :param c1: old Booking object
        :param c2: new Booking object
        :return: DiffSet (c1-c2)
        """
        strategy = Differ.get_strategy(DiffConsts.DiffingStrategy.CarDiff)
        return strategy.diff(c1, c2)
