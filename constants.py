# -*- coding: utf-8 -*-

from enum import Enum


class DiffConsts(object):
    """
    collection of all constants for the diffing subsystem
    """
    DiffTypes = Enum('DiffTypes',
                     'DatesDiff '
                     'GuestDetailsDiff '
                     'OccupancyDiff '
                     'PaymentsDiff '
                     'RoomsDiff '
                     'SoftBlockDiff '
                     'BookingStatusDiff ')

    DiffingMechanisms = Enum('DiffingMechanisms',
                             'BookingDiffMech '          # diff between two bookings
                             'CRSOrderBookingDiffMech '  # diff between a booking and a crs order
                             )

    PatchBehaviours = Enum('PatchBehaviours',
                           'CRSUpdate '
                           'ManualOverrideSteps '
                           'SelfUpdate '
                           'AuditTrail ')


