# -*- coding: utf-8 -*-
from b2b.models import Booking
from samples.constants import DiffConsts
from diff import BaseDiffItem


class SoftBlockDiff(BaseDiffItem):
    """
    reprensets soft block expiry diff in two bookings
    """
    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.BookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.SoftBlockDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        """
                :param lhs: existing Booking model object
                :param rhs: updated Booking model object
                :return: True if check-in/check-out dates have changed in the updated one
                """
        assert type(lhs) is Booking
        assert type(rhs) is Booking

        if lhs.is_soft_booking() and not rhs.is_soft_booking():
            return True

        if not lhs.is_soft_booking() or not rhs.is_soft_booking():
            return False

        if lhs.get_soft_booking_expiry() != rhs.get_soft_booking_expiry():
            return True

        return False
