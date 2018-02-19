# -*- coding: utf-8 -*-
from datetime import datetime

from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking


class DatesPatch(BaseBehaviour):
    """
    check-in/check-out date changes
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.AuditTrail

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.DatesDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        audit check-in/check-out date changes
        """
        from django.conf import settings
        super(DatesPatch, self).execute(diff_item, *args, **kwargs)

        parent_booking = diff_item.current_state()
        updated_booking = diff_item.target_state()

        assert type(parent_booking) is Booking
        assert type(updated_booking) is Booking

        if parent_booking.check_in != updated_booking.check_in:
            msg = "updated check-in date from {old_ci} to {new_ci}"
            updated_booking.audit_booking_update(msg.format(old_ci=datetime.strftime(parent_booking.check_in,
                                                                                     settings.BOOKING['date_format']),
                                                            new_ci=datetime.strftime(updated_booking.check_in,
                                                                                     settings.BOOKING['date_format'])))

        if parent_booking.check_out != updated_booking.check_out:
            msg = "updated check-out date from {old_co} to {new_co}"
            updated_booking.audit_booking_update(msg.format(old_co=datetime.strftime(parent_booking.check_out,
                                                                                     settings.BOOKING['date_format']),
                                                            new_co=datetime.strftime(updated_booking.check_out,
                                                                                     settings.BOOKING['date_format'])))
