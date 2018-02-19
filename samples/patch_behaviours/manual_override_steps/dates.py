# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking


class DatesPatch(BaseBehaviour):
    """
    check-in/check-out date changes
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.ManualOverrideSteps

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.DatesDiff

    def execute(self, diff_item, *args, **kwargs):
        super(DatesPatch, self).execute(diff_item, *args, **kwargs)

        updated_booking = diff_item.target_state()
        assert type(updated_booking) is Booking

        return ["Update Checkin Checkout Dates",
            "check-in: {ci}".format(ci=updated_booking.check_in),
            "check-out: {co}".format(co=updated_booking.check_out)
        ]
