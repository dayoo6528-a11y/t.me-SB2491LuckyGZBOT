import logging
import os
import random

from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ---------------------------------------------------------------------------
# Content (all harmless, no gambling, no prizes)
# ---------------------------------------------------------------------------

FACTS = [
    "Honey never spoils. Edible honey has been found in ancient Egyptian tombs.",
    "Octopuses have three hearts and blue blood.",
    "Bananas are berries, but strawberries are not.",
    "A day on Venus is longer than a year on Venus.",
    "Sharks existed before trees did.",
    "The Eiffel Tower can grow about 15 cm taller in summer because of heat.",
    "Wombat droppings are cube-shaped.",
    "Your brain uses about 20% of your body's energy.",
    "There are more stars in the universe than grains of sand on Earth.",
    "Sound travels about four times faster in water than in air.",
]

JOKES = [
    "Why don't programmers like nature? It has too many bugs.",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "I told my computer I needed a break. Now it won't stop sending me vacation ads.",
    "Why do Java developers wear glasses? Because they can't C#.",
    "What do you call fake spaghetti? An impasta.",
    "Why did the bicycle fall over? It was two-tired.",
    "I would tell you a UDP joke, but you might not get it.",
]

QUOTES = [
    "The best way to get started is to quit talking and begin doing. - Walt Disney",
    "It always seems impossible until it's done. - Nelson Mandela",
    "Well done is better than well said. - Benjamin Franklin",
    "Whether you think you can or you think you can't, you're right. - Henry Ford",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Small steps every day lead to big results.",
]

TRIVIA = [
    {
        "q": "What is the capital of Japan?",
        "options": ["Seoul", "Tokyo", "Beijing", "Bangkok"],
        "answer": 1,
    },
    {
        "q": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Jupiter", "Mars", "Mercury"],
        "answer": 2,
    },
    {
        "q": "How many continents are there?",
        "options": ["5", "6", "7", "8"],
        "answer": 2,
    },
    {
        "q": "What gas do plants absorb from the air?",
        "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Helium"],
        "answer": 1,
    },
    {
        "q": "Which ocean is the largest?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": 3,
    },
]

# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------


def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🧠 Random Fact", callback_data="fact"),
            InlineKeyboardButton("😂 Joke", callback_data="joke"),
        ],
        [
            InlineKeyboardButton("💬 Quote", callback_data="quote"),
            InlineKeyboardButton("❓ Trivia", callback_data="trivia"),
        ],
        [
            InlineKeyboardButton("🪙 Coin Flip", callback_data="coin"),
            InlineKeyboardButton("🎲 Roll Dice", callback_data="dice"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def again_menu(action: str, label: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(f"🔁 {label}", callback_data=action)],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user.first_name if update.effective_user else "there"
    text = (
        f"Hi {name}! 👋\n\n"
        "I'm a fun little bot with facts, jokes, quotes, trivia and simple "
        "random tools. Pick something below:"
    )
    await update.message.reply_text(text, reply_markup=main_menu())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Here is what I can do:\n\n"
        "/start - Open the main menu\n"
        "/fact - Random fact\n"
        "/joke - Random joke\n"
        "/quote - Random quote\n"
        "/trivia - Trivia question\n"
        "/coin - Flip a coin\n"
        "/dice - Roll a dice\n"
        "/random 1 100 - Random number between two numbers\n"
        "/pick pizza, burger, sushi - Pick one option from your list\n"
        "/about - About this bot"
    )
    await update.message.reply_text(text)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "This is a free entertainment bot. It does not collect personal data "
        "and has nothing to do with gambling or prizes."
    )


async def fact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🧠 " + random.choice(FACTS), reply_markup=again_menu("fact", "Another fact")
    )


async def joke_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "😂 " + random.choice(JOKES), reply_markup=again_menu("joke", "Another joke")
    )


async def quote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💬 " + random.choice(QUOTES), reply_markup=again_menu("quote", "Another quote")
    )


async def coin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = random.choice(["Heads", "Tails"])
    await update.message.reply_text(
        f"🪙 {result}!", reply_markup=again_menu("coin", "Flip again")
    )


async def dice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🎲 You rolled a {random.randint(1, 6)}!",
        reply_markup=again_menu("dice", "Roll again"),
    )


async def trivia_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, markup = build_trivia()
    await update.message.reply_text(text, reply_markup=markup)


async def random_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        low, high = int(context.args[0]), int(context.args[1])
        if low > high:
            low, high = high, low
        await update.message.reply_text(f"🔢 {random.randint(low, high)}")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /random 1 100")


async def pick_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = " ".join(context.args)
    options = [o.strip() for o in raw.split(",") if o.strip()]
    if len(options) < 2:
        await update.message.reply_text("Usage: /pick pizza, burger, sushi")
        return
    await update.message.reply_text(f"👉 I pick: {random.choice(options)}")


# ---------------------------------------------------------------------------
# Trivia helpers
# ---------------------------------------------------------------------------


def build_trivia():
    qid = random.randrange(len(TRIVIA))
    item = TRIVIA[qid]
    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"ans:{qid}:{i}")]
        for i, opt in enumerate(item["options"])
    ]
    return f"❓ {item['q']}", InlineKeyboardMarkup(buttons)


# ---------------------------------------------------------------------------
# Button handler
# ---------------------------------------------------------------------------


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        await query.edit_message_text(
            "Pick something below:", reply_markup=main_menu()
        )
    elif data == "fact":
        await query.edit_message_text(
            "🧠 " + random.choice(FACTS),
            reply_markup=again_menu("fact", "Another fact"),
        )
    elif data == "joke":
        await query.edit_message_text(
            "😂 " + random.choice(JOKES),
            reply_markup=again_menu("joke", "Another joke"),
        )
    elif data == "quote":
        await query.edit_message_text(
            "💬 " + random.choice(QUOTES),
            reply_markup=again_menu("quote", "Another quote"),
        )
    elif data == "coin":
        await query.edit_message_text(
            f"🪙 {random.choice(['Heads', 'Tails'])}!",
            reply_markup=again_menu("coin", "Flip again"),
        )
    elif data == "dice":
        await query.edit_message_text(
            f"🎲 You rolled a {random.randint(1, 6)}!",
            reply_markup=again_menu("dice", "Roll again"),
        )
    elif data == "trivia":
        text, markup = build_trivia()
        await query.edit_message_text(text, reply_markup=markup)
    elif data.startswith("ans:"):
        _, qid, choice = data.split(":")
        item = TRIVIA[int(qid)]
        correct = item["answer"]
        if int(choice) == correct:
            result = "✅ Correct!"
        else:
            result = f"❌ Not quite. The answer is: {item['options'][correct]}"
        await query.edit_message_text(
            f"❓ {item['q']}\n\n{result}",
            reply_markup=again_menu("trivia", "Next question"),
        )


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Open the main menu"),
            BotCommand("fact", "Random fact"),
            BotCommand("joke", "Random joke"),
            BotCommand("quote", "Random quote"),
            BotCommand("trivia", "Trivia question"),
            BotCommand("coin", "Flip a coin"),
            BotCommand("dice", "Roll a dice"),
            BotCommand("random", "Random number: /random 1 100"),
            BotCommand("pick", "Pick one: /pick a, b, c"),
            BotCommand("help", "Show all commands"),
            BotCommand("about", "About this bot"),
        ]
    )


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set.")

    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("fact", fact_cmd))
    app.add_handler(CommandHandler("joke", joke_cmd))
    app.add_handler(CommandHandler("quote", quote_cmd))
    app.add_handler(CommandHandler("trivia", trivia_cmd))
    app.add_handler(CommandHandler("coin", coin_cmd))
    app.add_handler(CommandHandler("dice", dice_cmd))
    app.add_handler(CommandHandler("random", random_cmd))
    app.add_handler(CommandHandler("pick", pick_cmd))
    app.add_handler(CallbackQueryHandler(buttons))

    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
