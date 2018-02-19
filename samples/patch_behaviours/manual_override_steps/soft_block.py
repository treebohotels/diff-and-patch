# -*- coding: utf-8 -*-
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
        return DiffConsts.PatchBehaviours.ManualOverrideSteps

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.SoftBlockDiff

    def execute(self, diff_item, *args, **kwargs):
        super(SoftBlockPatch, self).execute(diff_item, *args, **kwargs)

        parent_booking = diff_item.current_state()
        updated_booking = diff_item.target_state()
        assert type(updated_booking) is Booking

        if not updated_booking.is_soft_booking():
            return [
                'Confirm SoftBlock', "soft-booking-expiry: {ci}".format(ci=parent_booking.get_soft_booking_expiry())
            ]
        else:
            return [
                'Update SoftBlock', "soft-booking-expiry: {ci}".format(ci=updated_booking.get_soft_booking_expiry())

            ]
