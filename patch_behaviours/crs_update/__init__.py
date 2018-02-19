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
class CRSUpdatePatch(BasePatchBehaviour):
    """
    contains patching mechanisms for pushing diff-items to CRS/Hx
    """
    def __init__(self):
        super(CRSUpdatePatch, self).__init__(behaviours=[
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
        return DiffConsts.PatchBehaviours.CRSUpdate
