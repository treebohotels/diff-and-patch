# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour


class RoomsPatch(BaseBehaviour):
    """
    patch any changes in booked rooms
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.CRSUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.RoomsDiff

    def execute(self, diff_item, *args, **kwargs):
        super(RoomsPatch, self).execute(diff_item, *args, **kwargs)

        # todo: implement this
