# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.diffing_mechanisms import BaseDiffItem
from b2b.models import Booking
from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from b2b.domain.utils.misc import full_name

class GuestDetailsDiff(BaseDiffItem):
    """
    represents guest-details differences
    """
    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.CRSOrderBookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.GuestDetailsDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        assert type(lhs) is Booking
        assert CRSBookingOrderInterface in type(rhs).mro()
        rhs_booked_rooms = rhs.booked_rooms()
        lhs_booked_rooms = lhs.bookedroom_set.all()
        lhs_guests = [cls._get_guest_details(room) for room in lhs_booked_rooms]
        rhs_guests = [cls._get_crs_guest_details(room) for room in rhs_booked_rooms]
        if lhs_guests != rhs_guests:
            return True

        return False

    @classmethod
    def _get_guest_details(cls, room):
        return {"additional_guests": [{
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

    @classmethod
    def _get_crs_guest_details(cls, room):
        rhs_guest_details = {}
        additional_guest_details = []
        for guest_details in room['guests_details']:
            if guest_details['is_primary'] is True:
                rhs_guest_details['primary_guest'] = {
                    "name": full_name(guest_details["first_name"], guest_details["last_name"]),
                    "email": guest_details['email'],
                    "phone": guest_details['phone'],
                    "gender": guest_details['gender']
                }
            else:
                additional_guest_details.append(
                {
                    "name": full_name(guest_details["first_name"], guest_details["last_name"]),
                    "email": guest_details['email'],
                    "phone": guest_details['phone'],
                    "gender": guest_details['gender']
                }
                )
        rhs_guest_details['additional_guests'] = additional_guest_details
        return rhs_guest_details

    def patch_priority(self):
        # Guest details to be patched after occupancy but before payment and dates
        return 30
