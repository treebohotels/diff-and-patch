# -*- coding: utf-8 -*-
import logging

from b2b.consumer.crs.crs_order import get_b2b_order
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking


class BookingStatusPatch(BaseBehaviour):
    """
    Softblock expiry date changes
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.CRSUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.BookingStatusDiff

    def execute(self, diff_item, *args, **kwargs):
        pass
