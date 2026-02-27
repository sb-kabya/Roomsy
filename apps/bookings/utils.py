from django.core.mail import send_mail
from django.conf import settings
def send_booking_confirmation(booking):
    subject = f"Booking Confirmed - {booking.hotel_name} | StayEase"
    message = f"""
Hi {booking.user.first_name},

Your booking is confirmed!
Booking Reference: #{str(booking.booking_id).upper()[:8]}
Hotel: {booking.hotel_name}
Room: {booking.room.room_number} ({booking.room.get_room_type_display()})
Check-in: {booking.check_in_date}
Check-out: {booking.check_out_date}
Nights: {booking.total_nights}
Total Paid: ${booking.total_price}

Thank you for choosing Roomsy!
"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False
        )
    except Exception as e:
        print(f"[Email Error] {e}")
