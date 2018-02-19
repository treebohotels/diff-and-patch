# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking

class GuestDetailsPatch(BaseBehaviour):
    """
    patch any changes to guest-details
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.ManualOverrideSteps

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.GuestDetailsDiff

    def execute(self, diff_item, *args, **kwargs):
        super(GuestDetailsPatch, self).execute(diff_item, *args, **kwargs)

        updated_booking = diff_item.target_state()
        assert type(updated_booking) is Booking

        updated_bookedrooms = updated_booking.bookedroom_set.all()

        manual_steps = ["Update Guest Details"]
        manual_steps.extend([self._get_guest_details(room) for room in updated_bookedrooms])
        return manual_steps

    def _get_guest_details(self, room):
        return {"addtional_guests": [{
                                         "name": ag.name,
                                         "email": ag.email,
                                         "phone": ag.phone,
                                         "gender": ag.gender,
                                     }
                                     for ag in room.additional_guests()],
                "primary_guest": {
                    "name": room.guest.name,
                    "email": room.guest.email,
                    "phone": room.guest.phone,
                    "gender": room.guest.gender
                }
                }
