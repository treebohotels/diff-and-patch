# -*- coding: utf-8 -*-
from dates import DatesDiff
from guest_details import GuestDetailsDiff
from occupancy import OccupancyDiff
from payments import PaymentsDiff
from rooms import RoomsDiff
from soft_block import SoftBlockDiff
from booking_status import BookingStatusDiff

from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.diffing_mechanisms import BaseDiffMech
from b2b.domain.services.diffing import Differ


@Differ.register_diff_mech
class CRSOrderBookingDiffMech(BaseDiffMech):
    """
    collects DiffItems for diffing two bookings
    """

    def __init__(self):
        super(CRSOrderBookingDiffMech, self).__init__(diff_items=[
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
        return DiffConsts.DiffingMechanisms.CRSOrderBookingDiffMech
