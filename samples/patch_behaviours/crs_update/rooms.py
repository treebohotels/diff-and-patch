# -*- coding: utf-8 -*-
from samples.constants import DiffConsts
from diff import BaseBehaviour


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
