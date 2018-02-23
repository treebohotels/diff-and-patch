# -*- coding: utf-8 -*-
from samples.diffing_mechanisms.booking_diff.dates import DatesDiff
from samples.diffing_mechanisms.booking_diff.guest_details import GuestDetailsDiff
from samples.diffing_mechanisms.booking_diff.occupancy import OccupancyDiff
from samples.diffing_mechanisms.booking_diff.payments import PaymentsDiff
from samples.diffing_mechanisms.booking_diff.rooms import RoomsDiff
from samples.diffing_mechanisms.booking_diff.soft_block import SoftBlockDiff
from samples.diffing_mechanisms.booking_diff.booking_status import BookingStatusDiff
from diff import BaseDiffStrategy
from samples.constants import DiffConsts
from diff import Differ


@Differ.register_strategy
class BookingDiffMech(BaseDiffStrategy):
    """
    collects DiffItems for diffing two bookings
    """
    def __init__(self):
        super(BookingDiffMech, self).__init__(diff_items=[
            DatesDiff,
            GuestDetailsDiff,
            OccupancyDiff,
            PaymentsDiff,
            RoomsDiff,
            SoftBlockDiff,
            BookingStatusDiff
        ])

    @classmethod
    def name(cls):
        return DiffConsts.DiffingStrategy.BookingDiffMech
