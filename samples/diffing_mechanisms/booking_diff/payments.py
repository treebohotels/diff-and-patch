# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.diffing_mechanisms import BaseDiffItem
from b2b.models import Booking


class PaymentsDiff(BaseDiffItem):
    """
    reprensets payment diff in two bookings
    """

    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.BookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.PaymentsDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        """
                :param lhs: existing Booking model object
                :param rhs: updated Booking model object
                :return: True if payment/amount/payment-mode/payterm  have changed in the updated one
                """
        assert type(lhs) is Booking
        assert type(rhs) is Booking
        if lhs.is_soft_booking() and not rhs.is_soft_booking():
            return True

        if lhs.total_payment() != rhs.total_payment() or lhs.payment_type() != rhs.payment_type() \
                or lhs.get_booking_source() != rhs.get_booking_source() \
                or lhs.get_payterm() != rhs.get_payterm():
            return True

        lhs_room_occ_price_map = {
            (bookedroom.room_type, str(bookedroom.adults)): bookedroom.total_pre_tax_room_charges()
            for bookedroom
            in lhs.bookedroom_set.all()}

        rhs_room_occ_price_map = {
            (bookedroom.room_type, str(bookedroom.adults)): bookedroom.total_pre_tax_room_charges()
            for bookedroom
            in rhs.bookedroom_set.all()}

        if lhs_room_occ_price_map != rhs_room_occ_price_map:
            return True

        return False

    def patch_priority(self):
        # payments patch to be processed last
        return 100
