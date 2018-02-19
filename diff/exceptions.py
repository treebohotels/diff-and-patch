# -*- coding: utf-8 -*-


class NoDifferenceDetected(Exception):
    """
    raised in the edit/update booking flow when there is no difference detected
    by diffing service between old and new bookings
    """

    def __init__(self, old_booking, new_booking):
        """
        :param old_booking: old Booking model object
        :param new_booking: new Booking model object
        """
        self.old_booking_id = old_booking.booking_id
        self.new_booking_id = new_booking.booking_id

        message = "No difference was detected in old ({ob}) and new ({nb}) bookings"
        super(NoDifferenceDetected, self).__init__(message.format(ob=self.old_booking_id,
                                                                  nb=self.new_booking_id))
