# -*- coding: utf-8 -*-
from dates import DatesPatch
from guest_details import GuestDetailsPatch
from occupancy import OccupancyPatch
from payments import PaymentsPatch
from rooms import RoomsPatch
from soft_block import SoftBlockPatch
from booking_status import BookingStatusPatch
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing import Patcher
from b2b.domain.services.diffing.patch_behaviours import BasePatchBehaviour


@Patcher.register_behaviour
class SelfUpdatePatch(BasePatchBehaviour):
    """
    contains patching mechanisms for updating own database according
    to what the CRS/Hx order contains

    corp-res team can make manual changes to the CRS order, and individual
    behaviours in this patch kit define how we reverse/back sync those changes
    into our own database
    """
    def __init__(self):
        super(SelfUpdatePatch, self).__init__(behaviours=[
            DatesPatch,
            GuestDetailsPatch,
            OccupancyPatch,
            PaymentsPatch,
            RoomsPatch,
            SoftBlockPatch,
            BookingStatusPatch
        ])

    @classmethod
    def name(cls):
        return DiffConsts.PatchBehaviours.SelfUpdate
