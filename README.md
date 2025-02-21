💳 Telegram Subscription Bot with Stripe Integration
This Python-based Telegram bot allows users to subscribe to different tariff plans and complete payments securely using Stripe. The bot features an intuitive interface, enabling users to register, select subscription plans, and make payments directly through provided links.

🔍 Features
📋 User registration system
💰 View and select subscription tariffs:
Month - 100 UAH
Six months - 500 UAH
Year - 900 UAH
💳 Stripe integration for secure payments
📲 Telegram bot commands for easy interaction
📜 Logs all actions and errors for easier debugging
⚙️ How to Use
1️⃣ Install Required Libraries
Run the following command to install dependencies:

bash
Kopiuj
Edytuj
pip install python-telegram-bot stripe
2️⃣ Set Up API Keys
Replace the following placeholders in the script:

stripe.api_key: Replace with your Stripe Secret Key.
ApplicationBuilder().token(...): Replace with your Telegram Bot Token.
3️⃣ Run the Bot
Execute the script using Python:

bash
Kopiuj
Edytuj
python telegram_subscription_bot.py
💬 Available Commands
Command	Description
/start	Start the bot and receive a welcome message
/help	Get a list of available commands
/registration	Register a new user
/tariffs	View available subscription tariffs
/payment	Complete payment for the selected tariff
📚 Dependencies
python-telegram-bot – Telegram bot framework
stripe – For handling secure payments
logging – For logging activities and errors
🚀 Example Usage
User sends /registration to register.
Bot prompts the user to view available tariffs with /tariffs.
User selects a tariff from the provided list.
Bot generates a payment link through Stripe using /payment.
User completes the payment using the provided Stripe link.
💡 Notes
Make sure you replace the test API keys with live credentials when moving to production.
The bot uses Telegram polling, which should be replaced with webhooks for larger-scale deployments.
This bot is designed for demonstration and should be secured before going live.
🔒 Disclaimer
Do not share your Stripe Secret Key or Telegram Bot Token publicly. Always use secure environment variables to store sensitive information in production.

Let me know if you'd like me to help with setting up webhooks or deploying the bot on a server! 🚀
