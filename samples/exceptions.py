# -*- coding: utf-8 -*-


class CrsUpdateBookingFailed(Exception):
    """
    Raised when update Booking is failed in CRS
    """
    def __init__(self, old_booking, updated_booking):
        msg = "Edit Booking Failed for old booking {old_booking} and updated booking {updated_booking}"
        super(CrsUpdateBookingFailed, self).__init__(msg.format(old_booking=old_booking,
                                                                updated_booking=updated_booking))
