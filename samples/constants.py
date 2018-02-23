# -*- coding: utf-8 -*-

from enum import Enum


class DiffConsts(object):
    """
    collection of all constants for the diffing subsystem
    """
    class DiffTypes(Enum):
        BrandDiff = 8
        ModelDiff = 9
        MakeDiff = 10
        VariantDiff = 11

    class DiffingStrategy(Enum):
        DiffingMechanisms = 1
        BookingDiffMech = 2
        CarDiff = 3

    class PatchBehaviours(Enum):
        PatchBehaviours = 1
        CRSUpdate = 2
        AuditTrail = 3
