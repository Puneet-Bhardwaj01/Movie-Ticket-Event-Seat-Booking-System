# Class Diagram – model specification

- **User**: id, name, email, password_hash, role. Operations: set_password(), check_password().
- **Listing**: id, title, description, category, image_url, venue. One Listing has many Shows.
- **Show**: id, listing_id, show_date, show_time, seat_count, silver_price, gold_price, platinum_price. One Show belongs to one Listing and has many Bookings.
- **Booking**: id, booking_code, user_id, show_id, seats, total_amount, status, payment_method, created_at. One Booking belongs to one User and one Show.
- **BookedSeat**: id, show_id, seat_label, booking_id. Unique constraint on (show_id, seat_label).

Relationships:
- User 1 — many Booking
- Listing 1 — many Show
- Show 1 — many Booking
- Booking 1 — many BookedSeat
