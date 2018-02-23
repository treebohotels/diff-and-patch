# -*- coding: utf-8 -*-
from b2b.models import Booking
from samples.constants import DiffConsts
from diff import BaseDiffItem


class OccupancyDiff(BaseDiffItem):
    """
    reprensets occupancy diff in two bookings
    """
    @classmethod
    def diff_strategy(cls):
        return DiffConsts.DiffingStrategy.BookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.OccupancyDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        """
        Return true even in case of change in sequence of occupancy of rooms
        :param lhs: existing Booking model object
        :param rhs: updated Booking model object
        :return: True if occupancies have changed in the updated one
        """
        assert type(lhs) is Booking
        assert type(rhs) is Booking

        lhs_guest_counts = [
             room.guest_count() for room in lhs.bookedroom_set.all()]

        rhs_guest_counts = [
             room.guest_count() for room in rhs.bookedroom_set.all()]

        if lhs_guest_counts != rhs_guest_counts:
            return True

        return False

    def patch_priority(self):
        # Occupancy to be checked before guest details but after room addition and deletion
        return 20
