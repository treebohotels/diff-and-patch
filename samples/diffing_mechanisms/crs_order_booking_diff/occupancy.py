# -*- coding: utf-8 -*-
from b2b.models import Booking
from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from samples.constants import DiffConsts
from diff import BaseDiffItem


class OccupancyDiff(BaseDiffItem):
    """
    reprensets occupancy diff in two bookings
    """
    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.CRSOrderBookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.OccupancyDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        """
        This method considers the sequence of occupancies. Return true if the sequence is changed for occupancies
        In case hx order have occupancy listing in different order due to crs response, this method would still
        return true even if there is no actual occupancy change.
        :param lhs: existing Booking model object
        :param rhs: CRS order details conforming to CRSBookingOrderInterface
        :return: True if guests count do not match in the booking
        """
        assert type(lhs) is Booking
        assert CRSBookingOrderInterface in type(rhs).mro()

        rhs_booked_rooms = rhs.booked_rooms()
        lhs_booked_rooms = lhs.bookedroom_set.all()
        lhs_guest_counts = [room.guest_count() for room in lhs_booked_rooms]
        rhs_guest_counts = [len(crs_br['guests_details']) for crs_br in rhs_booked_rooms]
        if lhs_guest_counts != rhs_guest_counts:
            return True

        return False

    def patch_priority(self):
        # Occupancy to be checked before guest details but after room addition and deletion
        return 20
