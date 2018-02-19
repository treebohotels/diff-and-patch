# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking, Guest, AdditionalGuests
from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from b2b.domain.utils.misc import full_name

class GuestDetailsPatch(BaseBehaviour):
    """
    patch any changes to guest-details
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.SelfUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.GuestDetailsDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        Update guest details from hx
        Args:
            diff_item:
            *args:
            **kwargs:

        Returns:

        """

        super(GuestDetailsPatch, self).execute(diff_item, *args, **kwargs)

        old_booking = diff_item.current_state()
        assert type(old_booking) is Booking

        booking = Booking.objects.get(id=old_booking.id)
        assert type(booking) is Booking

        crs_order = diff_item.target_state()
        assert CRSBookingOrderInterface in type(crs_order).mro()

        booked_rooms = booking.bookedroom_set.all()
        crs_booked_rooms = crs_order.booked_rooms()

        crs_booked_rooms_indices = []
        for br in booked_rooms:
            for cbr in crs_booked_rooms:
                if br.room_type.lower() == cbr['room_type'] and int(br.guest_count()) == int(cbr['adult_count'])\
                        and crs_booked_rooms.index(cbr) not in crs_booked_rooms_indices:
                    cbr_guest_details = cbr['guests_details']

                    primary_guest = [guest_details for guest_details in cbr_guest_details
                                        if guest_details['is_primary'] is True]
                    # Only one primary guest per booking
                    p_guest = br.guest

                    if len(primary_guest) > 0:
                        primary_guest = primary_guest[0]
                        p_guest.name = full_name(primary_guest["first_name"], primary_guest["last_name"])
                        p_guest.gender = primary_guest["gender"]
                        p_guest.email = primary_guest["email"]
                        p_guest.phone = primary_guest["phone"]
                        p_guest.salutation = primary_guest["salutation"]

                    else:
                        p_guest.name = "N/A"
                        p_guest.gender = "M"
                        p_guest.email = "N/A"
                        p_guest.phone = "N/A"
                        p_guest.salutation = "Mr"

                    p_guest.save()

                    additional_guests = [guest_details for guest_details in
                                         cbr_guest_details if guest_details['is_primary'] is False]

                    br_additional_guests = br.additional_guests()

                    for br_ag in br_additional_guests:
                        index = br_additional_guests.index(br_ag)
                        br_ag.name = full_name(additional_guests[index]["first_name"],
                                               additional_guests[index]["last_name"])
                        br_ag.gender = additional_guests[index]["gender"]
                        br_ag.email = additional_guests[index]["email"]
                        br_ag.phone = additional_guests[index]["phone"]
                        br_ag.salutation = additional_guests[index]["salutation"]
                        br_ag.save()
                    crs_booked_rooms_indices.append(crs_booked_rooms.index(cbr))
                    break

        booked_rooms_ids = ','.join([str(room.id) for room in booked_rooms])

        msg = "Backsync done for guest details for room ids {room_ids}"

        booking.audit_backsync(msg.format(room_ids=booked_rooms_ids))
