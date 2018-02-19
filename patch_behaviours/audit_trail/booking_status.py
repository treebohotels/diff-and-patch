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
        return DiffConsts.PatchBehaviours.AuditTrail

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.BookingStatusDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        audit check-in/check-out date changes
        """
        from django.conf import settings
        super(BookingStatusPatch, self).execute(diff_item, *args, **kwargs)

        parent_booking = diff_item.current_state()
        updated_booking = diff_item.target_state()

        assert type(parent_booking) is Booking
        assert type(updated_booking) is Booking

        if parent_booking.get_soft_booking_expiry() != updated_booking.get_soft_booking_expiry():
            msg = "updated status from {old_status} to {new_status}"
            updated_booking.audit_booking_update(msg.format(old_status=parent_booking.status,

                                                            new_status=updated_booking.status))


