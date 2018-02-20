# -*- coding: utf-8 -*-
from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from b2b.models import Booking
from samples.constants import DiffConsts
from diff import BaseDiffItem


class PaymentsDiff(BaseDiffItem):
    """
    reprensets payments diff in two bookings
    """

    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.CRSOrderBookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.PaymentsDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Booking
        assert CRSBookingOrderInterface in type(rhs).mro()
        bookedroom_payment_map = {
            (bookedroom.room_type,str(bookedroom.guest_count())): bookedroom.total_pre_tax_room_charges() for bookedroom in
        lhs.bookedroom_set.all()}

        if bookedroom_payment_map != rhs.bookedroom_payment_map() \
                or lhs.get_payterm() != rhs.get_payterm() \
                or lhs.get_booking_source() != rhs.get_booking_source():

            return True

        return False

    def patch_priority(self):
        # payments patch to be processed last
        return 100
