# -*- coding: utf-8 -*-

from enum import Enum


class DiffConsts(object):
    """
    collection of all constants for the diffing subsystem
    """
    class DiffTypes(Enum):
        DatesDiff = 1
        GuestDetailsDiff = 2
        OccupancyDiff = 3
        PaymentsDiff = 4
        RoomsDiff = 5
        SoftBlockDiff = 6
        BookingStatusDiff = 7

    class DiffingMechanisms(Enum):
        DiffingMechanisms = 1
        BookingDiffMech = 2
        CRSOrderBookingDiffMech = 3

    class PatchBehaviours(Enum):
        PatchBehaviours = 1
        CRSUpdate = 2
        ManualOverrideSteps = 3
        SelfUpdate = 4
        AuditTrail = 5
