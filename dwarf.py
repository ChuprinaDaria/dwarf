import stripe
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# Налаштування Stripe API
stripe.api_key = "sk_test_111111111111"  # Замініть на ваш Stripe Secret Key
# Налаштування логування
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Список тарифів
TARIFFS = {
    "Month - 100 UAH": 100,
    "Six months - 500 UAH": 500,
    "Year - 900 UAH": 900,
}

# Зберігання даних користувачів
users = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot. Type /help to see what I can do!")


# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Command list:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/registration - Register in the system\n"
        "/tariffs - View tariffs and subscribe\n"
        "/payment - Complete your subscription"
    )


# Команда /registration
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in users:
        await update.message.reply_text("You are already registered!")
    else:
        users[user_id] = {"status": "Inactive", "tariff": None, "payment_status": False}
        await update.message.reply_text(
            "You have been successfully registered! Now you can view tariffs using the /tariffs command."
        )


# Команда /tariffs
async def tariffs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[tariff] for tariff in TARIFFS.keys()]  # Кнопки з тарифами
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Choose a tariff:", reply_markup=reply_markup)


# Обробка вибору тарифу
async def choose_tariff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Перевірка, чи користувач зареєстрований
    if user_id not in users:
        await update.message.reply_text("Please register first using the /registration command.")
        return

    tariff = update.message.text

    if tariff in TARIFFS:
        users[user_id]["tariff"] = tariff
        await update.message.reply_text(
            f"You have selected the tariff: {tariff}. To complete the subscription, type /payment"
        )
    else:
        await update.message.reply_text("Choose one of the suggested tariffs!")


# Створення Stripe Payment Session
def create_stripe_session(tariff, price, user_id):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": tariff,
                        },
                        "unit_amount": int(price * 100),  # Stripe використовує центи
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="https://uk.wikipedia.org/wiki/%D0%91%D0%B0%D0%BD%D0%B4%D0%B5%D1%80%D0%B0_%D0%A1%D1%82%D0%B5%D0%BF%D0%B0%D0%BD_%D0%90%D0%BD%D0%B4%D1%80%D1%96%D0%B9%D0%BE%D0%B2%D0%B8%D1%87",  # Замініть на свій success URL
            cancel_url="https://uk.wikipedia.org/wiki/%D0%9F%D1%83%D1%82%D1%96%D0%BD_%D0%92%D0%BE%D0%BB%D0%BE%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%92%D0%BE%D0%BB%D0%BE%D0%B4%D0%B8%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B8%D1%87",  # Замініть на свій cancel URL
        )
        return session.url
    except Exception as e:
        logger.error(f"Error creating Stripe session: {e}")
        return None


# Команда /payment
async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = users.get(user_id)

    if not user_data or not user_data.get("tariff"):
        await update.message.reply_text("First select a tariff using the /tariffs command.")
        return

    tariff = user_data["tariff"]
    price = TARIFFS[tariff]

    # Створення Stripe-сесії
    payment_link = create_stripe_session(tariff, price, user_id)
    if payment_link:
        await update.message.reply_text(
            f"To complete your subscription, please pay {price} USD using the following link: {payment_link}"
        )
    else:
        await update.message.reply_text("An error occurred while creating the payment session. Please try again.")


if __name__ == "__main__":
    # Ініціалізація бота
    app = ApplicationBuilder().token("11111111111").build()

    # Додавання обробників команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("registration", register))
    app.add_handler(CommandHandler("tariffs", tariffs))
    app.add_handler(CommandHandler("payment", payment))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, choose_tariff))  # Обробка тексту (вибір тарифу)

    print("Bot is running...")
    app.run_polling()
