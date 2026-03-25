# א"ל השד"ה — מחולל יחידות לימוד אוטומטי


## מה זה

מחולל מבוסס AI שיוצר **חומרי הוראה מוכנים להדפסה** בשיטת א"ל השד"ה —
שיטת למידה פעילה בתחנות המיושמת בבתי ספר בישראל.

קלט: נושא + מקצוע + כיתה.
פלט: קובץ PDF מלא לכל תחנה, לכל סבב, כולל מדריך למורה — מוכן להדפסה.

---

## שיטת א"ל השד"ה

ארבע תחנות עצמאיות — תלמיד יכול להתחיל בכל אחת:

| תחנה | תוכן | נוכחות מורה |
|------|------|-------------|
| **הבנה** | טקסט עשיר לקריאה + שאלות דיון בעל פה | רשות |
| **שיטות** | כתיבה מובנית ומדורגת לפי סוג הטקסט | חובה |
| **דיוק** | לשון ודקדוק: שורשים, בניינים, הכתבה, זמנים, גופים | רשות |
| **אוצר מילים** | חוויה ופעולה — מודפסת או פיזית | רשות |

---

## התקנה

```bash
cd alHasade
pip install -r requirements.txt
playwright install chromium
```

יש להעתיק את `.env.example` לקובץ `.env` ולמלא את מפתח ה-API:

```bash
cp .env.example .env
# ערוך את הקובץ — הוסף את GEMINI_API_KEY
```

---

## הרצה

```bash
# Windows — חשוב לתמיכה בעברית
python -X utf8 main.py
```

ערוך את `config.json` לבחירת הנושא:

```json
{
    "subject": "תנך",
    "topic": "שיבת ציון - ירמיה",
    "grade": "ח'",
    "rounds": 4
}
```

הפלט נשמר ב-`output/<נושא> <כיתה>/` — קובץ PDF אחד לכל סבב.

---

## מה מיוצר בכל סבב

לכל אחד מ-4 הסבבים מיוצרים הקבצים הבאים:

```
├── roadmap.html              — מפת יחידה למורה (פעם אחת לכל היחידה)
├── round{N}_comprehension    — תחנת הבנה
├── round{N}_methods          — תחנת שיטות
├── round{N}_precision        — תחנת דיוק
├── round{N}_vocabulary       — תחנת אוצר מילים
├── round{N}_teacher_prep     — הכנת המורה לסבב
└── round{N}_answer_key       — מחברת תשובות
```

---

## סוגי פעילות — תחנת אוצר מילים

**מודפסות:**
`matching_cards`, `sorting_table`, `dominoes`, `fill_in_poster`, `clothesline`, `idiom_cards`, `definition_table`, `crossword_mini`

**פיזיות/חווייתיות:**
`physical_plasticine` — פיסול מילים בפלסטלינה
`physical_model` — בניית מודל/דיאגרמה
`physical_game` — משחק קלפים/לוח/זיכרון
`physical_poster` — בניית כרזה ותערוכה
`physical_simulation` — משחק תפקידים וסימולציה
`physical_clothesline` — חבל כביסה

כל פעילות פיזית כוללת: רשימת חומרים, שלבי ביצוע ממוספרים, וקלפי מילים להדפסה וגזירה.

---

## סוגי כתיבה — תחנת שיטות

טיעון (בעד/נגד), תיאור, תשובה מיטבית, סיכום, מיזוג, חוות דעת, דוח, מכתב, שיר קצר, יומן אישי, ניתוח טקסט מידעי, תרשים זרימה.

מדרג קושי בכל שיעור — ירוק/צהוב/אדום.

---

## ספק ה-LLM

המערכת תומכת בשני ספקים — ניתן לשינוי ב-`.env`:

```env
# Gemini (ברירת מחדל — מומלץ לפרודקשן)
LLM_PROVIDER=gemini
GEMINI_API_KEY=...

# NVIDIA (לבדיקות — gpt-oss-20b, מודל reasoning)
LLM_PROVIDER=nvidia
NVIDIA_API_KEY=...
NVIDIA_MODEL=openai/gpt-oss-20b
```

מומלץ: **Gemini Flash** — מהיר, זול, עברית מעולה.

---

## מבנה הקוד

```
alHasade/
├── main.py               — נקודת כניסה
├── config.json           — הגדרות נושא
├── .env                  — מפתחות API
├── requirements.txt
└── src/
    ├── pipeline.py       — תזמור הזרימה הראשית
    ├── prompts.py        — כל ה-prompt engineering
    ├── gemini.py         — שכבת LLM (Gemini + NVIDIA)
    ├── renderers.py      — HTML → עיצוב A4 מוכן להדפסה
    ├── pdf.py            — המרת HTML ל-PDF + איחוד
    └── config.py         — הגדרות כיתות ותחנות
```

### תהליך הייצור

```
config.json
    │
    ▼
build_roadmap_prompt()   ─── LLM ──► מפת יחידה (STEAM + ימה"ע)
    │
    ▼ (לכל סבב)
build_*_prompt()         ─── LLM ──► JSON מובנה
    │
    ▼
render_*()               ──────────► HTML מעוצב (RTL, A4)
    │
    ▼
pdf.py                   ──────────► PDF (Playwright + pypdf)
```

---

## דרישות טכניות

- Python 3.10+
- `google-genai` — `pip install google-genai`
- `playwright` — `pip install playwright && playwright install chromium`
- `pypdf` — `pip install pypdf`


