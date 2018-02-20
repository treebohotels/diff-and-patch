# -*- coding: utf-8 -*-
import logging

from b2b.consumer.crs.crs_order import get_b2b_order
from b2b.models import Booking
from samples.constants import DiffConsts
from diff import BaseBehaviour


class DatesPatch(BaseBehaviour):
    """
    check-in/check-out date changes
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.CRSUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.DatesDiff

    def execute(self, diff_item, *args, **kwargs):
        super(DatesPatch, self).execute(diff_item, *args, **kwargs)

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
        logger.info("Updating stay dates as per {o}".format(o=repr(b2b_order)))
        with crs_txn_mgr:
            crs_txn_mgr.update_stay_dates(b2b_order)
