# -*- coding: utf-8 -*-
import logging

from b2b.consumer.crs.crs_order import get_b2b_order
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking
from b2b.constants import Booking as BookingConstants


class SoftBlockPatch(BaseBehaviour):
    """
    Softblock expiry date changes
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.CRSUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.SoftBlockDiff

    def execute(self, diff_item, *args, **kwargs):
        super(SoftBlockPatch, self).execute(diff_item, *args, **kwargs)

        logger = logging.getLogger(self.__class__.__name__)

        try:
            parent_booking = kwargs['old_booking']
            updated_booking = kwargs['new_booking']
            crs_txn_mgr = kwargs['crs_txn_mgr']

        except KeyError as e:
            msg = "{cls} needs to know {m}, but it's missing in the args".format(cls=self.__class__.__name__,
                                                                                 m=e.message)
            logger.error(msg)

            raise RuntimeError(msg)

        # ensure both of them are Booking model objects
        assert type(parent_booking) is Booking
        assert type(updated_booking) is Booking

        # convert the updated booking object into the unified booking interface object
        b2b_order = get_b2b_order(updated_booking)

        # finally, hand over the order to the transaction manager for further processing
        logger.info("Updating softbooking as per {o}".format(o=repr(b2b_order)))

        if parent_booking.is_soft_booking() and updated_booking.is_soft_booking():
            with crs_txn_mgr:
                crs_txn_mgr.update_softblock_expiry(b2b_order)
        if parent_booking.is_soft_booking() and not updated_booking.is_soft_booking():
            crs_txn_mgr.confirm_booking(b2b_order)
            updated_booking.set_status(BookingConstants.CONFIRMED)
            updated_booking.save()


