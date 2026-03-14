"""
BookMyShow - Flask Application v1
Task 1: Baseline Single VM
GCP Project: upgradlabs-1749732686213
"""

from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

# ── In-Memory Data (no database in Task 1) ─────────────────────────────────
events = [
    {"id": 1, "name": "Coldplay: Music of the Spheres", "venue": "DY Patil Stadium", "city": "Mumbai", "price": 4500, "seats_available": 1240},
    {"id": 2, "name": "Kapil Sharma Live: Comedy Night", "venue": "JN Stadium",       "city": "Delhi",  "price": 1200, "seats_available": 580},
    {"id": 3, "name": "Contemporary Art Exhibition",     "venue": "NGMA Bangalore",    "city": "Bangalore", "price": 800, "seats_available": 320},
]

bookings = []


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/health/ready")
def health():
    """Health check endpoint used by Load Balancer probes."""
    return jsonify({"status": "ok", "service": "bms-api"}), 200


@app.route("/api/events")
def get_events():
    """Return all events. Simulates DB read latency."""
    time.sleep(random.uniform(0.05, 0.15))   # simulate DB latency
    return jsonify({"events": events, "count": len(events)}), 200


@app.route("/api/events/<int:event_id>/seats")
def get_seats(event_id):
    """Return seat availability for an event."""
    time.sleep(random.uniform(0.03, 0.10))
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({
        "event_id":        event_id,
        "event_name":      event["name"],
        "seats_available": event["seats_available"],
        "price":           event["price"]
    }), 200


@app.route("/api/bookings", methods=["POST"])
def create_booking():
    """Create a booking. Simulates DB write latency."""
    time.sleep(random.uniform(0.10, 0.25))   # simulate write latency

    data = request.get_json()
    if not data or not all(k in data for k in ["user_id", "event_id", "seats"]):
        return jsonify({"error": "Missing required fields: user_id, event_id, seats"}), 400

    event = next((e for e in events if e["id"] == data["event_id"]), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    if data["seats"] > event["seats_available"]:
        return jsonify({"error": "Not enough seats available"}), 409

    # Reduce seat count (in-memory — resets on restart)
    event["seats_available"] -= data["seats"]

    booking = {
        "booking_id": len(bookings) + 1,
        "user_id":    data["user_id"],
        "event_id":   data["event_id"],
        "event_name": event["name"],
        "seats":      data["seats"],
        "total":      data["seats"] * event["price"],
        "status":     "confirmed"
    }
    bookings.append(booking)

    return jsonify(booking), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
