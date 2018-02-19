# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking, Guest, AdditionalGuests
from b2b.consumer.crs.crs_order import CRSBookingOrderInterface


class OccupancyPatch(BaseBehaviour):
    """
    patch any changes to occupancy details
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.SelfUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.OccupancyDiff

    def execute(self, diff_item, *args, **kwargs):
        """
        check check-in/check-out dates and update what doesn't match
        """
        super(OccupancyPatch, self).execute(diff_item, *args, **kwargs)

        old_booking = diff_item.current_state()
        assert type(old_booking) is Booking

        booking = Booking.objects.get(id=old_booking.id)
        assert type(booking) is Booking

        crs_order = diff_item.target_state()
        assert CRSBookingOrderInterface in type(crs_order).mro()
        # lhs_guest_counts = [room.guest_count() for room in booking.bookedroom_set.all()]
        # rhs_guest_counts = [len(crs_br['guests_details']) for crs_br in crs_order]
        crs_booked_rooms = crs_order.booked_rooms()
        traversed_crs_rooms = []
        for booked_room in booking.bookedroom_set.all():
            for crs_booked_room in crs_booked_rooms:
                br_guest_count = booked_room.guest_count()
                # get the index of crs_booked_room
                crs_room_index = crs_booked_rooms.index(crs_booked_room)
                if booked_room.room_type.lower() == crs_booked_room['room_type'].lower() and \
                        crs_room_index not in traversed_crs_rooms:
                    # adding the entry in a list not to traverse them again
                    traversed_crs_rooms.append(crs_room_index)
                    guest_count_diff = len(crs_booked_room["guests_details"]) - br_guest_count
                    if guest_count_diff > 0:
                        for count in range(guest_count_diff):
                            guest = Guest.objects.create(
                                salutation="Mr",
                                name="N/A",
                                email="N/A",
                                gender="M",
                                phone="N/A"
                            )
                            AdditionalGuests.objects.create(booking_id=booking,
                                                            booked_room=booked_room,
                                                            guest=guest)
                    else:
                        additional_guests = booked_room.additional_guests()
                        for count in range(abs(guest_count_diff)):
                            additional_guests[count].delete()
                    break

        booked_rooms_ids = ','.join([str(room.id) for room in booking.bookedroom_set.all()])

        msg = "Backsync done for Occupancy for room ids {room_ids}"
        booking.audit_backsync(msg.format(room_ids=booked_rooms_ids))
