"""
BookMyShow - Flask Application v2
Task 3: Cloud SQL with Read/Write Split

Routing logic:
  SELECT queries  --> Replica  (34.47.176.241) -- reads
  INSERT/UPDATE   --> Primary  (34.180.32.191) -- writes

GCP Project: upgradlabs-1749732686213
"""

from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# ── Database Config ───────────────────────────────────────────────────────────
DB_CONFIG = {
    "PRIMARY": {
        "host":     os.environ.get("DB_PRIMARY_HOST", "34.180.32.191"),
        "user":     os.environ.get("DB_USER",         "root"),
        "password": os.environ.get("DB_PASSWORD",     "BmsSecure123!"),
        "database": "bookmyshow",
        "port":     3306,
    },
    "REPLICA": {
        "host":     os.environ.get("DB_REPLICA_HOST", "34.47.176.241"),
        "user":     os.environ.get("DB_USER",         "root"),
        "password": os.environ.get("DB_PASSWORD",     "BmsSecure123!"),
        "database": "bookmyshow",
        "port":     3306,
    }
}


def get_conn(write=False):
    """
    Return a database connection.
    write=True  --> PRIMARY (handles INSERT, UPDATE, DELETE)
    write=False --> REPLICA (handles SELECT — read-only)

    This splits DB load so the primary only receives ~20% of queries.
    """
    config = DB_CONFIG["PRIMARY"] if write else DB_CONFIG["REPLICA"]
    return mysql.connector.connect(**config)


# ── Health Check ─────────────────────────────────────────────────────────────
@app.route("/health/ready")
def health():
    """
    Deep health check used by Load Balancer (every 10 seconds).
    Tests actual DB connectivity — not just 'is Flask running'.
    After 3 failures (30s), VM is removed from LB and replaced.
    """
    try:
        conn = get_conn(write=False)
        conn.ping(reconnect=True)
        conn.close()
        return jsonify({"status": "ok", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "db": str(e)}), 503


# ── Events ────────────────────────────────────────────────────────────────────
@app.route("/api/events")
def get_events():
    """
    Returns all events.
    READ --> goes to REPLICA (34.47.176.241)
    """
    conn   = get_conn(write=False)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events ORDER BY event_date")
    events = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert Decimal to float for JSON serialisation
    for e in events:
        e["price"] = float(e["price"])

    return jsonify({"events": events, "count": len(events)}), 200


# ── Seat Availability ─────────────────────────────────────────────────────────
@app.route("/api/events/<int:event_id>/seats")
def get_seats(event_id):
    """
    Returns seat availability for one event.
    READ --> goes to REPLICA (34.47.176.241)
    """
    conn   = get_conn(write=False)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name, seats_available, price FROM events WHERE id = %s",
        (event_id,)
    )
    event = cursor.fetchone()
    cursor.close()
    conn.close()

    if not event:
        return jsonify({"error": "Event not found"}), 404

    event["price"] = float(event["price"])
    return jsonify(event), 200


# ── Create Booking ────────────────────────────────────────────────────────────
@app.route("/api/bookings", methods=["POST"])
def create_booking():
    """
    Creates a new booking.
    WRITE --> goes to PRIMARY (34.180.32.191)

    Steps:
    1. Validate request body
    2. Check event exists (read replica)
    3. Check seat availability (read replica)
    4. Write booking to PRIMARY
    5. Decrement seats_available on PRIMARY
    """
    data = request.get_json()
    if not data or not all(k in data for k in ["user_id", "event_id", "seats"]):
        return jsonify({"error": "Missing required fields: user_id, event_id, seats"}), 400

    # Step 1: Read event from replica
    read_conn   = get_conn(write=False)
    read_cursor = read_conn.cursor(dictionary=True)
    read_cursor.execute(
        "SELECT id, name, seats_available, price FROM events WHERE id = %s",
        (data["event_id"],)
    )
    event = read_cursor.fetchone()
    read_cursor.close()
    read_conn.close()

    if not event:
        return jsonify({"error": "Event not found"}), 404

    if data["seats"] > event["seats_available"]:
        return jsonify({"error": "Not enough seats available"}), 409

    # Step 2: Write booking to primary
    total = data["seats"] * float(event["price"])

    write_conn   = get_conn(write=True)
    write_cursor = write_conn.cursor()

    write_cursor.execute(
        "INSERT INTO bookings (user_id, event_id, seats, total_amount, status) VALUES (%s, %s, %s, %s, 'confirmed')",
        (data["user_id"], data["event_id"], data["seats"], total)
    )
    booking_id = write_cursor.lastrowid

    # Step 3: Decrement seat count on primary
    write_cursor.execute(
        "UPDATE events SET seats_available = seats_available - %s WHERE id = %s",
        (data["seats"], data["event_id"])
    )

    write_conn.commit()
    write_cursor.close()
    write_conn.close()

    return jsonify({
        "booking_id": booking_id,
        "user_id":    data["user_id"],
        "event_id":   data["event_id"],
        "event_name": event["name"],
        "seats":      data["seats"],
        "total":      total,
        "status":     "confirmed"
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
