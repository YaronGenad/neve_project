from typing import Dict, List
from .config import get_grade_level, get_stem_grade_level, get_english_grade_level, STEAM_GAMES_LIST


def build_roadmap_prompt(subject: str, topic: str, grade: str, rounds: int) -> str:
    gl = get_grade_level(grade)
    return f"""אתה מתכנן יחידת לימוד בשיטת א"ל השד"ה (הבנה, שיטות, דיוק, הרחבת אוצר מילים).

**נושא:** {subject} — {topic}
**כיתה:** {grade} | **גיל:** {gl['age']} | **רמת שפה:** {gl['language']}
**מספר סבבים:** {rounds}

**חוקי ברזל:**
1. כל 4 תחנות בכל סבב — **עצמאיות לחלוטין** (תלמיד יכול להתחיל בכל אחת)
2. תחנת הבנה = טקסט עשיר לקריאה + דיון בעל פה בלבד, ללא כתיבה
3. תחנת שיטות = כתיבה מובנית ומדורגת — המורה נמצאת פה פיזית
4. תחנת דיוק = לשון ודקדוק טכני (מגוון: הכתבות, שורשים, בניינים, מאזכרים, הומופוניות, זמנים, גופים)
5. תחנת אוצר מילים = **חוויה ופעולה** — פיזית או מודפסת, לפי מה שמתאים לנושא
6. תחנת הבנה: חייב להתחיל עם טקסט סיפורי, לא לחזור על אותו טקסט בסבבים
7. שלב ב-STEAM: שלב רב-תחומיות אמיתית (מדע/טכנולוגיה/אמנות/מתמטיקה) איפה שמתאים
8. הפעילויות מתקדמות מסבב לסבב: מבוא → העמקה → שיא

**סוגי כתיבה לתחנת שיטות (בחר לפי גיל וסבב):**
טיעון (בעד/נגד), תיאור (דמות/מקום/אירוע), תשובה מיטבית, סיכום, מיזוג, חוות דעת,
דוח (ניסוי/חקר/תצפית), מכתב (א-ב), שיר קצר (א-ב), יומן אישי (ג ומעלה), ניתוח טקסט מידעי (ה-ו), תרשים זרימה

**סוגי פעילות לתחנת אוצר מילים:**
מודפסות: matching_cards, sorting_table, dominoes, fill_in_poster, clothesline, idiom_cards, definition_table, crossword_mini
פיזיות/חווייתיות: physical_plasticine (פיסול מילה), physical_model (בניית מודל), physical_game (משחק קלפים/התאמה), physical_poster (כרזה/תערוכה), physical_simulation (משחק תפקידים/סימולציה)

**אפשרויות לפי גיל {gl['age']}:**
- הבנה: {', '.join(gl['comprehension_options'])}
- שיטות: {', '.join(gl['methods_options'])}
- דיוק: {', '.join(gl['precision_options'])}
- אוצר מילים: {', '.join(gl['vocabulary_options'])}

**פורמט פלט — JSON בלבד:**
{{
  "unit_title": "שם היחידה",
  "central_text_type": "סוג הטקסט המרכזי",
  "steam_connections": ["חיבור STEAM 1", "חיבור STEAM 2"],
  "learning_goals": {{
    "knowledge": ["ידע 1", "ידע 2"],
    "skills": ["מיומנות 1", "מיומנות 2"],
    "values": ["ערך/הרגל 1", "ערך/הרגל 2"]
  }},
  "rounds": [
    {{
      "round": 1,
      "comprehension": {{
        "text_type": "סיפורי/מידעי/רב-היצגי",
        "description": "תיאור קצר של הטקסט",
        "discussion_focus": "מי/מה/מדוע/קונפליקט/דילמה"
      }},
      "methods": {{
        "writing_type": "סוג הכתיבה מהרשימה",
        "description": "תיאור המשימה"
      }},
      "precision": {{
        "activity_type": "הכתבה/שורשים/בניינים/מאזכרים/זמנים/גופים/הומופוניות/רצף משפטים",
        "description": "תיאור"
      }},
      "vocabulary": {{
        "activity_type": "סוג הפעילות (מודפסת או פיזית)",
        "is_physical": false,
        "description": "תיאור"
      }}
    }}
  ]
}}"""


def build_comprehension_prompt(subject: str, topic: str, grade: str,
                                round_num: int, total_rounds: int,
                                round_plan: Dict, prev_texts: List[str]) -> str:
    gl = get_grade_level(grade)
    prev = ""
    if prev_texts:
        prev = f"\n\n**טקסטים קודמים (אל תחזור על תוכן זה):**\n" + "\n".join(prev_texts[-2:])

    text_type = round_plan.get('comprehension', {}).get('text_type', 'סיפורי')
    text_desc = round_plan.get('comprehension', {}).get('description', '')
    disc_focus = round_plan.get('comprehension', {}).get('discussion_focus', 'קונפליקט ודילמה')

    return f"""כתוב טקסט {text_type} עשיר לתחנת ההבנה בשיטת א"ל השד"ה.

**נושא:** {subject} — {topic}
**כיתה:** {grade} | **גיל:** {gl['age']} | **שפה:** {gl['language']}
**סבב {round_num} מתוך {total_rounds}** | **תכנון:** {text_desc}
**מוקד הדיון:** {disc_focus}
{prev}

**אפשרויות פעילות לתחנת הבנה לגיל זה:** {', '.join(gl['comprehension_options'])}

**⚠️ חוקים קריטיים:**
1. **אורך: {gl['text_length']}** — אל תקצר! זה טקסט לקריאה בעל פה, חייב להיות ארוך ועשיר
2. **אל תכלול שאלות בגוף הטקסט** — התחנה כולה בעל פה, הדיון הוא בין התלמידים
3. כלול 8-12 **מונחי מפתח** — מודגשים בטקסט
4. חלק ל-4-6 פסקאות עם כותרות משנה
5. כל פסקה לפחות 80 מילים
6. כל מושג חדש — הסבר בסוגריים בתוך הטקסט
7. שלב: {'רקע, הכרת הדמויות/המצב' if round_num == 1 else 'המשך ישיר, העמקה' if round_num < total_rounds else 'שיא, קונפליקט, סיום'}

**שאלות הדיון בעל פה (חמשת הממים + עומק):**
כלול 4-5 שאלות מדורגות:
- רמה 1: מי/מה/מתי/איפה (עובדתי)
- רמה 2: מדוע/כיצד (ניתוח)
- רמה 3: דילמה, קונפליקט, ערך ("מה היית עושה אם...")

**פורמט פלט — JSON בלבד:**
{{
  "section_title": "כותרת הסבב",
  "intro_sentence": "משפט פתיחה מרתק (שאלה רטורית / מצב מסקרן)",
  "paragraphs": [
    {{
      "subtitle": "כותרת משנה",
      "text": "טקסט הפסקה (מינימום 80 מילים)",
      "key_terms": ["מונח1", "מונח2"]
    }}
  ],
  "all_key_terms": ["כל המונחים המרכזיים (8-12)"],
  "discussion_starters": [
    "שאלת עובדה (מי/מה/מתי)",
    "שאלת ניתוח (מדוע/כיצד)",
    "שאלת דילמה / ערך / קונפליקט",
    "שאלה פתוחה להרחבה",
    "שאלת סיכום והפנמה"
  ]
}}"""


def build_methods_prompt(subject: str, topic: str, grade: str,
                          round_num: int, round_plan: Dict,
                          comprehension_text: Dict) -> str:
    gl = get_grade_level(grade)
    writing_type = round_plan.get('methods', {}).get('writing_type', 'תשובה מיטבית')
    methods_desc = round_plan.get('methods', {}).get('description', '')
    key_terms = comprehension_text.get('all_key_terms', [])

    text_summary = comprehension_text.get('section_title', '') + ": "
    for p in comprehension_text.get('paragraphs', [])[:2]:
        text_summary += p.get('text', '')[:200] + "... "

    return f"""צור משימת כתיבה מובנית לתחנת השיטות — א"ל השד"ה.

**נושא:** {subject} — {topic} | **סבב {round_num}**
**כיתה:** {grade} | **גיל:** {gl['age']}
**סוג הכתיבה:** {writing_type} | **תכנון:** {methods_desc}
**מונחים מהטקסט:** {', '.join(key_terms[:8])}
**הקשר הטקסט:** {text_summary[:300]}

**סוגי כתיבה אפשריים ודרישותיהם:**
- טיעון: עמדה + 3 נימוקים + סיכום, כיתה ד ומעלה
- תיאור: דמות/מקום/אירוע — חושים + פרטים + תחושות
- תשובה מיטבית: מבוססת טקסט, מלאה ומפורטת
- סיכום: רעיונות מרכזיים, בלי העתקה
- חוות דעת: עמדה אישית מנומקת + דוגמאות
- דוח: מבנה מדעי — שאלה, שיטה, ממצאים, מסקנות
- מכתב: פנייה, גוף, סיום — א-ב
- יומן אישי: קול אישי, רגשות, אירועים — ג ומעלה
- מיזוג: שילוב מידע מ-2+ מקורות לטקסט חדש
- ניתוח טקסט מידעי: מבנה + מסר + שכנוע — ה-ו

**אפשרויות סוגי כתיבה לגיל זה:** {', '.join(gl['methods_options'])}

**חוקים:**
1. המשימה מובנית ומדורגת — ניתן לפגום (scaffold) לתלמידים חלשים
2. כלול: הוראה ברורה + דוגמה/תבנית + שאלות מנחות
3. מותאם לגיל {gl['age']} ולדרישות משרד החינוך
4. כלול 3 רמות קושי (רמזור ירוק/צהוב/אדום) לאותה משימה בדיוק

**פורמט פלט — JSON בלבד:**
{{
  "title": "שם המשימה",
  "writing_type": "{writing_type}",
  "main_instruction": "הוראה ראשית ברורה לתלמיד",
  "context_prompt": "השאלה/הנושא שעליו כותבים",
  "scaffold_template": "תבנית/פיגום לכתיבה (כותרת, מבנה, משפטי פתיחה מוצעים)",
  "guiding_questions": [
    "שאלה מנחה 1",
    "שאלה מנחה 2",
    "שאלה מנחה 3"
  ],
  "difficulty_levels": {{
    "green": "משימה בסיסית (לתלמידים שמתקשים) — היקף קצר, תבנית נתונה",
    "yellow": "המשימה הרגילה — עצמאות חלקית",
    "red": "הרחבה לתלמידים מתקדמים — יצירתיות, עומק, היקף גדול"
  }},
  "words_range": "X-Y מילים",
  "lines_needed": 10,
  "success_criteria": ["קריטריון 1", "קריטריון 2", "קריטריון 3"]
}}"""


def build_precision_prompt(subject: str, topic: str, grade: str,
                            round_num: int, round_plan: Dict,
                            key_terms: List[str]) -> str:
    gl = get_grade_level(grade)
    activity_type = round_plan.get('precision', {}).get('activity_type', 'הכתבה ושורשים')
    precision_desc = round_plan.get('precision', {}).get('description', '')

    return f"""צור פעילות לתחנת הדיוק (לשון ודקדוק) — א"ל השד"ה.

**נושא:** {subject} — {topic} | **סבב {round_num}**
**כיתה:** {grade} | **גיל:** {gl['age']}
**סוג הפעילות:** {activity_type} | **תכנון:** {precision_desc}
**מילים מהטקסט:** {', '.join(key_terms[:12])}
**מספר מילים להכתבה לגיל זה:** {gl['dictation_words']}

**ארגז הכלים הלשוני המלא — בחר מגוון:**
- הכתבה: מילים ומשפטים מהטקסט
- מאזכרים: שם עצם / פועל / תואר — זיהוי וסיווג
- זמנים: עבר / הווה / עתיד — המרה
- גופים: ראשון/שני/שלישי, יחיד/רבים, זכר/נקבה
- יחיד ורבים: שם עצם ← שינוי צורה
- זכר ונקבה: התאמה
- שורשים ומשפחות מילים: חילוץ שורש, בניית משפחה
- בניינים: קל / פיעל / הפעיל / התפעל — זיהוי ושימוש
- אותיות הומופוניות: ט/ת, ח/כ, כ/ק, כ/ה, ע/א — מילוי
- סוגי משפטים: חיווי / שאלה / פקודה / קריאה
- רצף משפטים: סידור משפטים להקשר הגיוני
- חיבור מילים למשפט תקין
- נכון/לא נכון: בדיקת משפטים לשוניים

**אפשרויות פעילות לתחנת דיוק לגיל זה:** {', '.join(gl['precision_options'])}

**חוקים:**
1. כל המילים/משפטים — **מהטקסט** שנקרא בתחנת ההבנה
2. לכלול {gl['dictation_words']} מילים להכתבה
3. לכלול **2-3 סוגי תרגילים שונים** — לא רק הכתבה
4. הכל טכני-לשוני (לא שאלות הבנה)
5. מגוון: כל סבב — סוגי תרגילים שונים מהסבב הקודם

**פורמט פלט — JSON בלבד:**
{{
  "title": "שם הפעילות",
  "activity_type": "{activity_type}",
  "dictation_list": [
    {{"word": "מילה", "difficulty": "קל/בינוני/קשה", "note": "הערה אם צריך"}}
  ],
  "exercises": [
    {{
      "type": "שורשים/מאזכרים/זמנים/גופים/בניינים/הומופוניות/רצף/...",
      "title": "כותרת התרגיל",
      "instruction": "הוראה לתלמיד",
      "items": [
        {{"question": "...", "answer": "..."}}
      ]
    }}
  ],
  "sentences_for_dictation": [
    "משפט 1 מהטקסט להכתבה",
    "משפט 2 מהטקסט להכתבה"
  ],
  "answer_key": "מפתח תשובות מלא"
}}"""


def build_vocabulary_prompt(subject: str, topic: str, grade: str,
                             round_num: int, round_plan: Dict,
                             key_terms: List[str], used_types: List[str]) -> str:
    gl = get_grade_level(grade)
    activity_type = round_plan.get('vocabulary', {}).get('activity_type', 'matching_cards')
    is_physical = round_plan.get('vocabulary', {}).get('is_physical', False)
    vocab_desc = round_plan.get('vocabulary', {}).get('description', '')

    physical_note = """
**⚠️ פעילות פיזית/חווייתית — הנחיות:**
התחנה הזו היא hands-on. המוצר הוא:
1. גיליון הוראות לתלמיד (מה לעשות, שלב אחרי שלב)
2. רשימת חומרים (מה צריך להכין)
3. קלפי מילים להדפסה וגזירה (אם צריך)
הפעילות חייבת לערב גוף, ידיים, תנועה — "מה שנצרב בעור נשמר לנצח"
""" if is_physical else ""

    return f"""צור פעילות לתחנת הרחבת אוצר מילים — א"ל השד"ה.

**נושא:** {subject} — {topic} | **סבב {round_num}**
**כיתה:** {grade} | **גיל:** {gl['age']}
**סוג הפעילות:** {activity_type} | **תכנון:** {vocab_desc}
**מונחים מהטקסט:** {', '.join(key_terms[:12])}
**סוגים שכבר השתמשנו בהם:** {', '.join(used_types) if used_types else 'אין'}
{physical_note}

**עקרון התחנה:** "מה שנצרב בעור נשמר לנצח" — זיכרון ויזואלי + שמיעתי + תחושתי-מוטורי

**סוגי פעילויות מודפסות:**
- matching_cards: קלפי התאמה לגזירה (מילה ↔ הגדרה)
- sorting_table: טבלת מיון לקטגוריות (גזור ↔ הדבק)
- dominoes: דומינו מילים לגזירה
- fill_in_poster: כרזה עם רווחים למילוי
- clothesline: חיבור זוגות עם קו (נרדפות/הפכים)
- idiom_cards: קלפי ביטויים + פירוש
- definition_table: מילה | הגדרה | משפט
- crossword_mini: תשבץ מיני

**סוגי פעילויות פיזיות/חווייתיות:**
- physical_plasticine: פיסול מילה/מושג בפלסטלינה/בצק — כולל הוראות + רשימת מילים לפיסול
- physical_model: בניית מודל/דיאגרמה מקרטון/קלפים — כולל הוראות + תוויות להדפסה
- physical_game: משחק קלפים/זכרון/דומינו/סולמות ונחשים — כולל לוח/קלפים מודפסים
- physical_poster: בניית כרזה/תערוכה — כולל שאלות מנחות + פריסת עיצוב
- physical_simulation: משחק תפקידים/סימולציה — כולל תפקידים + הוראות הנחיה
- physical_clothesline: "חבל כביסה" — תליית קלפי מילים + זוגות (נרדפות/הפכים)

**חוקים:**
1. הפעילות חווייתית ומגוונת — לא רק "כתוב משפט"
2. המילים/ביטויים: מהטקסט + מונחי נושא חדשים
3. כלול הוראות ברורות + בנק מילים אם רלוונטי
4. כל סבב — סוג שונה (אל תחזור על מה שבוצע)

**פורמט פלט — JSON בלבד:**
{{
  "title": "שם הפעילות",
  "activity_type": "סוג הפעילות",
  "is_physical": {str(is_physical).lower()},
  "instruction": "הוראה ברורה לתלמיד (שלב אחרי שלב לפיזית)",
  "materials_needed": ["חומר 1", "חומר 2"],
  "words": [
    {{
      "word": "מילה/ביטוי",
      "definition": "הגדרה קצרה",
      "example": "משפט דוגמה",
      "category": "קטגוריה (אם רלוונטי)",
      "partner": "נרדפת/הפך (אם רלוונטי)"
    }}
  ],
  "word_bank": ["מילה1", "מילה2"],
  "left_column": ["פריט1", "פריט2", "פריט3", "פריט4", "פריט5", "פריט6", "פריט7", "פריט8"],
  "right_column": ["זוג1", "זוג2", "זוג3", "זוג4", "זוג5", "זוג6", "זוג7", "זוג8"],
  "categories": ["קטגוריה1", "קטגוריה2", "קטגוריה3"],
  "fill_sentences": [
    {{"sentence": "משפט עם _____ חלל", "answer": "התשובה"}}
  ],
  "crossword_clues": [
    {{"direction": "מאונך/מאוזן", "number": 1, "clue": "רמז", "answer": "תשובה"}}
  ],
  "physical_steps": [
    "שלב 1: ...",
    "שלב 2: ...",
    "שלב 3: ..."
  ],
  "answer_key": "מפתח תשובות מלא"
}}"""


def build_teacher_prep_prompt(subject: str, topic: str, grade: str,
                               round_num: int, all_content: Dict) -> str:
    comp = all_content.get('comprehension', {})
    meth = all_content.get('methods', {})
    prec = all_content.get('precision', {})
    vocab = all_content.get('vocabulary', {})
    is_physical_vocab = vocab.get('is_physical', False)

    return f"""צור דף הכנה למורה לסבב {round_num} של יחידה בשיטת א"ל השד"ה.

**נושא:** {subject} — {topic} | **כיתה:** {grade} | **סבב {round_num}**

**תחנות הסבב:**
- הבנה: {comp.get('section_title', '')} ({len(comp.get('paragraphs', []))} פסקאות) — **תחנה בעל פה בלבד**, המורה לא נמצאת כאן
- שיטות: {meth.get('title', '')} — {meth.get('writing_type', '')} — **המורה יושבת כאן**
- דיוק: {prec.get('title', '')} — {prec.get('activity_type', '')}
- אוצר מילים: {vocab.get('title', '')} — {vocab.get('activity_type', '')} {'(פעילות פיזית — נדרשת הכנת חומרים)' if is_physical_vocab else '(מודפס)'}

**פורמט פלט — JSON בלבד:**
{{
  "objectives": {{
    "knowledge": ["ידע שיירכש 1", "ידע שיירכש 2"],
    "skills": ["מיומנות שתתפתח 1", "מיומנות 2"],
    "values": ["ערך/הרגל 1", "ערך/הרגל 2"]
  }},
  "steam_connections": ["חיבור בין-תחומי 1 (מדע/טכנולוגיה/אמנות/מתמטיקה)"],
  "materials": {{
    "comprehension": ["עותקי הטקסט לכל תלמיד", "..."],
    "methods": ["דף משימה", "..."],
    "precision": ["דף תרגילים", "..."],
    "vocabulary": ["חומרים נדרשים — במיוחד לפיזי: {', '.join(vocab.get('materials_needed', ['דפי הפעילות']))}"]
  }},
  "timing": {{
    "comprehension": "15-20 דקות",
    "methods": "20-25 דקות",
    "precision": "15-20 דקות",
    "vocabulary": "15-20 דקות"
  }},
  "rotation_tip": "הוראה לסיבוב קבוצות בין התחנות",
  "teacher_notes": [
    "נקודה חשובה לתחנת הבנה (בעל פה בלבד!)",
    "נקודה לתחנת שיטות (המורה כאן)",
    "קושי צפוי + פתרון מוצע",
    "הצעה להרחבה לתלמידים מתקדמים"
  ],
  "differentiation": {{
    "struggling": "איך לתמוך בתלמידים חלשים בכל תחנה",
    "advanced": "הרחבה לתלמידים חזקים",
    "special_needs": "התאמות לחינוך מיוחד"
  }},
  "self_check": [
    "האם כל תחנה עצמאית לחלוטין?",
    "האם תחנת הבנה ללא כתיבה?",
    "האם תחנת אוצר מילים hands-on/חווייתית?",
    "האם יש דיפרנציאציה מובנית?"
  ]
}}"""


# ═══════════════════════════════════════════════════════════════════
#  STEAM EDITION — prompts for STEM subjects
# ═══════════════════════════════════════════════════════════════════

def build_stem_roadmap_prompt(subject: str, topic: str, grade: str, rounds: int) -> str:
    gl = get_grade_level(grade)
    sgl = get_stem_grade_level(grade)
    return f"""אתה מתכנן יחידת לימוד בשיטת א"ל השד"ה — **גרסת STEAM** (מתמטיקה/מדעים/הנדסה/טכנולוגיה/אמנויות).

**מקצוע:** {subject} | **נושא:** {topic}
**כיתה:** {grade} | **גיל:** {gl['age']} | **מספר סבבים:** {rounds}

**שינויים עיקריים בגרסת STEAM לעומת גרסת השפה:**
- תחנת הבנה: ערוצי קלט מגוונים (טקסט/סרטון/תצפית/ניסוי) + תיעוד כתוב קצר מותר
- תחנת שיטות: חשיבה תהליכית-פרוצדורלית (EDP / מתודה מדעית / ניתוח נתונים / חשיבה מתמטית)
- תחנת דיוק: **HANDS-ON** — ניסויים, מדידות, בנייה הנדסית, יצירה מוחשית (לא דקדוק!)
- תחנת אוצר מילים: מושגי STEAM בעברית + אנגלית + 17 משחקים ייחודיים

**חוקי ברזל:**
1. כל 4 תחנות — **עצמאיות לחלוטין** (STAND-ALONE); אם תחנה X צריכה תוצר של תחנה Y — הכניסי אותו ישירות לתחנה X
2. תחנת דיוק = HANDS-ON בלבד — ניסוי/בנייה/מדידה; כולל הוראות ורקע מינימלי עצמאי
3. נתוני ניסוי לתחנת שיטות — מסופקים בתוך התחנה (לא תלויים בתחנת הדיוק)
4. תחנת אוצר מילים: חייבת לכלול מונחים בעברית ובאנגלית + משחק מהרשימה
5. התקדמות סבבים לפי מודל STEAM: גילוי → חקירה מעמיקה → ישום ותיכון → סיכום והצגה

**מודל התקדמות STEAM:**
- סבב 1: היכרות עם התופעה — הבנה ראשונית, ניסוי גילוי, מושגים בסיסיים
- סבב 2: חקירה מעמיקה — קריאה מדעית, ניסוי מובנה, ניתוח נתונים
- סבב 3: ישום ותיכון — פתרון בעיה, בנייה הנדסית, קישור לעולם אמיתי
- סבב 4: סיכום ושיקוף — הצגה, כתיבה סיכומית, מושגים מתקדמים

**ערוצי קלט לתחנת הבנה לגיל {gl['age']}:** {', '.join(sgl['comprehension_channels'])}
**מסגרות חשיבה לתחנת שיטות לגיל {gl['age']}:** {', '.join(sgl['methods_frameworks'])}
**פעילויות HANDS-ON לתחנת דיוק לגיל {gl['age']}:** {', '.join(sgl['precision_activities'])}
**משחקים לתחנת אוצר מילים לגיל {gl['age']}:** {', '.join(sgl['vocabulary_games'])}

**פורמט פלט — JSON בלבד:**
{{
  "unit_title": "שם היחידה",
  "is_steam": true,
  "central_phenomenon": "התופעה/הבעיה/השאלה המרכזית שמניעה את היחידה",
  "steam_connections": ["חיבור STEAM 1", "חיבור STEAM 2"],
  "learning_goals": {{
    "knowledge": ["ידע 1", "ידע 2"],
    "skills": ["מיומנות 1", "מיומנות 2"],
    "values": ["ערך/הרגל 1"]
  }},
  "rounds": [
    {{
      "round": 1,
      "comprehension": {{
        "input_type": "text|video|observation|experiment|multi_source",
        "description": "תיאור קצר של החומר/הפעילות",
        "discussion_focus": "שאלת חקירה / תופעה מעוררת מחשבה"
      }},
      "methods": {{
        "thinking_framework": "scientific_method|EDP|data_analysis|mathematical_thinking|art_design",
        "description": "תיאור המשימה"
      }},
      "precision": {{
        "hands_on_type": "science_experiment|measurement_data|engineering_building|math_hands_on|art_design",
        "description": "תיאור הניסוי/הבנייה/המדידה"
      }},
      "vocabulary": {{
        "game_type": "stem_memory|stem_alias|stem_taboo|stem_quartets|stem_bingo|stem_snakes|stem_quiz|stem_who_am_i|stem_dominoes|stem_flashcard|stem_concept_puzzle|stem_word_chain|stem_matching_board|stem_20_questions|stem_track|stem_catan|stem_monopoly",
        "description": "תיאור המשחק ומה לומדים"
      }}
    }}
  ]
}}"""


def build_stem_comprehension_prompt(subject: str, topic: str, grade: str,
                                     round_num: int, total_rounds: int,
                                     round_plan: Dict, prev_texts: List[str]) -> str:
    gl = get_grade_level(grade)
    sgl = get_stem_grade_level(grade)
    prev = ""
    if prev_texts:
        prev = f"\n\n**חומרים קודמים (אל תחזור על תוכן זה):**\n" + "\n".join(prev_texts[-2:])

    input_type = round_plan.get('comprehension', {}).get('input_type', 'text')
    desc = round_plan.get('comprehension', {}).get('description', '')
    disc_focus = round_plan.get('comprehension', {}).get('discussion_focus', 'תופעה מדעית מעוררת חשיבה')

    input_labels = {
        'text': 'טקסט מדעי / כתבה',
        'video': 'תיאור סרטון מדעי + שאלות הכוונה',
        'observation': 'תצפית מונחת + תיעוד',
        'experiment': 'ניסוי קצר להמחשה (לא ניתוח — זה שמור לתחנת הדיוק)',
        'multi_source': 'שילוב של מקורות (טקסט + גרף/תמונה/נתונים)',
    }
    input_label = input_labels.get(input_type, 'טקסט מדעי')

    progression = {
        1: 'היכרות ראשונית עם התופעה — עורר סקרנות, הצג את השאלה המרכזית',
        2: 'חקירה מעמיקה — הצג נתונים, ראיות, מנגנון',
        3: 'ישום — הצג קישור לעולם אמיתי, פתרון בעיה, הנדסה',
        4: 'סיכום — הצג סינתזה, תובנות, שאלות פתוחות לעתיד',
    }
    stage = progression.get(round_num, progression[min(round_num, 4)])
    {prev}

    return f"""כתוב חומר לתחנת ההבנה — א"ל השד"ה גרסת STEAM.

**מקצוע:** {subject} | **נושא:** {topic}
**כיתה:** {grade} | **גיל:** {gl['age']}
**סבב {round_num} מתוך {total_rounds}** | **שלב:** {stage}
**ערוץ קלט:** {input_label} | **תכנון:** {desc}
**מוקד חקירה:** {disc_focus}
{prev}

**⚠️ הבדלים מגרסת השפה:**
- מותר לכלול תשובה כתובה קצרה (1-3 משפטים) לצורך תיעוד הבנה
- שלב טבלת KWL (יודע / רוצה לדעת / למדתי)
- כל מונח מדעי חדש: עברית + אנגלית + הגדרה קצרה
- שאלות החקירה יכולות לכלול: ניבוי, השוואה, קישור לחיים, שאלת ניסוי

**⚠️ חוקים קריטיים:**
1. **אורך: {sgl['text_length']}** — עשיר ומעמיק
2. כלול 8-12 **מונחי מפתח** — עברית + אנגלית בסוגריים
3. חלק ל-4-5 פסקאות עם כותרות משנה
4. כל מושג חדש — הסבר בסוגריים בתוך הטקסט
5. שלב גרפים/נתונים/מספרים כשרלוונטי

**פורמט פלט — JSON בלבד:**
{{
  "section_title": "כותרת הסבב",
  "is_steam": true,
  "input_type": "{input_type}",
  "intro_question": "שאלת פתיחה מעוררת סקרנות (תופעה / בעיה / שאלה מדעית)",
  "paragraphs": [
    {{
      "subtitle": "כותרת משנה",
      "text": "טקסט מדעי עשיר (כולל מונחים מודגשים, מספרים, דוגמאות)",
      "key_terms": ["מונח בעברית (English Term)", "מונח2 (Term2)"]
    }}
  ],
  "kwl_table": {{
    "know_prompts": ["מה אני כבר יודע/ת על נושא זה: ___", "דוגמה שאני מכיר/ה: ___"],
    "wonder_prompts": ["שאלה שאני רוצה לברר: ___", "תהייה שעלתה לי: ___"]
  }},
  "written_response": {{
    "question": "שאלה קצרה לתשובה כתובה (1-3 משפטים)",
    "scaffold": "_____ קורה כי _____. לדעתי _____ כי _____.",
    "instruction": "כתוב/כתבי תשובה קצרה (1-3 משפטים) — אין צורך בפסקה מלאה"
  }},
  "all_key_terms": ["מונח1 (Term1)", "מונח2 (Term2)", "מונח3 (Term3)"],
  "discussion_starters": [
    "שאלת תצפית: מה קורה כאן? מה אתה/את מבחין/ה?",
    "שאלת תהליך: מדוע? באיזה סדר? מה גורם למה?",
    "שאלת ניבוי: מה יקרה אם נשנה את ___?",
    "שאלת קישור: איפה רואים את זה בחיים? מה הקשר ל___?",
    "שאלת ניסוי: מה היית רוצה לבדוק? מה ההשערה שלך?"
  ]
}}"""


def build_stem_methods_prompt(subject: str, topic: str, grade: str,
                               round_num: int, round_plan: Dict,
                               comprehension_text: Dict) -> str:
    gl = get_grade_level(grade)
    sgl = get_stem_grade_level(grade)
    framework = round_plan.get('methods', {}).get('thinking_framework', 'scientific_method')
    methods_desc = round_plan.get('methods', {}).get('description', '')
    key_terms = comprehension_text.get('all_key_terms', [])

    text_summary = comprehension_text.get('section_title', '') + ": "
    for p in comprehension_text.get('paragraphs', [])[:2]:
        text_summary += p.get('text', '')[:200] + "... "

    framework_descriptions = {
        'scientific_method': 'המתודה המדעית: תצפית → שאלת חקירה → השערה → ניסוי → ניתוח → מסקנה',
        'EDP': 'תהליך התיכון ההנדסי (EDP): זיהוי בעיה → מחקר → הצעת פתרונות → בחירה ותכנון → בנייה ובדיקה → שיפור',
        'data_analysis': 'ניתוח נתונים: קריאת גרף/טבלה → זיהוי מגמות → פרשנות → מסקנות',
        'mathematical_thinking': 'חשיבה מתמטית: הבנת הבעיה → תכנון → פתרון שלב אחר שלב → בדיקה → הכללה',
        'art_design': 'חשיבה עיצובית: ניתוח → כוונה → תכנון → ביצוע → הצגה',
    }
    fw_desc = framework_descriptions.get(framework, framework_descriptions['scientific_method'])

    # For data_analysis framework, we provide sample data directly in the station
    data_note = ""
    if framework == 'data_analysis':
        data_note = "\n**חשוב:** כלול בתוך המשימה נתונים/גרף/טבלה ספציפיים לניתוח — התחנה עצמאית לחלוטין ואינה תלויה בניסוי מתחנת הדיוק!"

    return f"""צור משימת חשיבה תהליכית-פרוצדורלית לתחנת השיטות — א"ל השד"ה גרסת STEAM.

**מקצוע:** {subject} | **נושא:** {topic} | **סבב {round_num}**
**כיתה:** {grade} | **גיל:** {gl['age']}
**מסגרת חשיבה:** {fw_desc}
**תכנון:** {methods_desc}
**מונחים מהחומר:** {', '.join(key_terms[:8])}
**הקשר:** {text_summary[:300]}
{data_note}

**מסגרות חשיבה זמינות לגיל זה:** {', '.join(sgl['methods_frameworks'])}

**חוקים:**
1. המשימה מובנית — כלול פיגום (scaffold) מלא: תבנית, שלבים, דוגמה
2. אם הניתוח מצריך נתוני ניסוי — **ספק אותם ישירות בתוך המשימה** (תחנה עצמאית!)
3. כלול 3 רמות קושי (רמזור ירוק/צהוב/אדום)
4. מותאם לגיל {gl['age']}

**פורמט פלט — JSON בלבד:**
{{
  "title": "שם המשימה",
  "thinking_framework": "{framework}",
  "main_instruction": "הוראה ראשית ברורה לתלמיד",
  "context_prompt": "הבעיה/השאלה/הנתונים שעובדים איתם",
  "framework_steps": ["שלב 1: ...", "שלב 2: ...", "שלב 3: ..."],
  "context_data": "נתונים/גרף/טבלה/בעיה מוחשית לניתוח (אם נדרש — מלא כאן!)",
  "scaffold_template": "תבנית/פיגום לכתיבה עם מבנה ברור",
  "guiding_questions": [
    "שאלה מנחה 1",
    "שאלה מנחה 2",
    "שאלה מנחה 3"
  ],
  "difficulty_levels": {{
    "green": "משימה בסיסית — שלבים נתונים, מבנה מלא, תמיכה מרבית",
    "yellow": "המשימה הרגילה — עצמאות חלקית לפי המסגרת",
    "red": "הרחבה — יישום בהקשר חדש, ביקורת, הכללה"
  }},
  "words_range": "X-Y מילים / משפטים / פריטים",
  "lines_needed": 12,
  "success_criteria": ["קריטריון 1", "קריטריון 2", "קריטריון 3"]
}}"""


def build_stem_precision_prompt(subject: str, topic: str, grade: str,
                                 round_num: int, round_plan: Dict,
                                 key_terms: List[str]) -> str:
    gl = get_grade_level(grade)
    sgl = get_stem_grade_level(grade)
    hands_on_type = round_plan.get('precision', {}).get('hands_on_type', 'science_experiment')
    precision_desc = round_plan.get('precision', {}).get('description', '')

    type_descriptions = {
        'science_experiment': 'ניסוי מדעי — בדיקת השערה, מדידה, תיעוד תוצאות, מסקנה',
        'measurement_data': 'מדידות ואיסוף נתונים — מדידה, רישום בטבלה, בניית גרף',
        'engineering_building': 'בנייה הנדסית — בנייה לפי מפרט, בדיקת ביצועים, שיפור',
        'math_hands_on': 'מתמטיקה מוחשית — מניפולטיבים, מדידה, פיצול/הרכבה גיאומטרי',
        'art_design': 'יצירה ועיצוב — יצירת מודל/אינפוגרפיקה/פרוטוטייפ המדגים מושג',
    }
    type_desc = type_descriptions.get(hands_on_type, type_descriptions['science_experiment'])

    return f"""צור פעילות HANDS-ON לתחנת הדיוק — א"ל השד"ה גרסת STEAM.

**מקצוע:** {subject} | **נושא:** {topic} | **סבב {round_num}**
**כיתה:** {grade} | **גיל:** {gl['age']}
**סוג הפעילות:** {type_desc}
**תכנון:** {precision_desc}
**מונחי מפתח:** {', '.join(key_terms[:10])}

**פעילויות HANDS-ON מתאימות לגיל זה:** {', '.join(sgl['precision_activities'])}

**⚠️ חוקים קריטיים — גרסת STEAM:**
1. זו תחנת HANDS-ON בלבד — **אין הכתבות ואין תרגילי דקדוק**
2. כלול הוראות מלאות ועצמאיות — תלמיד יכול להתחיל ישירות ללא תלות בתחנות אחרות
3. כלול שאלת חקירה + השערה לפני הניסוי
4. כלול טבלת תיעוד ריקה + שאלות ניתוח + מסקנה מובנית
5. ציין חומרים בטוחים לגיל {gl['age']} + הערות בטיחות
6. כלול 3 רמות קושי (ירוק/צהוב/אדום) — קל/רגיל/מאתגר

**פורמט פלט — JSON בלבד:**
{{
  "title": "שם הניסוי/הפעילות",
  "is_hands_on": true,
  "hands_on_type": "{hands_on_type}",
  "research_question": "מה אנחנו בודקים/בונים/מודדים?",
  "background_mini": "רקע מינימלי (2-3 משפטים) לביצוע עצמאי של הפעילות",
  "hypothesis_scaffold": "ההשערה שלי: אני חושב/ת שיקרה ___ כי ___",
  "materials_needed": ["חומר 1", "חומר 2", "כלי 1"],
  "safety_notes": ["הערת בטיחות 1 (אם רלוונטי)"],
  "steps": [
    "שלב 1: ...",
    "שלב 2: ...",
    "שלב 3: ..."
  ],
  "data_table": {{
    "headers": ["תצפית/מדידה", "תוצאה 1", "תוצאה 2"],
    "rows": [["ניסיון 1", "", ""], ["ניסיון 2", "", ""], ["ניסיון 3", "", ""]]
  }},
  "analysis_questions": [
    {{"question": "מה גילינו? האם ההשערה אושרה?", "answer": "תשובה צפויה למורה"}},
    {{"question": "מה השפיע על התוצאה?", "answer": "תשובה צפויה למורה"}},
    {{"question": "מה היית משנה בניסוי הבא?", "answer": "תשובה פתוחה"}}
  ],
  "conclusion_scaffold": "גילינו ש ___ כי ___. הדבר קורה בגלל ___. קישור לחיים: ___.",
  "difficulty_levels": {{
    "green": "גרסה קלה — שלבים נתונים, טבלה ממולאת חלקית, הוראות מפורטות יותר",
    "yellow": "הגרסה הרגילה — כמתואר למעלה",
    "red": "אתגר נוסף — שאלת הרחבה, שינוי משתנה, ניסוי נוסף עצמאי"
  }},
  "expected_results": "תוצאות צפויות + הסבר מדעי מלא — למורה בלבד"
}}"""


def build_stem_vocabulary_prompt(subject: str, topic: str, grade: str,
                                  round_num: int, round_plan: Dict,
                                  key_terms: List[str], used_types: List[str]) -> str:
    gl = get_grade_level(grade)
    sgl = get_stem_grade_level(grade)
    game_type = round_plan.get('vocabulary', {}).get('game_type', 'stem_memory')
    vocab_desc = round_plan.get('vocabulary', {}).get('description', '')

    game_labels = {
        'stem_memory': ('זיכרון מושגים (Memory Match)', 'זוגות עברית↔אנגלית / מונח↔הגדרה'),
        'stem_alias': ('אליאס מדעי (Science Alias)', 'הסבר מושג ללא המילה; צוות מנחש'),
        'stem_taboo': ('טאבו מדעי (Science Taboo)', 'הסבר ללא מילות המפתח האסורות'),
        'stem_quartets': ('רביעיות מדעיות (Quartets)', 'אסיפת 4 קלפים מאותה קטגוריה STEAM'),
        'stem_bingo': ('Bingo מדעי (STEAM Bingo)', 'הגדרות נקראות; מי שמזהה — סומן'),
        'stem_snakes': ('סולמות ונחשים STEAM', 'שאלת מושג בכל ריבוע; עלה/רד'),
        'stem_quiz': ('שאלות ותשובות (Quiz Bowl)', 'קלפי שאלות לפי נושאי STEAM'),
        'stem_who_am_i': ('מי אני? (Who Am I? Science)', 'כרטיס מושג על המצח; שאלות כן/לא'),
        'stem_dominoes': ('דומינו STEAM', 'מושג↔הגדרה; הנח קלף שמושג פוגש הגדרתו'),
        'stem_flashcard': ('כרטיסיות אוצר (Flashcard Battle)', 'מי עונה על ההגדרה מהר יותר'),
        'stem_concept_puzzle': ('פאזל מושגים (Concept Puzzle)', 'חתוך ל-4 חלקים: שם/הגדרה/דוגמה/ציור'),
        'stem_word_chain': ('שרשרת מדעית (Word Chain)', 'מושג שמתחיל באות אחרונה + הסבר הקשר'),
        'stem_matching_board': ('התאמת מושגים (Matching Board)', 'לוח גדול; חיבור מושג↔הגדרה/תמונה'),
        'stem_20_questions': ('20 שאלות מדעיות', 'שאלות כן/לא לגילוי המושג הנסתר'),
        'stem_track': ('מסלול מדעי (STEAM Track)', 'כרטיסיות ירוק/צהוב/אדום לפי קושי'),
        'stem_catan': ('קטאן מדעי (Science Catan)', 'בנה ממלכה; ענה נכון — קבל משאב'),
        'stem_monopoly': ('מונופול מדעי (Science Monopoly)', 'נכסים = מושגי STEAM; ענה הגדרה'),
    }
    game_name, game_mechanic = game_labels.get(game_type, ('זיכרון מושגים', 'זוגות מושגים'))

    return f"""צור פעילות לתחנת הרחבת אוצר מילים — א"ל השד"ה גרסת STEAM.

**מקצוע:** {subject} | **נושא:** {topic} | **סבב {round_num}**
**כיתה:** {grade} | **גיל:** {gl['age']}
**המשחק:** {game_name} | **מנגנון:** {game_mechanic}
**תכנון:** {vocab_desc}
**מונחים מהחומר:** {', '.join(key_terms[:12])}
**סוגים שבוצעו כבר:** {', '.join(used_types) if used_types else 'אין'}

**עקרון STEAM לתחנה זו:**
- כל מונח: עברית + אנגלית + הגדרה + קטגוריית STEAM (מדעים/מתמטיקה/הנדסה/טכנולוגיה/אמנויות)
- המשחק צריך להיות מהנה, תחרותי, ומפנים את המושגים לזיכרון ארוך-טווח

**רשימת 17 המשחקים לעיון:**
{STEAM_GAMES_LIST}

**משחקים מתאימים לגיל זה:** {', '.join(sgl['vocabulary_games'])}

**חוקים:**
1. כלול 8-14 מושגים בעברית + אנגלית
2. כלול הוראות משחק מפורטות שלב אחרי שלב
3. כלול רשימת חומרים נדרשים (קלפים לגזירה וכו')
4. כלול קלפי מושגים להדפסה/גזירה

**פורמט פלט — JSON בלבד:**
{{
  "title": "שם הפעילות",
  "game_type": "{game_type}",
  "is_physical": true,
  "bilingual": true,
  "instruction": "הוראות המשחק שלב אחרי שלב (כולל: הכנה / שחקנים / כיצד משחקים / כיצד מנצחים)",
  "materials_needed": ["קלפים להדפסה וגזירה", "חומר נוסף אם נדרש"],
  "words": [
    {{
      "word": "מונח בעברית",
      "english": "English Term",
      "definition": "הגדרה קצרה ובהירה",
      "example": "דוגמה מהחיים",
      "category": "מדעים|מתמטיקה|הנדסה|טכנולוגיה|אמנויות"
    }}
  ],
  "categories": ["קטגוריה 1", "קטגוריה 2"],
  "physical_steps": [
    "שלב 1: הדפס וגזור את הקלפים",
    "שלב 2: ...",
    "שלב 3: ..."
  ],
  "answer_key": "מפתח תשובות / רשימת ההתאמות הנכונות — למורה"
}}"""


# ═══════════════════════════════════════════════════════════════════
#  ENGLISH EDITION — prompts for English as a subject (EFL/ESL)
#  All output must be entirely in English, adapted to grade CEFR level.
# ═══════════════════════════════════════════════════════════════════

def build_english_roadmap_prompt(subject: str, topic: str, grade: str, rounds: int) -> str:
    egl = get_english_grade_level(grade)
    return f"""You are planning an English language learning unit using the Al-HaSadeh (station-rotation) method.

**Subject:** {subject} | **Topic:** {topic}
**Grade:** {grade} | **Age:** {egl['age']} | **CEFR Level:** {egl['cefr']}
**Number of rounds:** {rounds}

**IMPORTANT: ALL output — every word, title, instruction, question, and label — must be in English.**

**Station structure (same as Hebrew edition, but fully in English):**
1. **Comprehension Station** — rich reading text + oral discussion only (no writing)
2. **Methods Station** — structured, scaffolded writing task (teacher present)
3. **Precision Station** — spelling, grammar, vocabulary accuracy (technical language work)
4. **Vocabulary Station** — experiential activity (printed or hands-on)

**Iron rules:**
1. All 4 stations in every round are **fully independent** (student can start at any station)
2. Comprehension = reading text + oral discussion only, no writing required
3. Methods = structured writing — teacher is physically present here
4. Precision = technical language work (spelling, grammar, word forms — NOT comprehension questions)
5. Vocabulary = experiential and engaging — printed or hands-on
6. Progression across rounds: introduction → development → deepening → synthesis

**Writing types for Methods station:**
opinion paragraph, descriptive writing, narrative, summary, compare and contrast,
personal response, formal letter, dialogue writing, short poem, information report

**Activity types for Vocabulary station:**
Printed: matching_cards, sorting_table, dominoes, fill_in_poster, clothesline, idiom_cards, definition_table, crossword_mini
Physical/experiential: physical_plasticine, physical_model, physical_game, physical_poster, physical_simulation, physical_clothesline

**Age-appropriate options for grade {grade} ({egl['cefr']}):**
- Comprehension: {', '.join(egl['comprehension_options'])}
- Methods: {', '.join(egl['methods_options'])}
- Precision: {', '.join(egl['precision_options'])}
- Vocabulary: {', '.join(egl['vocabulary_options'])}

**Output format — JSON only (all values in English):**
{{
  "unit_title": "Unit title in English",
  "central_text_type": "text type",
  "language_focus": "main language/grammar focus of the unit",
  "learning_goals": {{
    "knowledge": ["knowledge goal 1", "knowledge goal 2"],
    "skills": ["skill 1", "skill 2"],
    "values": ["value/habit 1"]
  }},
  "rounds": [
    {{
      "round": 1,
      "comprehension": {{
        "text_type": "narrative/informational/dialogue/poem",
        "description": "brief description of the text",
        "discussion_focus": "main discussion question / conflict / theme"
      }},
      "methods": {{
        "writing_type": "writing type from the list",
        "description": "description of the task"
      }},
      "precision": {{
        "activity_type": "spelling/grammar/word-forms/punctuation/tenses/prepositions",
        "description": "description"
      }},
      "vocabulary": {{
        "activity_type": "activity type (printed or physical)",
        "is_physical": false,
        "description": "description"
      }}
    }}
  ]
}}"""


def build_english_comprehension_prompt(subject: str, topic: str, grade: str,
                                        round_num: int, total_rounds: int,
                                        round_plan: Dict, prev_texts: List[str]) -> str:
    egl = get_english_grade_level(grade)
    prev = ""
    if prev_texts:
        prev = f"\n\n**Previous texts (do not repeat this content):**\n" + "\n".join(prev_texts[-2:])

    text_type = round_plan.get('comprehension', {}).get('text_type', 'narrative')
    text_desc = round_plan.get('comprehension', {}).get('description', '')
    disc_focus = round_plan.get('comprehension', {}).get('discussion_focus', 'conflict and values')

    return f"""Write a rich {text_type} text for the Comprehension Station of an Al-HaSadeh English lesson.

**IMPORTANT: ALL output — every word, title, instruction, question, and label — must be in English.**

**Subject:** {subject} | **Topic:** {topic}
**Grade:** {grade} | **Age:** {egl['age']} | **CEFR:** {egl['cefr']} | **Language level:** {egl['language']}
**Round {round_num} of {total_rounds}** | **Plan:** {text_desc}
**Discussion focus:** {disc_focus}
{prev}

**Age-appropriate comprehension activities:** {', '.join(egl['comprehension_options'])}

**⚠️ Critical rules:**
1. **Length: {egl['text_length']}** — do not shorten! This is a read-aloud text, it must be rich and engaging
2. **Do NOT include written questions in the text body** — the station is oral discussion only
3. Include 8-12 **key vocabulary words** — highlighted/bolded in the text
4. Divide into 4-6 paragraphs with subheadings
5. Each paragraph at least 60 words
6. Explain any new word in parentheses within the text
7. Stage: {'introduction — meet the characters/situation' if round_num == 1 else 'development — deepen the story/topic' if round_num < total_rounds else 'climax — conflict, resolution, conclusion'}
8. Language complexity must match CEFR {egl['cefr']} — use {egl['language']}

**Oral discussion questions (5 Ws + depth):**
Include 4-5 graded questions:
- Level 1: Who/What/When/Where (factual)
- Level 2: Why/How (analysis)
- Level 3: Opinion, dilemma, personal connection ("What would you do if...")

**Output format — JSON only (ALL values in English):**
{{
  "section_title": "Round title in English",
  "intro_sentence": "Engaging opening sentence (rhetorical question / intriguing situation)",
  "paragraphs": [
    {{
      "subtitle": "Subheading in English",
      "text": "Paragraph text (minimum 60 words, CEFR {egl['cefr']} level)",
      "key_terms": ["term1", "term2"]
    }}
  ],
  "all_key_terms": ["all key vocabulary words (8-12)"],
  "discussion_starters": [
    "Factual question (Who/What/When/Where)",
    "Analysis question (Why/How)",
    "Opinion/dilemma/values question",
    "Open-ended extension question",
    "Summary and reflection question"
  ]
}}"""


def build_english_methods_prompt(subject: str, topic: str, grade: str,
                                  round_num: int, round_plan: Dict,
                                  comprehension_text: Dict) -> str:
    egl = get_english_grade_level(grade)
    writing_type = round_plan.get('methods', {}).get('writing_type', 'opinion paragraph')
    methods_desc = round_plan.get('methods', {}).get('description', '')
    key_terms = comprehension_text.get('all_key_terms', [])

    text_summary = comprehension_text.get('section_title', '') + ": "
    for p in comprehension_text.get('paragraphs', [])[:2]:
        text_summary += p.get('text', '')[:200] + "... "

    return f"""Create a structured writing task for the Methods Station of an Al-HaSadeh English lesson.

**IMPORTANT: ALL output — every word, title, instruction, question, and label — must be in English.**

**Subject:** {subject} | **Topic:** {topic} | **Round {round_num}**
**Grade:** {grade} | **Age:** {egl['age']} | **CEFR:** {egl['cefr']}
**Writing type:** {writing_type} | **Plan:** {methods_desc}
**Key words from text:** {', '.join(key_terms[:8])}
**Text context:** {text_summary[:300]}

**Writing types and their requirements:**
- Opinion paragraph: clear stance + 2-3 reasons + conclusion
- Descriptive writing: sensory details + vivid adjectives + structure
- Narrative: beginning/middle/end, characters, setting, problem/solution
- Summary: main ideas only, no copying, own words
- Compare and contrast: similarities and differences, organized structure
- Personal response: personal connection + evidence from text
- Formal letter: greeting, body paragraphs, closing
- Information report: topic sentence, facts, conclusion

**Age-appropriate writing options for grade {grade} ({egl['cefr']}):** {', '.join(egl['methods_options'])}

**Rules:**
1. Task is structured and scaffolded — support for struggling students
2. Include: clear instruction + example/template + guiding questions
3. Appropriate for age {egl['age']} and CEFR {egl['cefr']}
4. Include 3 difficulty levels (traffic light: green/yellow/red) for the same task

**Output format — JSON only (ALL values in English):**
{{
  "title": "Task title in English",
  "writing_type": "{writing_type}",
  "main_instruction": "Clear main instruction for the student",
  "context_prompt": "The question/topic to write about",
  "scaffold_template": "Writing template/scaffold (title, structure, suggested opening sentences)",
  "guiding_questions": [
    "Guiding question 1",
    "Guiding question 2",
    "Guiding question 3"
  ],
  "difficulty_levels": {{
    "green": "Basic task (for struggling students) — short, full template provided",
    "yellow": "Regular task — partial independence",
    "red": "Extension for advanced students — creativity, depth, longer response"
  }},
  "words_range": "X-Y words",
  "lines_needed": 10,
  "success_criteria": ["criterion 1", "criterion 2", "criterion 3"]
}}"""


def build_english_precision_prompt(subject: str, topic: str, grade: str,
                                    round_num: int, round_plan: Dict,
                                    key_terms: List[str]) -> str:
    egl = get_english_grade_level(grade)
    activity_type = round_plan.get('precision', {}).get('activity_type', 'spelling and grammar')
    precision_desc = round_plan.get('precision', {}).get('description', '')

    return f"""Create a language accuracy activity for the Precision Station of an Al-HaSadeh English lesson.

**IMPORTANT: ALL output — every word, title, instruction, question, and label — must be in English.**

**Subject:** {subject} | **Topic:** {topic} | **Round {round_num}**
**Grade:** {grade} | **Age:** {egl['age']} | **CEFR:** {egl['cefr']}
**Activity type:** {activity_type} | **Plan:** {precision_desc}
**Words from the text:** {', '.join(key_terms[:12])}
**Number of spelling words for this grade:** {egl['dictation_words']}

**Full language toolkit — choose a variety:**
- Spelling: words and sentences from the text
- Grammar: tenses (present/past/future), subject-verb agreement, articles
- Word forms: noun/verb/adjective/adverb transformations
- Punctuation: capital letters, full stops, commas, apostrophes
- Prepositions: in/on/at/by/with/for/to/from
- Singular/plural: regular and irregular forms
- Sentence types: statement/question/command/exclamation
- Sentence ordering: unscramble sentences
- Error correction: find and fix the mistake
- Collocations: common word pairs from the topic

**Age-appropriate precision options for grade {grade} ({egl['cefr']}):** {', '.join(egl['precision_options'])}

**Rules:**
1. All words/sentences must come from the text read at the Comprehension Station
2. Include {egl['dictation_words']} spelling words
3. Include **2-3 different exercise types** — not only spelling
4. All technical language work (NOT comprehension questions)
5. Variety: each round uses different exercise types from the previous round

**Output format — JSON only (ALL values in English):**
{{
  "title": "Activity title in English",
  "activity_type": "{activity_type}",
  "dictation_list": [
    {{"word": "word", "difficulty": "easy/medium/hard", "note": "note if needed"}}
  ],
  "exercises": [
    {{
      "type": "spelling/grammar/word-forms/punctuation/tenses/prepositions/ordering/error-correction",
      "title": "Exercise title",
      "instruction": "Instruction for the student",
      "items": [
        {{"question": "...", "answer": "..."}}
      ]
    }}
  ],
  "sentences_for_dictation": [
    "Sentence 1 from the text for dictation",
    "Sentence 2 from the text for dictation"
  ],
  "answer_key": "Full answer key"
}}"""


def build_english_vocabulary_prompt(subject: str, topic: str, grade: str,
                                     round_num: int, round_plan: Dict,
                                     key_terms: List[str], used_types: List[str]) -> str:
    egl = get_english_grade_level(grade)
    activity_type = round_plan.get('vocabulary', {}).get('activity_type', 'matching_cards')
    is_physical = round_plan.get('vocabulary', {}).get('is_physical', False)
    vocab_desc = round_plan.get('vocabulary', {}).get('description', '')

    physical_note = """
**⚠️ Physical/experiential activity — guidelines:**
This station is hands-on. The product is:
1. Student instruction sheet (what to do, step by step)
2. Materials list (what needs to be prepared)
3. Word cards for printing and cutting (if needed)
The activity must involve body, hands, movement — "what is felt is remembered"
""" if is_physical else ""

    return f"""Create a vocabulary activity for the Vocabulary Station of an Al-HaSadeh English lesson.

**IMPORTANT: ALL output — every word, title, instruction, question, and label — must be in English.**

**Subject:** {subject} | **Topic:** {topic} | **Round {round_num}**
**Grade:** {grade} | **Age:** {egl['age']} | **CEFR:** {egl['cefr']}
**Activity type:** {activity_type} | **Plan:** {vocab_desc}
**Key words from text:** {', '.join(key_terms[:12])}
**Types already used:** {', '.join(used_types) if used_types else 'none'}
{physical_note}

**Station principle:** "What is felt is remembered" — visual + auditory + kinaesthetic memory

**Printed activity types:**
- matching_cards: cut-and-match cards (word ↔ definition)
- sorting_table: sorting table into categories (cut ↔ paste)
- dominoes: word dominoes for cutting
- fill_in_poster: poster with gaps to fill
- clothesline: connect pairs with a line (synonyms/antonyms)
- idiom_cards: idiom cards + meaning
- definition_table: word | definition | example sentence
- crossword_mini: mini crossword

**Physical/experiential activity types:**
- physical_plasticine: sculpt a word/concept in clay — includes instructions + word list
- physical_model: build a model/diagram — includes instructions + labels to print
- physical_game: card game/memory/dominoes/snakes and ladders — includes board/cards to print
- physical_poster: build a poster/display — includes guiding questions + layout
- physical_simulation: role play/simulation — includes roles + facilitation instructions
- physical_clothesline: "washing line" — hang word cards + pairs (synonyms/antonyms)

**Rules:**
1. Activity is experiential and varied — not just "write a sentence"
2. Words/phrases: from the text + new topic vocabulary
3. Include clear instructions + word bank if relevant
4. Each round — different type (do not repeat what was done)

**Age-appropriate vocabulary options for grade {grade} ({egl['cefr']}):** {', '.join(egl['vocabulary_options'])}

**Output format — JSON only (ALL values in English):**
{{
  "title": "Activity title in English",
  "activity_type": "activity type",
  "is_physical": {str(is_physical).lower()},
  "instruction": "Clear instruction for the student (step by step for physical)",
  "materials_needed": ["material 1", "material 2"],
  "words": [
    {{
      "word": "word/phrase",
      "definition": "short definition",
      "example": "example sentence",
      "category": "category (if relevant)",
      "partner": "synonym/antonym (if relevant)"
    }}
  ],
  "word_bank": ["word1", "word2"],
  "left_column": ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8"],
  "right_column": ["pair1", "pair2", "pair3", "pair4", "pair5", "pair6", "pair7", "pair8"],
  "categories": ["category1", "category2", "category3"],
  "fill_sentences": [
    {{"sentence": "Sentence with a _____ gap", "answer": "the answer"}}
  ],
  "crossword_clues": [
    {{"direction": "across/down", "number": 1, "clue": "clue", "answer": "answer"}}
  ],
  "physical_steps": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "answer_key": "Full answer key"
}}"""


def build_english_teacher_prep_prompt(subject: str, topic: str, grade: str,
                                       round_num: int, all_content: Dict) -> str:
    egl = get_english_grade_level(grade)
    comp = all_content.get('comprehension', {})
    meth = all_content.get('methods', {})
    prec = all_content.get('precision', {})
    vocab = all_content.get('vocabulary', {})
    is_physical_vocab = vocab.get('is_physical', False)

    return f"""Create a teacher preparation sheet for Round {round_num} of an Al-HaSadeh English lesson.

**IMPORTANT: ALL output — every word, title, instruction, question, and label — must be in English.**

**Subject:** {subject} | **Topic:** {topic} | **Grade:** {grade} | **CEFR:** {egl['cefr']} | **Round {round_num}**

**Round stations:**
- Comprehension: {comp.get('section_title', '')} ({len(comp.get('paragraphs', []))} paragraphs) — **oral station only, teacher NOT required here**
- Methods: {meth.get('title', '')} — {meth.get('writing_type', '')} — **teacher sits here**
- Precision: {prec.get('title', '')} — {prec.get('activity_type', '')}
- Vocabulary: {vocab.get('title', '')} — {vocab.get('activity_type', '')} {'(physical activity — materials preparation required)' if is_physical_vocab else '(printed)'}

**Output format — JSON only (ALL values in English):**
{{
  "objectives": {{
    "knowledge": ["knowledge to be gained 1", "knowledge to be gained 2"],
    "skills": ["skill to be developed 1", "skill 2"],
    "values": ["value/habit 1"]
  }},
  "language_focus": ["main grammar/language focus 1", "language focus 2"],
  "materials": {{
    "comprehension": ["copies of the text for each student", "..."],
    "methods": ["task sheet", "..."],
    "precision": ["exercise sheet", "..."],
    "vocabulary": ["required materials — especially for physical: {', '.join(vocab.get('materials_needed', ['activity sheets']))}"]
  }},
  "timing": {{
    "comprehension": "15-20 minutes",
    "methods": "20-25 minutes",
    "precision": "15-20 minutes",
    "vocabulary": "15-20 minutes"
  }},
  "rotation_tip": "Instruction for rotating groups between stations",
  "teacher_notes": [
    "Key point for comprehension station (oral only!)",
    "Key point for methods station (teacher here)",
    "Anticipated difficulty + suggested solution",
    "Suggestion for extension for advanced students"
  ],
  "differentiation": {{
    "struggling": "How to support struggling students at each station",
    "advanced": "Extension for strong students",
    "special_needs": "Adaptations for special education"
  }},
  "self_check": [
    "Is every station fully independent?",
    "Is the comprehension station writing-free?",
    "Is the vocabulary station hands-on/experiential?",
    "Is differentiation built in?"
  ]
}}"""
