from diff import Differ
from samples.constants import DiffConsts


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
