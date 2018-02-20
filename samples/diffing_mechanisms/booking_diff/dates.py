# -*- coding: utf-8 -*-
from b2b.models import Booking
from samples.constants import DiffConsts
from diff import BaseDiffItem


class DatesDiff(BaseDiffItem):
    """
    check-in/check-out date changes
    """
    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.BookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.DatesDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        """
        :param lhs: existing Booking model object
        :param rhs: updated Booking model object
        :return: True if check-in/check-out dates have changed in the updated one
        """
        assert type(lhs) is Booking
        assert type(rhs) is Booking

        if lhs.check_in != rhs.check_in or lhs.check_out != rhs.check_out:
            return True

        return False

    def patch_priority(self):
        # dates to be patched after occupancy and guest details changes, preferably
        return 50
