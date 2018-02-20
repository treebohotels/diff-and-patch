# -*- coding: utf-8 -*-
from b2b.models import Booking
from samples.constants import DiffConsts
from diff import BaseDiffItem


class BookingStatusDiff(BaseDiffItem):
    """
    reprensets soft block expiry diff in two bookings
    """
    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.BookingStatusDiff

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.BookingStatusDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        """
                :param lhs: existing Booking model object
                :param rhs: updated Booking model object
                :return: True if check-in/check-out dates have changed in the updated one
                """
        assert type(lhs) is Booking
        assert type(rhs) is Booking

        return False
