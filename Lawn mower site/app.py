from flask import Flask, render_template_string, request, redirect, url_for
import requests

app = Flask(__name__)

# Your Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1366259731509022730/UwDXjhrv2sh4h4gPxCi6LhpVMo0AdMFGJJDcDK0SuDrC3vaUyGUC48umbhIoJr8ie7az"

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lil' Legend Lawns</title>
        <link rel="icon" href="{{ url_for('static', filename='icon.png') }}" type="image/png">
        <style>
            /* Your CSS (unchanged) */
        </style>
    </head>
    <body>
        <!-- Sections (unchanged) -->
        <section id="landing">
            <h1>Lil' Legend Lawns</h1>
            <p>We make your lawn look legendary!</p>
            <a href="#booking" class="button">Book the Mow</a>
            <img id="mower" src="/static/mower.png" alt="Mower" class="mower">
        </section>

        <section id="booking">
            <h2>Book Your Lawn Mowing</h2>
            <form class="booking-form" action="{{ url_for('book') }}" method="POST">
                <input class="form-input" type="text" name="name" placeholder="Your Name" required>
                <input class="form-input" type="text" name="address" placeholder="Your Address (Waratah or Georgetown)" required>
                <input class="form-input" type="date" name="date" required>
                <textarea class="form-input" name="note" placeholder="Additional Note (optional)" rows="4"></textarea>
                <input class="form-input" type="submit" value="Book Now">
            </form>
        </section>

        <section id="about">
            <h2>About Me</h2>
            <p>Hi! I'm a young lawn mowing enthusiast based in Waratah and Georgetown. I started this business to help keep your lawns looking fresh and tidy!</p>
        </section>

        <section id="pricing">
            <h2>Pricing</h2>
            <div class="pricing-item">Basic Lawn Mowing: $30</div>
            <div class="pricing-item">Lawn Care (Mowing + Edging): $45</div>
        </section>
    </body>
    </html>
    """)

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name', 'Unknown')
    address = request.form.get('address', 'Unknown')
    date = request.form.get('date', 'Unknown')
    note = request.form.get('note') or "No note provided."

    # Log for dev
    print(f"[NEW BOOKING] Name: {name}, Address: {address}, Date: {date}, Note: {note}")

    # Send to Discord
    success = send_discord_notification(name, address, date, note)

    if not success:
        return "Failed to send booking to Discord. Try again later.", 500

    return redirect(url_for('home'))

def send_discord_notification(name, address, date, note):
    payload = {
        "content": f"**📋 New Lawn Booking!**\n\n"
                   f"**Name:** {name}\n"
                   f"**Address:** {address}\n"
                   f"**Date:** {date}\n"
                   f"**Note:** {note}"
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)
        if response.status_code in [200, 204]:
            print("[SUCCESS] Sent booking to Discord.")
            return True
        else:
            print(f"[ERROR] Discord webhook failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[EXCEPTION] Discord webhook crash: {str(e)}")
        return False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
