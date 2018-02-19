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
        return DiffConsts.PatchBehaviours.ManualOverrideSteps

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.PaymentsDiff

    def execute(self, diff_item, *args, **kwargs):
        super(PaymentsPatch, self).execute(diff_item, *args, **kwargs)

        updated_booking = diff_item.target_state()
        assert type(updated_booking) is Booking

        return ['Update Payments',
            "booking-source: {bs}".format(bs=updated_booking.get_booking_source()),
            "payment-type: {pt}".format(pt=updated_booking.payment_type()),
            "payment-amount: {po}".format(po=updated_booking.total_payment())]
