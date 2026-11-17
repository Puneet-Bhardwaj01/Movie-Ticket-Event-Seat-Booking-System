from datetime import datetime, date, time
from functools import wraps
import os
import uuid

from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-development-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "booking.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
os.makedirs(app.instance_path, exist_ok=True)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)
    bookings = db.relationship("Booking", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default="")
    category = db.Column(db.String(20), nullable=False)  # Movie or Event
    image_url = db.Column(db.String(500), default="")
    venue = db.Column(db.String(150), nullable=False)
    shows = db.relationship("Show", backref="listing", cascade="all, delete-orphan", lazy=True)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id"), nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.Time, nullable=False)
    seat_count = db.Column(db.Integer, default=40, nullable=False)
    silver_price = db.Column(db.Float, default=150, nullable=False)
    gold_price = db.Column(db.Float, default=220, nullable=False)
    platinum_price = db.Column(db.Float, default=300, nullable=False)
    bookings = db.relationship("Booking", backref="show", lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
    seats = db.Column(db.String(500), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="CONFIRMED", nullable=False)
    payment_method = db.Column(db.String(30), default="Demo payment")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BookedSeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
    seat_label = db.Column(db.String(8), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)
    __table_args__ = (db.UniqueConstraint("show_id", "seat_label", name="uq_show_seat"),)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


def current_user():
    if "user_id" in session:
        return db.session.get(User, session["user_id"])
    return None


@app.context_processor
def inject_user():
    return {"current_user": current_user()}


@app.route("/")
def index():
    category = request.args.get("category")
    query = Listing.query
    if category in ("Movie", "Event"):
        query = query.filter_by(category=category)
    listings = query.order_by(Listing.id.desc()).all()
    return render_template("index.html", listings=listings, category=category)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 6:
            flash("Enter all details. Password must contain at least 6 characters.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
        else:
            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            session["name"] = user.name
            session["role"] = user.role
            return redirect(url_for("admin_dashboard") if user.role == "admin" else url_for("index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route("/listing/<int:listing_id>")
def listing_detail(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    shows = Show.query.filter_by(listing_id=listing.id).filter(Show.show_date >= date.today()).order_by(Show.show_date, Show.show_time).all()
    return render_template("listing.html", listing=listing, shows=shows)


@app.route("/show/<int:show_id>/seats")
@login_required
def seats(show_id):
    show = db.get_or_404(Show, show_id)
    booked = {s.seat_label for s in BookedSeat.query.filter_by(show_id=show.id).all()}
    return render_template("seats.html", show=show, booked=booked)


@app.route("/show/<int:show_id>/book", methods=["POST"])
@login_required
def book(show_id):
    show = db.get_or_404(Show, show_id)
    seats_selected = sorted(set(request.form.getlist("seats")))
    if not seats_selected:
        flash("Select at least one seat.", "warning")
        return redirect(url_for("seats", show_id=show.id))
    valid_seats = {f"{row}{n}" for row in "ABCDEFGH" for n in range(1, 6)}
    if any(s not in valid_seats for s in seats_selected) or len(seats_selected) > 10:
        flash("Invalid seat selection. You can select up to 10 seats.", "danger")
        return redirect(url_for("seats", show_id=show.id))

    price_map = {}
    for seat in seats_selected:
        row = seat[0]
        price_map[seat] = show.silver_price if row in "AB" else show.gold_price if row in "CDEF" else show.platinum_price

    booking = Booking(
        booking_code="BK" + uuid.uuid4().hex[:8].upper(),
        user_id=session["user_id"],
        show_id=show.id,
        seats=",".join(seats_selected),
        total_amount=sum(price_map.values()),
        payment_method="Demo payment",
        status="CONFIRMED"
    )
    try:
        db.session.add(booking)
        db.session.flush()
        for seat in seats_selected:
            db.session.add(BookedSeat(show_id=show.id, seat_label=seat, booking_id=booking.id))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("One or more selected seats have just been booked. Please choose again.", "danger")
        return redirect(url_for("seats", show_id=show.id))
    return redirect(url_for("ticket", booking_id=booking.id))


@app.route("/ticket/<int:booking_id>")
@login_required
def ticket(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.user_id != session["user_id"] and session.get("role") != "admin":
        abort(403)
    return render_template("ticket.html", booking=booking)


@app.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=session["user_id"]).order_by(Booking.created_at.desc()).all()
    return render_template("my_bookings.html", bookings=bookings)


@app.route("/booking/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.user_id != session["user_id"] and session.get("role") != "admin":
        abort(403)
    if booking.status == "CANCELLED":
        flash("This booking is already cancelled.", "warning")
    else:
        booking.status = "CANCELLED"
        BookedSeat.query.filter_by(booking_id=booking.id).delete()
        db.session.commit()
        flash("Booking cancelled. Seats are now available.", "success")
    return redirect(url_for("my_bookings") if session.get("role") != "admin" else url_for("admin_bookings"))


@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    return render_template("admin/dashboard.html",
        listing_count=Listing.query.count(),
        show_count=Show.query.count(),
        booking_count=Booking.query.count(),
        user_count=User.query.count())


@app.route("/admin/listings", methods=["GET", "POST"])
@login_required
@admin_required
def admin_listings():
    if request.method == "POST":
        listing = Listing(
            title=request.form["title"].strip(),
            description=request.form.get("description", "").strip(),
            category=request.form["category"],
            venue=request.form["venue"].strip(),
            image_url=request.form.get("image_url", "").strip()
        )
        db.session.add(listing)
        db.session.commit()
        flash("Movie/event added.", "success")
        return redirect(url_for("admin_listings"))
    return render_template("admin/listings.html", listings=Listing.query.order_by(Listing.id.desc()).all())


@app.route("/admin/listing/<int:listing_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_listing(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    db.session.delete(listing)
    db.session.commit()
    flash("Listing deleted.", "success")
    return redirect(url_for("admin_listings"))


@app.route("/admin/listing/<int:listing_id>/shows", methods=["GET", "POST"])
@login_required
@admin_required
def admin_shows(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    if request.method == "POST":
        try:
            show_date = datetime.strptime(request.form["show_date"], "%Y-%m-%d").date()
            show_time = datetime.strptime(request.form["show_time"], "%H:%M").time()
            show = Show(
                listing_id=listing.id, show_date=show_date, show_time=show_time,
                silver_price=float(request.form["silver_price"]),
                gold_price=float(request.form["gold_price"]),
                platinum_price=float(request.form["platinum_price"])
            )
            db.session.add(show)
            db.session.commit()
            flash("Show added.", "success")
        except (ValueError, KeyError):
            flash("Please enter valid show details and prices.", "danger")
        return redirect(url_for("admin_shows", listing_id=listing.id))
    return render_template("admin/shows.html", listing=listing, shows=Show.query.filter_by(listing_id=listing.id).order_by(Show.show_date).all())


@app.route("/admin/bookings")
@login_required
@admin_required
def admin_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin/bookings.html", bookings=bookings)


def seed_data():
    if not User.query.filter_by(email="admin@bookmyshow.local").first():
        admin = User(name="Project Admin", email="admin@bookmyshow.local", role="admin")
        admin.set_password("Admin@123")
        db.session.add(admin)
    if Listing.query.count() == 0:
        movie = Listing(title="The Last Horizon", category="Movie", venue="Grand Cinema, Panipat",
                        description="A sample adventure movie listing for demonstration.",
                        image_url="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=900")
        event = Listing(title="Live Music Night", category="Event", venue="City Auditorium, Panipat",
                        description="A sample live music event for demonstrating event ticket booking.",
                        image_url="https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=900")
        db.session.add_all([movie, event])
        db.session.flush()
        db.session.add_all([
            Show(listing_id=movie.id, show_date=date(2027, 1, 15), show_time=time(18, 30)),
            Show(listing_id=movie.id, show_date=date(2027, 1, 15), show_time=time(21, 30)),
            Show(listing_id=event.id, show_date=date(2027, 1, 20), show_time=time(19, 0))
        ])
    db.session.commit()


with app.app_context():
    db.create_all()
    seed_data()


if __name__ == "__main__":
    app.run(debug=True)
