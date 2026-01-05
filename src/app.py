from flask import Flask, jsonify, request
import os
from pathlib import Path

COUNTER_PATH = Path(os.getenv("COUNTER_PATH", "/data/counter.txt"))
app = Flask(__name__)

# ---------- Helpers ----------

def read_counter() -> int:
    """Read counter from file; if missing or invalid, treat as 0."""
    try:
        if not COUNTER_PATH.exists():
            return 0

        content = COUNTER_PATH.read_text().strip()
        return int(content) if content else 0

    except ValueError:
        return 0


def write_counter(value: int) -> None:
    COUNTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    COUNTER_PATH.write_text(str(value))


def inc_and_get() -> int:
    current = read_counter()
    new_value = current + 1
    write_counter(new_value)
    return new_value


# ---------- Routes ----------
@app.route("/")
def root():
    """
    Main page: increment the counter for each visit
    and return the new value.
    """
    new_value = inc_and_get()
    return jsonify({
        "message": "Welcome to the Counter API",
        "counter": new_value,
    })


@app.route("/count", methods=["GET"])
def counter():
    """
    Return the current counter value without changing it
    """
    value = read_counter()
    return jsonify({"counter": value})


@app.route("/inc", methods=["POST"])
def inc_counter():
    """
    Explicit increment endpoint (POST).
    """
    new_value = inc_and_get()
    return jsonify({"counter": new_value})


@app.route("/healthz", methods=["GET"])
def healthz():
    """
    Liveness probe: if this response 200, the process is alive
    """
    return jsonify({"status": "ok"}), 200


@app.route("/readyz", methods=["GET"])
def readyz():
    """
    Readiness probe: checks whether the app is actually able
    to use the counter file configured by COUNTER_PATH.

    If we can't read OR create/update the file, we return 503,
    so Kubernetes will stop sending traffic to this pod.
    """
    try:
        # Can we read?
        _ = read_counter()
        # Can we write?
        write_counter(read_counter())
        return jsonify({"ready": True}), 200
    except Exception as e:
        return jsonify({
            "ready": False,
            "error": str(e),
            "counter_path": str(COUNTER_PATH),
        }), 503


@app.route("/admin/reset", methods=["POST"])
def admin_reset():
    """
    Admin-only endpoint: resets the counter back to 0.
    Requires header:
      X-Admin-Token: <token>
    The valid token is provided via the ADMIN_TOKEN environment variable.
    """
    token = request.headers.get("X-Admin-Token")
    admin_token = os.getenv("ADMIN_TOKEN")

    if not admin_token or admin_token != token:
        return jsonify({"error": "unauthorized"}), 401

    write_counter(0)
    return jsonify({"message": "counter reset"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)