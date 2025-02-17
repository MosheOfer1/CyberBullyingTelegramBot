# 🤖 בוט טלגרם למניעת בריונות ברשת

בוט טלגרם המיועד לזהות ולמנוע בריונות ברשת בקבוצות. הבוט משתמש ב-OpenAI API לניתוח הודעות וזיהוי תוכן פוגעני.

## 📋 תכונות עיקריות

- זיהוי אוטומטי של תוכן פוגעני
- שליחת אזהרות פרטיות למשתמשים
- מעקב אחר התנהגות חוזרת
- התראות למנהלי קבוצות
- תמיכה מלאה בעברית

## 🛠 דרישות מערכת

- Python 3.8 ומעלה
- חשבון טלגרם
- מפתח API של OpenAI
- טוקן של בוט טלגרם BotFather

## ⚙️ התקנה

1. שכפל את המאגר:
```bash
git clone https://github.com/your-username/telegram-cyberbully-bot.git
cd telegram-cyberbully-bot
```

2. צור סביבה וירטואלית והפעל אותה:
```bash
python -m venv venv
# ב-Windows:
venv\Scripts\activate
# ב-Linux/Mac:
source venv/bin/activate
```

3. התקן את החבילות הנדרשות:
```bash
pip install -r requirements.txt
```

4. צור קובץ `.env` והוסף את המפתחות הנדרשים:
```
TELEGRAM_TOKEN=your_telegram_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 הפעלה

להפעלת הבוט:
```bash
python bot.py
```

## 🔍 כיצד זה עובד

1. **ניטור הודעות**:
   - הבוט מנטר את כל ההודעות בקבוצה
   - מנתח כל הודעה באמצעות OpenAI API

2. **זיהוי תוכן פוגעני**:
   - קללות
   - שפה פוגענית
   - איומים
   - הטרדה
   - לעג
   - קריאה לחרם

3. **מערכת אזהרות**:
   - אזהרה ראשונה: הודעה פרטית למשתמש
   - אזהרה שנייה: התראה למנהלי הקבוצה
   - אזהרה שלישית: המלצה להרחקה מהקבוצה

## ⚠️ מערכת האזהרות

הבוט מנהל מערכת אזהרות מדורגת:

1. **אזהרה ראשונה**:
   - שליחת הודעה פרטית למשתמש
   - הסבר על הבעייתיות בתוכן

2. **אזהרה שנייה**:
   - הודעה נוספת למשתמש
   - עדכון מנהלי הקבוצה

3. **אזהרה שלישית**:
   - המלצה למנהלים להרחיק את המשתמש
   - תיעוד מלא של ההפרות

## 👥 תפקידי מנהל

מנהלי הקבוצה מקבלים:
- התראות על משתמשים בעייתיים
- סטטיסטיקות שימוש
- המלצות לפעולה

## 📊 מעקב ותיעוד

הבוט מנהל מעקב אחר:
- מספר האזהרות לכל משתמש
- סוגי ההפרות
- זמני ההפרות

## 🔒 פרטיות ואבטחה

- כל התקשורת עם OpenAI מוצפנת
- מידע רגיש נשמר בזיכרון בלבד
- לא נשמר מידע מזהה של משתמשים

## 🤝 תרומה לפרויקט

נשמח לקבל תרומות לפרויקט! אנא:
1. צרו fork למאגר
2. צרו branch חדש לתכונה
3. העלו pull request

## 📄 רישיון

מופץ תחת רישיון MIT. ראה קובץ `LICENSE` למידע נוסף.
