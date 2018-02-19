# -*- coding: utf-8 -*-
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
        return DiffConsts.PatchBehaviours.ManualOverrideSteps

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.BookingStatusDiff

    def execute(self, diff_item, *args, **kwargs):
        super(BookingStatusPatch, self).execute(diff_item, *args, **kwargs)

        updated_booking = diff_item.target_state()
        assert type(updated_booking) is Booking

        return [
            'Update BookingStatus',"booking-status: {bs}".format(ci=updated_booking.status)

        ]
