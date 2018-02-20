# -*- coding: utf-8 -*-
from samples.diffing_mechanisms.crs_order_booking_diff import CRSBookingOrderInterface
from samples.models import Booking
from samples.constants import DiffConsts
from diff import BaseDiffItem


class BookingStatusDiff(BaseDiffItem):
    """
    softblock expiry changes
    """
    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.CRSOrderBookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.BookingStatusDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        """
        :param lhs: existing Booking model object
        :param rhs: CRS order details conforming to CRSBookingOrderInterface
        :return: True if check-in/check-out dates have changed in the CRS order
        """
        assert type(lhs) is Booking
        assert CRSBookingOrderInterface in type(rhs).mro()

        if lhs.status != rhs.booking_status():
            return True

        return False
