from flask import Flask, render_template_string, request, redirect, url_for
import requests

app = Flask(__name__)

# Your Discord webhook URL
DISCORD_WEBHOOK_URL = ""https://discord.com/api/webhooks/1366259731509022730/UwDXjhrv2sh4h4gPxCi6LhpVMo0AdMFGJJDcDK0SuDrC3vaUyGUC48umbhIoJr8ie7az"

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
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Arial', sans-serif; overflow-x: hidden; }

            section {
                height: 100vh;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                color: white;
                text-align: center;
                padding: 0 20px;
            }

            #landing {
                position: relative;
                background-image: url("/static/long-grass.png");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                padding-top: 100px;
                overflow: hidden;
                transition: background-image 1s ease-in-out;
            }

            h1 { font-size: 3.5em; margin-bottom: 20px; }
            p { font-size: 1.5em; margin-bottom: 30px; }

            .button {
                background-color: #4CAF50;
                padding: 15px 30px;
                font-size: 1.2em;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                transition: background-color 0.3s;
            }
            .button:hover { background-color: #45a049; }

            #booking { background-color: #2b8b47; padding: 40px 20px; border-radius: 10px; }
            .form-input {
                margin-bottom: 15px;
                padding: 12px;
                width: 80%;
                max-width: 600px;
                border-radius: 5px;
                font-size: 1em;
                border: none;
            }
            .form-input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }
            .form-input[type="submit"]:hover { background-color: #45a049; }

            #about { background-color: #2f2f2f; padding: 40px 20px; }
            #pricing { background-color: #4CAF50; padding: 40px 20px; }

            .pricing-item { font-size: 1.2em; margin: 10px 0; }

            html { scroll-behavior: smooth; }

            #mower {
                position: absolute;
                top: 40%;
                left: -250px;
                transition: left 4s linear;
                z-index: 1;
                width: 200px;
                height: auto;
                animation: moveMower 6s linear infinite;
            }

            @keyframes moveMower {
                0% { left: -250px; transform: scale(1.5); }
                50% { left: 100%; transform: scale(2); }
                100% { left: -250px; transform: scale(1.5); }
            }

            #mower.shortgrass {
                content: url("/static/shortgrass.png");
            }
        </style>
    </head>

    <body>
        <!-- Landing Section -->
        <section id="landing">
            <h1>Lil' Legend Lawns</h1>
            <p>We make your lawn look legendary!</p>
            <a href="#booking" class="button">Book the Mow</a>
            <img id="mower" src="/static/mower.png" alt="Mower" class="mower">
        </section>

        <!-- Booking Section -->
        <section id="booking">
            <h2>Book Your Lawn Mowing</h2>
            <form class="booking-form" action="/book" method="POST">
                <input class="form-input" type="text" name="name" placeholder="Your Name" required>
                <input class="form-input" type="text" name="address" placeholder="Your Address (Waratah or Georgetown)" required>
                <input class="form-input" type="date" name="date" required>
                <textarea class="form-input" name="note" placeholder="Additional Note (optional)" rows="4"></textarea>
                <input class="form-input" type="submit" value="Book Now">
            </form>
        </section>

        <!-- About Section -->
        <section id="about">
            <h2>About Me</h2>
            <p>Hi! I'm a young lawn mowing enthusiast based in Waratah and Georgetown. I started this business to help keep your lawns looking fresh and tidy!</p>
        </section>

        <!-- Pricing Section -->
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
    name = request.form.get('name')
    address = request.form.get('address')
    date = request.form.get('date')
    note = request.form.get('note') or "No note provided."

    # Print it in console (for devs)
    print(f"New Booking: {name}, {address}, {date}, Note: {note}")

    # Send Discord Notification
    send_discord_notification(name, address, date, note)

    return redirect(url_for('home'))

def send_discord_notification(name, address, date, note):
    data = {
        "content": f"**New Booking!** 🚀\n\n**Name:** {name}\n**Address:** {address}\n**Date:** {date}\n**Note:** {note}"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"Failed to send Discord notification: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error sending Discord notification: {e}")

if __name__ == "__main__":
    app.run(debug=True)
