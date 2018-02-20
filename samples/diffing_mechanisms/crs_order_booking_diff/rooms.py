# -*- coding: utf-8 -*-
from samples.constants import DiffConsts
from diff import BaseDiffItem


class RoomsDiff(BaseDiffItem):
    """
    reprensets rooms diff in two bookings
    """
    @classmethod
    def diff_mech(cls):
        return DiffConsts.DiffingMechanisms.CRSOrderBookingDiffMech

    @classmethod
    def diff_type(cls):
        return DiffConsts.DiffTypes.RoomsDiff

    @classmethod
    def is_applicable(cls, lhs, rhs):
        return False
