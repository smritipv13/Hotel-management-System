from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for
from mysql.connector import Error

from database import execute, fetch_all, fetch_one


app = Flask(__name__)
app.config["SECRET_KEY"] = "hotel-management-dev-key"


ROOM_STATUSES = ("Available", "Occupied", "Maintenance")
BOOKING_STATUSES = ("Booked", "Checked In", "Checked Out", "Cancelled")
PAYMENT_METHODS = ("Cash", "Card", "UPI", "Net Banking")
PAYMENT_STATUSES = ("Pending", "Paid", "Refunded")


@app.errorhandler(Error)
def handle_database_error(error):
    return render_template("error.html", message=str(error)), 500


@app.route("/")
def dashboard():
    stats = {
        "customers": fetch_one("SELECT COUNT(*) AS total FROM customers")["total"],
        "rooms": fetch_one("SELECT COUNT(*) AS total FROM rooms")["total"],
        "bookings": fetch_one("SELECT COUNT(*) AS total FROM bookings")["total"],
        "revenue": fetch_one(
            "SELECT COALESCE(SUM(amount), 0) AS total FROM payments WHERE status = 'Paid'"
        )["total"],
    }
    recent_bookings = fetch_all(
        """
        SELECT b.booking_id, c.name AS customer_name, r.room_number, b.check_in,
               b.check_out, b.status
        FROM bookings b
        JOIN customers c ON c.customer_id = b.customer_id
        JOIN rooms r ON r.room_id = b.room_id
        ORDER BY b.booking_id DESC
        LIMIT 5
        """
    )
    return render_template("dashboard.html", stats=stats, recent_bookings=recent_bookings)


@app.route("/customers")
def customers():
    records = fetch_all("SELECT * FROM customers ORDER BY customer_id DESC")
    return render_template("customers.html", customers=records)


@app.route("/customers/new", methods=["GET", "POST"])
def create_customer():
    if request.method == "POST":
        execute(
            """
            INSERT INTO customers (name, email_id, phone_no, passkey, address)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                request.form["name"],
                request.form["email_id"],
                request.form["phone_no"],
                request.form["passkey"],
                request.form["address"],
            ),
        )
        flash("Customer added successfully.", "success")
        return redirect(url_for("customers"))
    return render_template("customer_form.html", customer=None)


@app.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def edit_customer(customer_id):
    customer = fetch_one("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    if not customer:
        flash("Customer not found.", "warning")
        return redirect(url_for("customers"))

    if request.method == "POST":
        execute(
            """
            UPDATE customers
            SET name = %s, email_id = %s, phone_no = %s, passkey = %s, address = %s
            WHERE customer_id = %s
            """,
            (
                request.form["name"],
                request.form["email_id"],
                request.form["phone_no"],
                request.form["passkey"],
                request.form["address"],
                customer_id,
            ),
        )
        flash("Customer updated successfully.", "success")
        return redirect(url_for("customers"))
    return render_template("customer_form.html", customer=customer)


@app.route("/customers/<int:customer_id>/delete", methods=["POST"])
def delete_customer(customer_id):
    execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    flash("Customer deleted successfully.", "success")
    return redirect(url_for("customers"))


@app.route("/rooms")
def rooms():
    records = fetch_all("SELECT * FROM rooms ORDER BY room_number")
    return render_template("rooms.html", rooms=records)


@app.route("/rooms/new", methods=["GET", "POST"])
def create_room():
    if request.method == "POST":
        execute(
            """
            INSERT INTO rooms (room_number, room_type, price_per_night, status)
            VALUES (%s, %s, %s, %s)
            """,
            (
                request.form["room_number"],
                request.form["room_type"],
                request.form["price_per_night"],
                request.form["status"],
            ),
        )
        flash("Room added successfully.", "success")
        return redirect(url_for("rooms"))
    return render_template("room_form.html", room=None, statuses=ROOM_STATUSES)


@app.route("/rooms/<int:room_id>/edit", methods=["GET", "POST"])
def edit_room(room_id):
    room = fetch_one("SELECT * FROM rooms WHERE room_id = %s", (room_id,))
    if not room:
        flash("Room not found.", "warning")
        return redirect(url_for("rooms"))

    if request.method == "POST":
        execute(
            """
            UPDATE rooms
            SET room_number = %s, room_type = %s, price_per_night = %s, status = %s
            WHERE room_id = %s
            """,
            (
                request.form["room_number"],
                request.form["room_type"],
                request.form["price_per_night"],
                request.form["status"],
                room_id,
            ),
        )
        flash("Room updated successfully.", "success")
        return redirect(url_for("rooms"))
    return render_template("room_form.html", room=room, statuses=ROOM_STATUSES)


@app.route("/rooms/<int:room_id>/delete", methods=["POST"])
def delete_room(room_id):
    execute("DELETE FROM rooms WHERE room_id = %s", (room_id,))
    flash("Room deleted successfully.", "success")
    return redirect(url_for("rooms"))


@app.route("/bookings")
def bookings():
    records = fetch_all(
        """
        SELECT b.*, c.name AS customer_name, r.room_number
        FROM bookings b
        JOIN customers c ON c.customer_id = b.customer_id
        JOIN rooms r ON r.room_id = b.room_id
        ORDER BY b.booking_id DESC
        """
    )
    return render_template("bookings.html", bookings=records)


@app.route("/bookings/new", methods=["GET", "POST"])
def create_booking():
    customers_list = fetch_all("SELECT customer_id, name FROM customers ORDER BY name")
    rooms_list = fetch_all("SELECT room_id, room_number FROM rooms ORDER BY room_number")

    if request.method == "POST":
        execute(
            """
            INSERT INTO bookings (customer_id, room_id, check_in, check_out, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                request.form["customer_id"],
                request.form["room_id"],
                request.form["check_in"],
                request.form["check_out"],
                request.form["status"],
            ),
        )
        flash("Booking created successfully.", "success")
        return redirect(url_for("bookings"))

    return render_template(
        "booking_form.html",
        booking=None,
        customers=customers_list,
        rooms=rooms_list,
        statuses=BOOKING_STATUSES,
        today=date.today().isoformat(),
    )


@app.route("/bookings/<int:booking_id>/edit", methods=["GET", "POST"])
def edit_booking(booking_id):
    booking = fetch_one("SELECT * FROM bookings WHERE booking_id = %s", (booking_id,))
    if not booking:
        flash("Booking not found.", "warning")
        return redirect(url_for("bookings"))

    customers_list = fetch_all("SELECT customer_id, name FROM customers ORDER BY name")
    rooms_list = fetch_all("SELECT room_id, room_number FROM rooms ORDER BY room_number")

    if request.method == "POST":
        execute(
            """
            UPDATE bookings
            SET customer_id = %s, room_id = %s, check_in = %s, check_out = %s, status = %s
            WHERE booking_id = %s
            """,
            (
                request.form["customer_id"],
                request.form["room_id"],
                request.form["check_in"],
                request.form["check_out"],
                request.form["status"],
                booking_id,
            ),
        )
        flash("Booking updated successfully.", "success")
        return redirect(url_for("bookings"))

    return render_template(
        "booking_form.html",
        booking=booking,
        customers=customers_list,
        rooms=rooms_list,
        statuses=BOOKING_STATUSES,
        today=date.today().isoformat(),
    )


@app.route("/bookings/<int:booking_id>/delete", methods=["POST"])
def delete_booking(booking_id):
    execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
    flash("Booking deleted successfully.", "success")
    return redirect(url_for("bookings"))


@app.route("/payments")
def payments():
    records = fetch_all(
        """
        SELECT p.*, c.name AS customer_name, r.room_number
        FROM payments p
        JOIN bookings b ON b.booking_id = p.booking_id
        JOIN customers c ON c.customer_id = b.customer_id
        JOIN rooms r ON r.room_id = b.room_id
        ORDER BY p.payment_id DESC
        """
    )
    return render_template("payments.html", payments=records)


@app.route("/payments/new", methods=["GET", "POST"])
def create_payment():
    booking_options = booking_select_options()
    if request.method == "POST":
        execute(
            """
            INSERT INTO payments (booking_id, amount, payment_date, payment_method, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                request.form["booking_id"],
                request.form["amount"],
                request.form["payment_date"],
                request.form["payment_method"],
                request.form["status"],
            ),
        )
        flash("Payment added successfully.", "success")
        return redirect(url_for("payments"))
    return render_template(
        "payment_form.html",
        payment=None,
        bookings=booking_options,
        methods=PAYMENT_METHODS,
        statuses=PAYMENT_STATUSES,
        today=date.today().isoformat(),
    )


@app.route("/payments/<int:payment_id>/edit", methods=["GET", "POST"])
def edit_payment(payment_id):
    payment = fetch_one("SELECT * FROM payments WHERE payment_id = %s", (payment_id,))
    if not payment:
        flash("Payment not found.", "warning")
        return redirect(url_for("payments"))

    if request.method == "POST":
        execute(
            """
            UPDATE payments
            SET booking_id = %s, amount = %s, payment_date = %s,
                payment_method = %s, status = %s
            WHERE payment_id = %s
            """,
            (
                request.form["booking_id"],
                request.form["amount"],
                request.form["payment_date"],
                request.form["payment_method"],
                request.form["status"],
                payment_id,
            ),
        )
        flash("Payment updated successfully.", "success")
        return redirect(url_for("payments"))

    return render_template(
        "payment_form.html",
        payment=payment,
        bookings=booking_select_options(),
        methods=PAYMENT_METHODS,
        statuses=PAYMENT_STATUSES,
        today=date.today().isoformat(),
    )


@app.route("/payments/<int:payment_id>/delete", methods=["POST"])
def delete_payment(payment_id):
    execute("DELETE FROM payments WHERE payment_id = %s", (payment_id,))
    flash("Payment deleted successfully.", "success")
    return redirect(url_for("payments"))


def booking_select_options():
    return fetch_all(
        """
        SELECT b.booking_id, c.name AS customer_name, r.room_number,
               b.check_in, b.check_out
        FROM bookings b
        JOIN customers c ON c.customer_id = b.customer_id
        JOIN rooms r ON r.room_id = b.room_id
        ORDER BY b.booking_id DESC
        """
    )


if __name__ == "__main__":
    app.run(debug=True)
