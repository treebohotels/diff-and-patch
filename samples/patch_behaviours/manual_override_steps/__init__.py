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
class ManualOverridePatch(BasePatchBehaviour):
    """
    contains patching mechanisms for generating manual-override steps
    for the corporate-reservation team to execute, in case of failure

    the individual behaviours in this kit define steps to execute for
    associated diff-types
    """
    def __init__(self):
        super(ManualOverridePatch, self).__init__(behaviours=[
            DatesPatch,
            GuestDetailsPatch,
            OccupancyPatch,
            PaymentsPatch,
            RoomsPatch,
            SoftBlockPatch
        ])

    @classmethod
    def name(cls):
        return DiffConsts.PatchBehaviours.ManualOverrideSteps
