# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts


class Differ(object):
    """
    Differ diffs between two booking objects or one booking and
    one CRS-order-details object
    """

    _diff_mech_registry = {}

    @classmethod
    def register_diff_mech(cls, diff_mech_cls):
        """
        decorator for registering diff-mech kits
        """
        from b2b.domain.services.diffing.diffing_mechanisms import BaseDiffMech
        assert BaseDiffMech in diff_mech_cls.mro()

        diff_mech_name = diff_mech_cls.name()
        cls._diff_mech_registry[diff_mech_name] = diff_mech_cls

        return diff_mech_cls

    @classmethod
    def get_diff_mech(cls, diff_mech):
        """
        get specified diffing mechanism
        :param diff_mech: name of the diffing mechanism (one of DiffConsts.DiffingMechanisms enum)
        """
        if diff_mech not in cls._diff_mech_registry:
            raise RuntimeError('Unknown diffing mechanism {d}'.format(d=str(diff_mech)))

        return cls._diff_mech_registry[diff_mech]()

    @classmethod
    def diff_bookings(cls, b1, b2):
        """
        diffs two bookings
        returns a DiffSet containing DiffItems that tell what's missing in b1
        as compared to b2

        :param b1: old Booking object
        :param b2: new Booking object
        :return: DiffSet (b1-b2)
        """
        diff_mech = cls.get_diff_mech(DiffConsts.DiffingMechanisms.BookingDiffMech)
        return diff_mech.diff(b1, b2)

    @classmethod
    def diff_booking_and_crs_order(cls, booking, crs_order):
        """
        diffs a booking and crs-order-details
        returns a DiffSet containing DiffItems that detail what's missing in the
        booking compared to the crs order

        :param booking: Booking model object
        :param crs_order: CRSOrder object
        :return: DiffSet (what's missing in the booking compared to the crs-order)
        """
        diff_mech = cls.get_diff_mech(DiffConsts.DiffingMechanisms.CRSOrderBookingDiffMech)
        return diff_mech.diff(booking, crs_order)


