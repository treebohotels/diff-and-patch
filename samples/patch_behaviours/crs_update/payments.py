# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
import logging
from b2b.models import Booking
from b2b.consumer.crs.crs_order import get_b2b_order
from b2b.constants import BookingAttributes


class PaymentsPatch(BaseBehaviour):
    """
    patch any changes to payments
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.CRSUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.PaymentsDiff

    def execute(self, diff_item, *args, **kwargs):
        super(PaymentsPatch, self).execute(diff_item, *args, **kwargs)

        logger = logging.getLogger(self.__class__.__name__)

        try:
            parent_booking = kwargs['old_booking']
            updated_booking = kwargs['new_booking']
            crs_txn_mgr = kwargs['crs_txn_mgr']

        except KeyError as e:
            msg = "{cls} needs to know {m}, but it's missing in the args".format(cls=self.__class__.__name__,
                                                                                 m=e.message)
            logger.error(msg)

            raise RuntimeError(msg)

        # ensure both of them are Booking model objects
        assert type(parent_booking) is Booking
        assert type(updated_booking) is Booking

        # convert the updated booking object into the unified booking interface object
        b2b_order = get_b2b_order(updated_booking)

        # finally, hand over the order to the transaction manager for further processing
        logger.info("Updating payemts as per {o}".format(o=repr(b2b_order)))

        bookedroom_map = {(bookedroom.room_type, bookedroom.guest_count()): bookedroom.total_pre_tax_room_charges() for
                          bookedroom in
                          updated_booking.bookedroom_set.all()}

        with crs_txn_mgr:
            crs_txn_mgr.update_pre_tax(b2b_order, bookedroom_map)
            if parent_booking.total_payment() != updated_booking.total_payment() or (
                            parent_booking.is_soft_booking() and not updated_booking.is_soft_booking() and updated_booking.is_btc_booking()):
                crs_txn_mgr.update_payment(b2b_order)
            if parent_booking.get_booking_source() != updated_booking.get_booking_source():
                crs_txn_mgr.get_hotel_data()
                crs_txn_mgr.update_source(b2b_order)

        if parent_booking.payment_type() != updated_booking.payment_type() or (
                        parent_booking.is_soft_booking() and not updated_booking.is_soft_booking() and updated_booking.is_btc_booking()):
            crs_txn_mgr.update_payterm(b2b_order)
            if not updated_booking.is_payment_processed():
                updated_booking.set_attribute(BookingAttributes.PAYMENT_PROCESSED, True)


