# -*- coding: utf-8 -*-

from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking


class SoftBlockPatch(BaseBehaviour):
    """
    check-in/check-out date changes
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.AuditTrail

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.SoftBlockDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        audit check-in/check-out date changes
        """
        super(SoftBlockPatch, self).execute(diff_item, *args, **kwargs)

        parent_booking = diff_item.current_state()
        updated_booking = diff_item.target_state()

        assert type(parent_booking) is Booking
        assert type(updated_booking) is Booking

        if not updated_booking.is_soft_booking():
            updated_booking.audit_booking_update(
                "confirmed softblock with expiry  {expiry}".format(expiry=parent_booking.get_soft_booking_expiry()))

        else:
            msg = "updated soft-expiry date from {old_expiry} to {new_expiry}"
            updated_booking.audit_booking_update(msg.format(old_expiry=parent_booking.get_soft_booking_expiry(),

                                                            new_expiry=updated_booking.get_soft_booking_expiry()))
