# Hotel Management System

A Flask and MySQL project that demonstrates database-focused CRUD operations for a hotel.

## Features

- Dashboard with total customers, rooms, bookings, and paid revenue.
- Customer CRUD: create, read, update, and delete customers.
- Room CRUD: manage room numbers, room types, prices, and status.
- Booking CRUD: connect customers to rooms with check-in/check-out dates.
- Payment CRUD: record payment amount, method, date, and status.
- MySQL schema with primary keys, foreign keys, constraints, and sample data.

## Setup

1. Create a virtual environment.

```bash
python -m venv .venv
```

2. Activate it on Windows PowerShell.

```bash
.venv\Scripts\Activate.ps1
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Import the database schema into MySQL.

```bash
mysql -h 127.0.0.1 -P 3307 -u root -p < schema.sql
```

5. Run the app.

```bash
python app.py
```

The app runs at `http://127.0.0.1:5000`.

## Database Configuration

By default the app uses:

- Host: `127.0.0.1`
- Port: `3307`
- User: `root`
- Password: set with `DB_PASSWORD`
- Database: `hotel_management`

You can override these with environment variables:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

Example for PowerShell:

```bash
$env:DB_PASSWORD="smriti"
$env:DB_PORT="3307"
python app.py

## Recent Update

- Created a new Git branch for learning Git workflow.
```
Learning Git - Authentication Branch