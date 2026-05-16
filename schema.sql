CREATE DATABASE IF NOT EXISTS hotel_management;
USE hotel_management;

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email_id VARCHAR(120) NOT NULL UNIQUE,
    phone_no VARCHAR(20) NOT NULL,
    passkey VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    room_type VARCHAR(50) NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    status ENUM('Available', 'Occupied', 'Maintenance') NOT NULL DEFAULT 'Available'
);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    room_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    status ENUM('Booked', 'Checked In', 'Checked Out', 'Cancelled') NOT NULL DEFAULT 'Booked',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bookings_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_bookings_room
        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
        ON DELETE CASCADE,
    CONSTRAINT chk_booking_dates CHECK (check_out >= check_in)
);

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('Cash', 'Card', 'UPI', 'Net Banking') NOT NULL,
    status ENUM('Pending', 'Paid', 'Refunded') NOT NULL DEFAULT 'Pending',
    CONSTRAINT fk_payments_booking
        FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
        ON DELETE CASCADE
);

INSERT INTO customers (name, email_id, phone_no, passkey, address) VALUES
('Smriti', 'smriti@example.com', '7795884780', 'sm04', 'Bangalore'),
('Rohit', 'rohit@example.com', '9591625019', 'rohit1', 'Montreal'),
('Anvi', 'anvi@example.com', '8073465065', 'anvi05', 'Bangalore');

INSERT INTO rooms (room_number, room_type, price_per_night, status) VALUES
('101', 'Single', 1800.00, 'Available'),
('102', 'Double', 2800.00, 'Occupied'),
('201', 'Suite', 5200.00, 'Available');

INSERT INTO bookings (customer_id, room_id, check_in, check_out, status) VALUES
(1, 1, '2026-05-16', '2026-05-18', 'Booked'),
(2, 2, '2026-05-15', '2026-05-20', 'Checked In');

INSERT INTO payments (booking_id, amount, payment_date, payment_method, status) VALUES
(1, 3600.00, '2026-05-16', 'UPI', 'Paid'),
(2, 14000.00, '2026-05-15', 'Card', 'Pending');
