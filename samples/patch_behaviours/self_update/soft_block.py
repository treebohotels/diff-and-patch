# -*- coding: utf-8 -*-
from datetime import datetime

from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking
from b2b import constants

class SoftBlockPatch(BaseBehaviour):
    """
    check-in/check-out date changes
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.SelfUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.SoftBlockDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        check softblock-expiry and update what doesn't match
        """
        from django.conf import settings
        super(SoftBlockPatch, self).execute(diff_item, *args, **kwargs)

        booking = diff_item.current_state()
        assert type(booking) is Booking

        crs_order = diff_item.target_state()
        assert CRSBookingOrderInterface in type(crs_order).mro()

        if crs_order.is_soft_booking() and booking.get_soft_booking_expiry() != crs_order.soft_booking_expiry():
            booking.set_attribute(key=constants.BookingAttributes.SOFT_BOOKING_EXPIRY,
                                  value=crs_order.soft_booking_expiry())

            booking.save()

            booking.audit_backsync("soft block expiry: {soft_block_expiry}".format(soft_block_expiry=crs_order.soft_booking_expiry()))

        if booking.is_soft_booking() and not crs_order.is_soft_booking():
            booking.set_attribute(constants.BookingAttributes.SOFT_BOOKING_CONFIRMED, datetime.now())
            booking.audit_backsync("confirm soft block: {soft_block_expiry}".format(soft_block_expiry=booking.get_soft_booking_expiry()))
            booking.remove_attribute(constants.BookingAttributes.SOFT_BOOKING_EXPIRY)
            booking.save()





