import logging
from typing import Dict, List
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from openai import OpenAI

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("נא להגדיר TELEGRAM_TOKEN ו-OPENAI_API_KEY בקובץ .env")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


class UserWarningTracker:
    def __init__(self):
        self.warnings: Dict[int, List[datetime]] = {}
        self.warning_threshold = 3
        self.warning_window = timedelta(hours=24)

    def add_warning(self, user_id: int) -> int:
        current_time = datetime.now()
        if user_id not in self.warnings:
            self.warnings[user_id] = []

        self.warnings[user_id] = [
            time for time in self.warnings[user_id]
            if current_time - time <= self.warning_window
        ]

        self.warnings[user_id].append(current_time)
        return len(self.warnings[user_id])


warning_tracker = UserWarningTracker()


async def analyze_message(text: str) -> tuple[bool, str]:
    """
    בדיקת הודעה לתוכן פוגעני
    מחזיר: (האם_פוגעני, הסבר)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                תפקידך לנתח הודעות ולזהות תוכן פוגעני או בריונות.
                עליך להחזיר תשובה במבנה JSON הבא:
                {
                    "is_offensive": true/false,
                    "explanation": "הסבר מדוע ההודעה פוגענית או לא"
                }

                הודעה נחשבת פוגענית אם היא כוללת:
                - קללות
                - שפה פוגענית
                - איומים
                - הטרדה
                - לעג
                - קריאה לחרם
                - פגיעה ברגשות
                """},
                {"role": "user", "content": text}
            ],
            max_tokens=200,
            temperature=0.3
        )

        try:
            result = json.loads(response.choices[0].message.content)
            return result["is_offensive"], result["explanation"]
        except json.JSONDecodeError:
            # במקרה שהתגובה אינה JSON תקין
            content = response.choices[0].message.content
            is_offensive = "פוגעני" in content or "בריונות" in content
            return is_offensive, content

    except Exception as e:
        logger.error(f"שגיאה בניתוח ההודעה: {str(e)}")
        return False, ""


async def send_warning(context: ContextTypes.DEFAULT_TYPE, user_id: int, explanation: str):
    """שליחת אזהרה למשתמש"""
    warning = f"""
⚠️ שלום,

זיהינו תוכן פוגעני בהודעה שלך:
{explanation}

חשוב לזכור:
• מילים יכולות לפגוע
• לכל אדם יש רגשות
• אפשר להביע דעה בצורה מכבדת

אנא הימנע משימוש בשפה פוגענית.
    """
    try:
        await context.bot.send_message(chat_id=user_id, text=warning)
    except Exception as e:
        logger.error(f"שגיאה בשליחת אזהרה: {str(e)}")


async def notify_admin(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user_id: int, warning_count: int):
    """עדכון מנהל הקבוצה"""
    try:
        admins = await context.bot.get_chat_administrators(chat_id)
        message = f"""
⚠️ התראת מנהל:

משתמש קיבל {warning_count} אזהרות על תוכן פוגעני.
מזהה משתמש: {user_id}

המלצה: {'להרחיק מהקבוצה' if warning_count >= 3 else 'לשוחח עם המשתמש'}
        """

        for admin in admins:
            if admin.user.is_bot:
                continue
            await context.bot.send_message(chat_id=admin.user.id, text=message)
    except Exception as e:
        logger.error(f"שגיאה בשליחת התראה למנהל: {str(e)}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """טיפול בהודעות נכנסות"""
    if not update.message or not update.message.text:
        return

    try:
        # בדיקת ההודעה
        is_offensive, explanation = await analyze_message(update.message.text)

        if is_offensive:
            user_id = update.message.from_user.id
            chat_id = update.message.chat_id

            # הוספת אזהרה
            warning_count = warning_tracker.add_warning(user_id)

            # שליחת אזהרה פרטית
            await send_warning(context, user_id, explanation)

            # עדכון מנהל במקרה הצורך
            if warning_count >= 2:
                await notify_admin(context, chat_id, user_id, warning_count)

    except Exception as e:
        logger.error(f"שגיאה בטיפול בהודעה: {str(e)}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """פקודת התחלה"""
    message = """
👋 שלום! אני בוט למניעת בריונות ברשת.

אני עוזר לשמור על שיח מכבד בקבוצה.

פקודות:
/start - הודעת פתיחה
/help - עזרה
    """
    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """פקודת עזרה"""
    message = """
🤖 אני בוט שעוזר למנוע בריונות ברשת:

• מזהה תוכן פוגעני
• שולח אזהרות פרטיות
• מעדכן מנהלים במקרה הצורך

המטרה היא ליצור סביבה בטוחה ונעימה לכולם.
    """
    await update.message.reply_text(message)


def main():
    """הפעלת הבוט"""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("הבוט החל לפעול")
    application.run_polling()


if __name__ == '__main__':
    main()