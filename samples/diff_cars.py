from diff import BaseDiffItem
from diff import Differ
from diff import BaseDiffStrategy
from enum import Enum

CAR_DIFF_STRATEGY = 1


class CarDiff(Enum):
    BrandDiff = 1
    ModelDiff = 2
    MakeDiff = 3
    VariantDiff = 4


class Car:
    def __init__(self, brand, model, make, variant):
        self.brand = brand
        self.model = model
        self.make = make
        self.variant = variant


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
        return CAR_DIFF_STRATEGY


class BrandDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return CAR_DIFF_STRATEGY

    @classmethod
    def diff_type(cls):
        return BrandDiff.__name__

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Car
        assert type(rhs) is Car

        ret_value = lhs.brand != rhs.brand
        print('{} is {}'.format(cls.diff_type(), ('different' if ret_value else 'same')))
        return ret_value


class MakeDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return CAR_DIFF_STRATEGY

    @classmethod
    def diff_type(cls):
        return MakeDiff.__name__

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Car
        assert type(rhs) is Car

        ret_value = lhs.make != rhs.make
        print('{} is {}'.format(cls.diff_type(), ('different' if ret_value else 'same')))
        return ret_value


class ModelDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return CAR_DIFF_STRATEGY

    @classmethod
    def diff_type(cls):
        return ModelDiff.__name__

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Car
        assert type(rhs) is Car

        ret_value = lhs.model != rhs.model
        print('{} is {}'.format(cls.diff_type(), ('different' if ret_value else 'same')))
        return ret_value


class VariantDiff(BaseDiffItem):
    @classmethod
    def diff_strategy(cls):
        return CAR_DIFF_STRATEGY

    @classmethod
    def diff_type(cls):
        return VariantDiff.__name__

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Car
        assert type(rhs) is Car

        ret_value = lhs.variant != rhs.variant
        print('{} is {}'.format(cls.diff_type(), ('different' if ret_value else 'same')))
        return ret_value


def diff_cars(c1, c2):
    """
    diffs two cars
    returns a DiffSet containing DiffItems that tell what's missing in c1
    as compared to c2

    :param c1: old Booking object
    :param c2: new Booking object
    :return: DiffSet (c1-c2)
    """
    strategy = Differ.get_strategy(CAR_DIFF_STRATEGY)
    return strategy.diff(c1, c2)


def main():
    car_1 = Car('Maruti', 'Swift', '2018', 'ZXi')
    car_3 = Car('Maruti', 'Swift', '2018', 'ZXi')
    car_2 = Car('Maruti', 'Swift', '2016', 'ZXi')

    diff_cars(car_1, car_2)
    diff_cars(car_1, car_3)


main()
