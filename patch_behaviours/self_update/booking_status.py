# -*- coding: utf-8 -*-
from datetime import datetime

from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking
from b2b import constants

class BookingStatusPatch(BaseBehaviour):
    """
    check-in/check-out date changes
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.SelfUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.BookingStatusDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        check softblock-expiry and update what doesn't match
        """
        from django.conf import settings
        super(BookingStatusPatch, self).execute(diff_item, *args, **kwargs)

        booking = diff_item.current_state()
        assert type(booking) is Booking

        crs_order = diff_item.target_state()
        assert CRSBookingOrderInterface in type(crs_order).mro()
        booking.set_status(crs_order.booking_status())
        booking.audit_backsync("booking status: {booking_status}".format(booking_status=crs_order.booking_status()))


