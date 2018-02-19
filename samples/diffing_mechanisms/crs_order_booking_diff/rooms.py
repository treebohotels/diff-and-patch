# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.diffing_mechanisms import BaseDiffItem


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

