# -*- coding: utf-8 -*-
from b2b.models import Booking, AdditionalGuests
from samples.constants import DiffConsts
from diff import BaseDiffItem


class GuestDetailsDiff(BaseDiffItem):
    """
    represents guest-details differences
    """
    @classmethod
    def diff_strategy(cls):
        return DiffConsts.DiffingStrategy.BookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.GuestDetailsDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        """
        Return true even in case of change of sequence of quests in rooms
        Args:
            lhs: Old Booking object
            rhs: New Booking Object

        Returns:

        """
        assert type(lhs) is Booking
        assert type(rhs) is Booking
        parent_bookedrooms = lhs.bookedroom_set.all()
        updated_bookedrooms = rhs.bookedroom_set.all()

        lhs_guests = [{
                          "guests": cls._get_guest_details(room),
                      } for room in parent_bookedrooms]

        rhs_guests = [{
                          "guests": cls._get_guest_details(room),
                      } for room in updated_bookedrooms]

        if lhs_guests != rhs_guests:
            return True

        return False

    @classmethod
    def _get_guest_details(cls, room):
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

    def patch_priority(self):
        # Guest details to be patched after occupancy but before payment and dates
        return 30
