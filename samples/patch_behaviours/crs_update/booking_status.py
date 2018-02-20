# -*- coding: utf-8 -*-
from samples.constants import DiffConsts
from diff import BaseBehaviour


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
