# SeatSpark – Movie & Event Seat Booking System

A Python Flask + SQLite web application developed as a B.Tech Software Engineering project. Users can browse movie/event listings, select a show, choose seats, complete a simulated booking, print a ticket, and manage bookings. Admin users can manage listings and show schedules.

## Features

- User registration and login with hashed passwords
- Movie and event catalogue
- Show date and time selection
- Interactive seat map with available/booked/selected states
- Silver, Gold and Platinum seat pricing
- Booking reference generation and printable e-ticket
- Booking history and cancellation
- Admin dashboard, listing management, show management and booking overview
- SQLite database created automatically on first run
- Database-level unique constraint prevents the same seat being booked twice for one show

## Technology

- Python 3.10+
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- SQLite
- HTML, CSS, JavaScript and Bootstrap 5

## Run locally

1. Install Python 3.10 or newer.
2. Download or clone this repository.
3. Open a terminal in the project directory.
4. Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the application:
   ```bash
   python app.py
   ```
7. Open `http://127.0.0.1:5000` in your browser.

The SQLite database is created in the Flask `instance` folder on first launch.

## Demo administrator

- Email: `admin@bookmyshow.local`
- Password: `Admin@123`

Change the demo admin password and the Flask secret key before any deployment. The demo credentials are for local academic demonstration only.

## First-time demo flow

1. Register a normal user account.
2. Log in.
3. Open a sample movie or event and select an available show.
4. Select seats and click **Confirm demo booking**.
5. View and print the generated ticket.
6. Open **My bookings** to view or cancel the booking.
7. Log in as the demo administrator to add listings and schedule shows.

Sample data is inserted automatically when the database is empty. Sample shows are dated in January 2027; an administrator can create additional dates.

## Project structure

```text
movie-event-booking-system/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── listing.html
│   ├── seats.html
│   ├── ticket.html
│   ├── my_bookings.html
│   └── admin/
├── static/
│   ├── css/style.css
│   └── js/main.js
├── documentation/
└── screenshots/
```

## Important project limitations

- Payment is simulated; no real payment gateway or financial transaction is used.
- Seat booking is protected by a database uniqueness constraint. For a production deployment, use a production database, transaction/retry strategy, CSRF protection, secure environment secrets, rate limiting, and proper deployment configuration.
- This is an academic prototype, not a production ticketing service.
- External Bootstrap and sample image URLs require an internet connection.

## Documentation

See the `documentation/` directory for the SRS, feasibility study, design diagrams, and test cases.

## GitHub upload

```bash
git init
git add .
git commit -m "Initial SeatSpark movie and event booking system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/movie-event-booking-system.git
git push -u origin main
```

Create an empty GitHub repository first, then replace the remote URL with your repository URL.

## Author

B.Tech Software Engineering Project  
Project: SeatSpark – Movie & Event Seat Booking System
