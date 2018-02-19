# -*- coding: utf-8 -*-
from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.diffing_mechanisms import BaseDiffItem
from b2b.models import Booking


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
