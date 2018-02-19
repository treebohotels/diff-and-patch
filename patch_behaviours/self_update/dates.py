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
        return DiffConsts.PatchBehaviours.SelfUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.DatesDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        check check-in/check-out dates and update what doesn't match
        """
        from django.conf import settings
        super(DatesPatch, self).execute(diff_item, *args, **kwargs)

        booking = diff_item.current_state()
        assert type(booking) is Booking

        crs_order = diff_item.target_state()
        assert CRSBookingOrderInterface in type(crs_order).mro()

        if booking.check_in != crs_order.check_in():
            booking.check_in = crs_order.check_in()
            booking.save()

            booking.audit_backsync("check_in: {ci}".format(ci=datetime.strftime(booking.check_in,
                                                                                settings.BOOKING['date_format'])))

        if booking.check_out != crs_order.check_out():
            booking.check_out = crs_order.check_out()
            booking.save()

            booking.audit_backsync("check_out: {co}".format(co=datetime.strftime(booking.check_out,
                                                                                 settings.BOOKING['date_format'])))
