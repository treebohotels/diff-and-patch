# -*- coding: utf-8 -*-
from samples.patch_behaviours.crs_update.dates import DatesPatch
from samples.patch_behaviours.crs_update.guest_details import GuestDetailsPatch
from samples.patch_behaviours.crs_update.occupancy import OccupancyPatch
from samples.patch_behaviours.crs_update.payments import PaymentsPatch
from samples.patch_behaviours.crs_update.rooms import RoomsPatch
from samples.patch_behaviours.crs_update.soft_block import SoftBlockPatch
from samples.patch_behaviours.crs_update.booking_status import BookingStatusPatch
from samples.constants import DiffConsts
from diff import Patcher
from diff import BasePatchBehaviour


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
