from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Your Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1337368742413209631/DTDRQWphimU8Fg6eCQne8GY5pYgAy3mAUX-D3KQQlHgII7bP1K5lxlXqQEZMZNlELeQJ"

@app.route("/")
def index():
    return render_template("contact-us.html")

@app.route("/send-to-discord", methods=["POST"])
def send_to_discord():
    # Collect form data
    username = request.form["username"]
    email = request.form["email"]
    message = request.form["message"]
    port_fw = request.form["portFw"]

    # Construct the message to send to Discord
    discord_message = {
        "content": f"New Contact Form Submission:\n\nUsername: {username}\nEmail: {email}\nMessage: {message}\nCan Port Forward: {port_fw}"
    }

    # Send the message to Discord via the webhook
    response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

    # Check if the message was sent successfully
    if response.status_code == 204:
        return "Your message has been sent successfully! We'll contact you soon."
    else:
        return "There was an error sending your message. Please try again later."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6006)  # Set port to 6005
