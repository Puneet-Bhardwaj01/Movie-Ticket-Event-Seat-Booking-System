# Use Case Diagram – textual specification

Actors:
- Visitor
- Registered Customer
- Administrator

Visitor use cases:
- Browse movies and events
- View listing details
- Register
- Log in

Registered Customer use cases:
- Select show
- View seat availability
- Select seats
- Confirm demo booking
- View/print ticket
- View booking history
- Cancel booking
- Log out

Administrator use cases:
- Log in
- Add/delete movie or event
- Schedule shows and set prices
- View all bookings
- Cancel bookings
- View dashboard

Relationship: A registered customer is an authenticated visitor. Administrator is a privileged user with all admin management use cases.
