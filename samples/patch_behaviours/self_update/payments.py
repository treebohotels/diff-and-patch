# -*- coding: utf-8 -*-
from decimal import Decimal

from b2b import constants
from b2b.consumer.crs.crs_order import CRSBookingOrderInterface
from b2b.domain.services.diffing import DiffConsts
from b2b.domain.services.diffing.patch_behaviours import BaseBehaviour
from b2b.models import Booking, BookingInclusions
from b2b.domain.utils.date_utils import count_room_nights
from b2b.domain.services.pricing import PricingService

class PaymentsPatch(BaseBehaviour):
    """
    patch any changes to payments
    """

    @classmethod
    def behaviour_kit(cls):
        return DiffConsts.PatchBehaviours.SelfUpdate

    @classmethod
    def associated_diff_type(cls):
        return DiffConsts.DiffTypes.PaymentsDiff

    def execute(self, diff_item, *args, **kwargs):
        super(PaymentsPatch, self).execute(diff_item, *args, **kwargs)

        old_booking = diff_item.current_state()
        assert type(old_booking) is Booking

        booking = Booking.objects.get(id=old_booking.id)
        assert type(booking) is Booking

        crs_order = diff_item.target_state()
        assert CRSBookingOrderInterface in type(crs_order).mro()

        if float(booking.pre_tax_price) != crs_order.total_payment():
            pricing_service = PricingService(corporate_id=booking.corporate.corporate_id)
            room_nights = count_room_nights(str(booking.check_in), str(booking.check_out))
            bookedroom_payment_map = crs_order.bookedroom_payment_map()
            pre_tax_price = 0
            old_pre_tax_price = 0
            flexible_prices = pricing_service.get_flexi_min_prices(booking) if booking.is_flexi_booking() else {}
            for bookedroom in booking.bookedroom_set.all():
                old_pre_tax_price += Decimal(bookedroom.pre_tax_price)
                ep_charges = (bookedroom.adults-1)*flexible_prices[bookedroom.room_type] if bookedroom.room_type in flexible_prices else self.build_ep_dto(bookedroom.room_type,booking,bookedroom.adults)['price']
                key = (bookedroom.room_type, str(
                    bookedroom.guest_count()))
                bookedroom.pre_tax_price = round(
                    Decimal(bookedroom_payment_map[key]) - ep_charges*room_nights+ bookedroom.tmc_commission, 2)
                pre_tax_price += Decimal(bookedroom_payment_map[key]) - ep_charges*room_nights + bookedroom.tmc_commission
                bookedroom.save()
            booking.pre_tax_price = booking.pre_tax_price - old_pre_tax_price + pre_tax_price

        if crs_order.get_payterm() != booking.get_payterm():
            if crs_order.get_payterm() == '1':
                booking.sub_channel = constants.Booking.BTC
            else:
                booking.sub_channel = constants.Booking.DIRECT

        if crs_order.get_booking_source() == constants.Booking.BTC:
            if 'Bill to Treebo' in crs_order.get_payment_desc():
                booking.sub_channel = constants.Booking.BTT
            else:
                booking.sub_channel = constants.Booking.BTC

        else:
            booking.sub_channel = constants.Booking.DIRECT

        booking.save()

        booking.audit_backsync(
            "payment: {bs},{pt},{po}".format(po=crs_order.total_payment(), pt=crs_order.get_payterm(),
                                             bs=crs_order.get_booking_source()))


    @classmethod
    def _get_extra_person_prices(self, room_type, booking, adults):
        from b2b.dto import EPChargeRequestDTO
        from b2b.domain.services.pricing import PricingService
        ep_charge_request_dto = EPChargeRequestDTO(data=dict(corporate=booking.corporate.corporate_id,
                                                             hotel=booking.hotel.hotel_id,
                                                             from_date=booking.check_in,
                                                             to_date=booking.check_out,
                                                             room_type=room_type,
                                                             room_config=str(adults)+'-0'))

        pricing_service = PricingService(corporate_id=booking.corporate.corporate_id)
        ep_charges_dto = pricing_service.get_extra_person_charges(ep_charge_request_dto)
        if not ep_charges_dto.is_valid():
            # TODO: Segregate Exception Types
            raise Exception('Invalid data received from Pricing Service for Extra person charges')
        return ep_charges_dto.data

    @classmethod
    def build_ep_dto(self, room_type, booking, adults):
        ep_charges = {'price': Decimal(self._get_extra_person_prices(room_type, booking, adults)['pre_tax_charge'])}
        return ep_charges

    @classmethod
    def __update_ep_inclusion(self, crs_order, booking):
        crs_booked_rooms = crs_order.booked_rooms()
        for booked_room in booking.bookedroom_set.all():
            for crs_booked_room in crs_booked_rooms:
                br_guest_count = booked_room.guest_count()
                guest_count_diff = len(crs_booked_room["guests_details"]) - br_guest_count
                if booked_room.room_type.lower() == crs_booked_room['room_type'].lower() and guest_count_diff == 0:
                    pricing_service = PricingService(corporate_id=booking.corporate.corporate_id)
                    room_nights = count_room_nights(str(booking.check_in), str(booking.check_out))
                    flexible_prices = pricing_service.get_flexi_min_prices(booking) if booking.is_flexi_booking() else {}
                    ep_charges = (booked_room.adults - 1) * flexible_prices[
                        booked_room.room_type] if booked_room.room_type in flexible_prices else \
                        self.build_ep_dto(booked_room.room_type, booking, booked_room.adults)['price']
                    EP_CHARGES = constants.Inclusions.EPCharges
                    try:
                        ep_inclusion_instance = BookingInclusions.objects.get(booking=booking, category=
                        constants.Inclusions.CategoryMapping[
                            EP_CHARGES], booked_room=booked_room)
                        ep_inclusion_instance.pre_tax_price = ep_charges * room_nights
                        ep_inclusion_instance.save()
                    except BookingInclusions.DoesNotExist:
                        BookingInclusions.objects.create(booking=booking,
                                                         category=
                                                         constants.Inclusions.CategoryMapping[
                                                             EP_CHARGES],
                                                         inclusion=EP_CHARGES,
                                                         pre_tax_price=ep_charges * room_nights,
                                                         booked_room=booked_room
                                                         )
                    break
