# -*- coding: utf-8 -*-
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking


class PaymentsPatch(BaseBehaviour):
    """
    patch any changes to payments
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.AuditTrail

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.PaymentsDiff

    def execute(self, diff_item, *args, **kwargs):
        super(PaymentsPatch, self).execute(diff_item, *args, **kwargs)

        """
                audit check-in/check-out date changes
                """
        super(PaymentsPatch, self).execute(diff_item, *args, **kwargs)

        parent_booking = diff_item.current_state()
        updated_booking = diff_item.target_state()

        assert type(parent_booking) is Booking
        assert type(updated_booking) is Booking

        msg = "updated payment from {o_b_s},{o_p_t},{o_t_p} to {n_b_s},{n_p_t},{n_t_p}"
        updated_booking.audit_booking_update(msg.format(o_b_s=parent_booking.get_booking_source(),o_p_t=parent_booking.payment_type(), o_t_p=parent_booking.total_payment(),

                                                        n_b_s=updated_booking.get_booking_source(),n_p_t=updated_booking.payment_type(), n_t_p=updated_booking.total_payment()))


