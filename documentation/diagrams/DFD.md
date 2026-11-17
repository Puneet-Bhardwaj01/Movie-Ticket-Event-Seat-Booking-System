# Data Flow Diagrams

## Level 0 – Context
External entities: Customer, Administrator.
Central process: SeatSpark Booking System.
Data stores: User Database, Listing/Show Database, Booking/Seat Database.

Customer sends registration/login data, listing search requests, show selection, seat selection and cancellation requests. The system returns listings, seat availability, booking confirmation, tickets and booking history.
Administrator sends listing/show management requests and receives dashboard and booking reports.

## Level 1 – Processes
1.0 Account Management: validates registration/login and reads/writes User Database.
2.0 Catalogue Management: reads listings and show schedules; administrator creates listings and shows.
3.0 Seat Availability: reads BookedSeat records for a selected show.
4.0 Booking Management: validates selected seats, calculates amount, creates Booking and BookedSeat records.
5.0 Ticket and Cancellation: retrieves ticket details or marks a booking cancelled and releases its seats.
