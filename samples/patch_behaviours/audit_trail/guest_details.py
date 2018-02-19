# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking
import json

class GuestDetailsPatch(BaseBehaviour):
    """
    patch any changes to guest-details
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.AuditTrail

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.GuestDetailsDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        audit guest details changes
        """
        super(GuestDetailsPatch, self).execute(diff_item, *args, **kwargs)

        parent_booking = diff_item.current_state()
        updated_booking = diff_item.target_state()

        assert type(parent_booking) is Booking
        assert type(updated_booking) is Booking

        room_ids = ','.join([str(room.id) for room in parent_booking.bookedroom_set.all()])

        msg = "updated guest details for room ids {room_ids}"

        updated_booking.audit_booking_update(msg.format(room_ids=room_ids))
