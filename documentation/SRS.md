# Software Requirements Specification (SRS)
## SeatSpark – Movie & Event Seat Booking System

### 1. Introduction
SeatSpark is a web-based academic prototype for booking seats for movies and events. It provides a common platform for customers to discover listings, select a scheduled show, choose seats and receive a booking confirmation.

### 2. Purpose
The purpose is to demonstrate requirements analysis, web application design, database modelling, implementation, and software testing through a functioning ticket-booking application.

### 3. Scope
The system supports customer accounts, movie/event listings, show schedules, seat selection, booking, cancellation, printable tickets, and administrator management. Payment is simulated and does not process real money.

### 4. User classes
- **Visitor:** Can browse available listings and show details.
- **Registered customer:** Can book seats, view tickets, and cancel bookings.
- **Administrator:** Can create listings, schedule shows, and inspect bookings.

### 5. Functional requirements
| ID | Requirement |
|---|---|
| FR-01 | The system shall allow a visitor to register with name, email and password. |
| FR-02 | The system shall authenticate registered users. |
| FR-03 | The system shall display movie and event listings. |
| FR-04 | The system shall display future shows for a listing. |
| FR-05 | The system shall display available and booked seats for a show. |
| FR-06 | The customer shall select up to ten available seats. |
| FR-07 | The system shall calculate price according to seat category. |
| FR-08 | The system shall create a unique booking reference after a successful booking. |
| FR-09 | The system shall prevent a seat from being booked twice for the same show. |
| FR-10 | The customer shall view booking history and ticket details. |
| FR-11 | The customer shall cancel a confirmed booking. |
| FR-12 | The administrator shall add and delete listings. |
| FR-13 | The administrator shall schedule shows and set category prices. |
| FR-14 | The administrator shall view all bookings. |

### 6. Non-functional requirements
- Usability: pages should be understandable and responsive.
- Security: passwords are stored as hashes; protected routes require authentication.
- Reliability: database constraints prevent duplicate seat allocation.
- Maintainability: routes, models, templates and static assets are separated.
- Portability: the application runs on systems supporting Python and Flask.
- Performance: the prototype is intended for classroom-scale use.

### 7. Business rules
1. A user must be logged in to book seats.
2. A booking may contain a maximum of ten seats.
3. Rows A–B are Silver, C–F are Gold, and G–H are Platinum.
4. A seat is unique per show, not across all shows.
5. Cancelling a confirmed booking releases its seats.
6. Payment is a demonstration-only process.

### 8. Assumptions and constraints
- The user has a modern browser and network access for CDN assets.
- The initial deployment is local and uses SQLite.
- The sample administrator credentials must be changed before deployment.
- Real payment processing, SMS, and email delivery are outside the prototype scope.

### 9. Acceptance criteria
The project is accepted when a user can register, log in, browse a listing, select a show, book currently available seats, view a ticket, and cancel a booking; and an administrator can manage listings and show schedules.
