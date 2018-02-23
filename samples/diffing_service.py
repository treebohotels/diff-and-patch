# -*- coding: utf-8 -*-
from samples.constants import DiffConsts
from diff.differ import Differ
from diff.patcher import Patcher
from diff.exceptions import NoDifferenceDetected
from samples.exceptions import CrsUpdateBookingFailed


class DiffingService(object):
    """
    finds differences between two bookings or a booking and corresponding crs order,
    and applies appropriate behaviour to bring them in sync
    """

    @classmethod
    def check_diff(cls, old_booking, new_booking, audit=False):
        """
        checks the difference between old and new booking (new state for the same old booking)
        used to veto an update-booking request in its tracks if the DiffingService finds
        no difference between the existing booking and the request

        :param old_booking: current Booking (model object)
        :param new_booking: new state of the Booking (model object)
        :param audit: should the changes in the new booking be audited?
        :raises: NoDifferenceDetected if there is no difference between the two bookings
        """
        # diff the bookings
        diff_set = DiffingService.diff_bookings(old_booking, new_booking)

        # check if there was no diff detected
        if diff_set.is_empty():
            raise NoDifferenceDetected(old_booking, new_booking)

        if audit:
            # apply AuditTrail patch behaviour to the diff-set
            audit_trail_behaviour = Patcher.get_behaviour(DiffConsts.PatchBehaviours.AuditTrail)
            diff_set.attach_behaviour(patch_behaviour_kit=audit_trail_behaviour)

            # execute the actions on collected diff-items
            diff_set.execute(remove_on_success=False)

    @classmethod
    def diff_and_update_booking_in_crs(cls, old_booking, new_booking, txn_manager):
        """
        diffs between old and new booking (new state for the same old booking), and
        syncs the differences into the CRS

        :param old_booking: booking object for the current booking
        :param new_booking: booking object representing new state of the booking
        :param txn_manager: the CRS transaction manager to talk to for updating the booking
        """
        # diff the bookings
        diff_set = DiffingService.diff_bookings(old_booking, new_booking)

        # check if there was no diff detected
        if diff_set.is_empty():
            raise NoDifferenceDetected(old_booking, new_booking)

        # apply CRSUpdate patch behaviour to the diff-set
        crs_update_behaviour = Patcher.get_behaviour(DiffConsts.PatchBehaviours.CRSUpdate)
        diff_set.attach_behaviour(patch_behaviour_kit=crs_update_behaviour)

        # finally execute the actions on the diff-items
        diff_set.execute(remove_on_success=True,
                         old_booking=old_booking,
                         new_booking=new_booking,
                         crs_txn_mgr=txn_manager)

        # if there is still some diff-items remaining, there was a failure,
        # and we need to trigger manual action
        if not diff_set.is_empty():
            # attach ManualOverrideSteps behaviour to rest of the diff items
            manual_override_steps_behaviour = Patcher.get_behaviour(DiffConsts.PatchBehaviours.ManualOverrideSteps)
            diff_set.attach_behaviour(patch_behaviour_kit=manual_override_steps_behaviour)

            # then execute the actions, and collect the result
            diff_set.execute(remove_on_success=True)

            raise CrsUpdateBookingFailed(old_booking=old_booking.booking_id, updated_booking=new_booking.booking_id)

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
        diff_mech = Differ.get_strategy(DiffConsts.DiffingStrategy.BookingDiffMech)
        return diff_mech.diff(b1, b2)
