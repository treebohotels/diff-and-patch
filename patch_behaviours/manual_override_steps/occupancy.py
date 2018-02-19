# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking


class OccupancyPatch(BaseBehaviour):
    """
    patch any changes to occupancy details
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.ManualOverrideSteps

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.OccupancyDiff

    def execute(self, diff_item, *args, **kwargs):
        super(OccupancyPatch, self).execute(diff_item, *args, **kwargs)

        super(OccupancyPatch, self).execute(diff_item, *args, **kwargs)

        updated_booking = diff_item.target_state()
        assert type(updated_booking) is Booking

        manual_steps = ["Update Occupancy"]
        manual_steps.extend([{
                                 "room_type": room.room_type,
                                 "guest_count": room.guest_count(),
                             } for room in updated_booking.bookedroom_set.all()])
        return manual_steps