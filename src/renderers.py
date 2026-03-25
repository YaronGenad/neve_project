import random
from typing import Dict, List
from .config import STATION_COLORS, get_grade_level, is_english as _is_english_subject


# ─── English-mode UI labels ──────────────────────────────────────────────────
ENGLISH_STATION_NAMES = {
    "comprehension": {"name": "Comprehension Station", "emoji": "🔴"},
    "methods":       {"name": "Methods Station",       "emoji": "🔵"},
    "precision":     {"name": "Precision Station",     "emoji": "🟢"},
    "vocabulary":    {"name": "Vocabulary Station",    "emoji": "🟡"},
    "teacher":       {"name": "Teacher Preparation",   "emoji": "📋"},
    "answers":       {"name": "Answer Key",            "emoji": "🔑"},
}

ENGLISH_LABELS = {
    "student_name":    "Name:",
    "student_class":   "Class:",
    "student_date":    "Date:",
    "round":           "Round",
    "key_terms":       "📌 Key Vocabulary:",
    "discussion":      "💬 Oral Discussion with your group:",
    "discussion_note": "* Discussion questions — oral only, no writing needed!",
    "reading_instr":   "📌 Read the text carefully.",
    "dictation_title": "✏️ Spelling ({n} words)",
    "dictation_note":  "* A partner dictates, you write in the blank row",
    "word":            "Word",
    "spelling":        "Spelling",
    "sentences_title": "📝 Sentences for Dictation (for teacher)",
    "writing_title":   "✏️ Write here:",
    "scaffold_title":  "📝 Writing Structure (scaffold)",
    "guiding_title":   "❓ Guiding Questions",
    "traffic_green":   "🟢 Basic",
    "traffic_yellow":  "🟡 Regular",
    "traffic_red":     "🔴 Challenge",
    "scissors":        "✂️ Cut out all cards, shuffle, and match each word to its definition",
    "word_bank":       "📚 Word Bank:",
    "footer_copy":     "© All rights reserved",
    "teacher_only":    "⚠️ This sheet is for the teacher only — do not distribute to students",
    "answers_only":    "⚠️ Answer Key — for teacher only",
    "materials_title": "🎒 What you need:",
    "steps_title":     "📋 Activity steps:",
    "physical_badge":  "Hands-on Activity",
    "cut_hint":        "✂️ Cut out the cards before the activity",
}


def get_css(station: str = "comprehension") -> str:
    c = STATION_COLORS[station]
    return f"""
    @page {{ size: A4; margin: 1.4cm 1.6cm; }}
    * {{ box-sizing: border-box; }}
    body {{
        font-family: Arial, 'Arial Hebrew', sans-serif;
        direction: rtl;
        line-height: 1.8;
        color: #2c3e50;
        background: white;
        font-size: 13px;
        margin: 0; padding: 0;
    }}
    .page-header {{
        background: linear-gradient(135deg, {c['primary']}, {c['border']});
        color: white;
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .header-left {{ display: flex; align-items: center; gap: 10px; }}
    .header-icon {{
        width: 44px; height: 44px;
        background: rgba(255,255,255,0.25);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
    }}
    .header-title {{ font-size: 18px; font-weight: 800; }}
    .header-subtitle {{ font-size: 12px; opacity: 0.9; }}
    .header-badge {{
        background: rgba(255,255,255,0.2);
        border: 1.5px solid rgba(255,255,255,0.5);
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 13px;
        font-weight: 700;
    }}
    .student-bar {{
        display: flex; gap: 16px;
        margin-bottom: 14px;
        font-size: 12px;
    }}
    .student-field {{
        display: flex; align-items: center; gap: 5px; flex: 1;
    }}
    .student-field label {{ font-weight: 700; color: #555; white-space: nowrap; }}
    .student-line {{
        flex: 1; border-bottom: 1.5px solid #aaa; min-width: 60px; height: 18px;
    }}
    .instruction-box {{
        background: {c['light']};
        border: 2px solid {c['border']};
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 14px;
        font-size: 13px;
        font-weight: 600;
        color: {c['primary']};
    }}
    .section-title {{
        background: {c['primary']};
        color: white;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 700;
        margin: 14px 0 10px 0;
        display: inline-block;
        page-break-after: avoid;
    }}
    .section-block {{
        page-break-inside: avoid;
    }}
    .answer-line {{
        border-bottom: 1.5px solid #bbb;
        height: 22px; width: 100%; margin-bottom: 6px;
    }}
    .writing-box {{
        border: 1.5px solid {c['border']};
        border-radius: 8px;
        padding: 10px;
        min-height: 120px;
        background: #fafafa;
        margin-top: 8px;
        page-break-inside: avoid;
    }}
    .writing-line {{
        border-bottom: 1px solid #ccc;
        height: 24px; width: 100%; margin-bottom: 2px;
    }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; page-break-inside: avoid; }}
    th {{ background: {c['primary']}; color: white; padding: 8px 10px; font-size: 13px; }}
    td {{ border: 1px solid #ddd; padding: 7px 10px; font-size: 12.5px; }}
    tr:nth-child(even) td {{ background: {c['light']}; }}
    .word-bank {{
        background: #fffde7;
        border: 1.5px dashed #f39c12;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 12px;
        font-size: 12px;
    }}
    .word-pill {{
        display: inline-block;
        background: {c['light']};
        border: 1.5px solid {c['border']};
        color: {c['primary']};
        padding: 2px 12px;
        border-radius: 14px;
        margin: 2px 3px;
        font-size: 12px;
        font-weight: 700;
    }}
    .key-term {{
        font-weight: 700;
        color: {c['primary']};
        background: {c['light']};
        padding: 1px 4px;
        border-radius: 3px;
    }}
    .cards-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-top: 10px;
    }}
    .cut-card {{
        border: 2.5px dashed {c['border']};
        border-radius: 8px;
        padding: 10px;
        min-height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 12px;
        background: {c['light']};
    }}
    .cut-card-term {{
        font-weight: 800;
        font-size: 14px;
        color: {c['primary']};
    }}
    .cut-card-def {{
        font-size: 11px;
        color: #555;
        background: white;
    }}
    .scissors-hint {{
        font-size: 11px; color: #888; margin-top: 6px;
        text-align: center; font-style: italic;
    }}
    .match-container {{
        display: grid;
        grid-template-columns: 1fr 40px 1fr;
        gap: 6px;
        align-items: center;
        margin-bottom: 6px;
    }}
    .match-left {{
        background: {c['light']};
        border: 2px solid {c['border']};
        border-radius: 6px;
        padding: 7px 10px;
        font-weight: 700;
        font-size: 12px;
        text-align: center;
        color: {c['primary']};
    }}
    .match-right {{
        background: white;
        border: 2px solid #bbb;
        border-radius: 6px;
        padding: 7px 10px;
        font-size: 11.5px;
        text-align: center;
        color: #444;
    }}
    .match-line-area {{
        text-align: center;
        font-size: 18px;
        color: #ccc;
    }}
    .sort-categories {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 10px;
        margin-top: 12px;
    }}
    .sort-box {{
        border: 2.5px solid {c['border']};
        border-radius: 8px;
        min-height: 100px;
        padding: 8px;
    }}
    .sort-box-title {{
        background: {c['primary']};
        color: white;
        border-radius: 5px;
        padding: 4px 8px;
        font-size: 12px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
    }}
    .traffic-light {{
        display: flex; gap: 8px; margin: 10px 0;
        page-break-inside: avoid;
    }}
    .tl-green {{ background: #d5f5e3; border: 1.5px solid #27ae60; border-radius: 6px; padding: 6px 10px; font-size: 12px; flex: 1; }}
    .tl-yellow {{ background: #fef9e7; border: 1.5px solid #f1c40f; border-radius: 6px; padding: 6px 10px; font-size: 12px; flex: 1; }}
    .tl-red {{ background: #fadbd8; border: 1.5px solid #e74c3c; border-radius: 6px; padding: 6px 10px; font-size: 12px; flex: 1; }}
    .tl-label {{ font-size: 10px; font-weight: 700; margin-bottom: 3px; }}
    .page-footer {{
        text-align: center; font-size: 10px; color: #aaa;
        border-top: 1px solid #eee; padding-top: 6px; margin-top: 20px;
    }}
    .page-break {{ page-break-before: always; }}
    .physical-badge {{
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 12px;
    }}
    .materials-box {{
        background: #fef9e7;
        border: 2px dashed #f39c12;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 14px;
    }}
    .materials-box-title {{
        font-weight: 700;
        font-size: 13px;
        color: #e67e22;
        margin-bottom: 6px;
    }}
    .materials-list {{
        list-style: none;
        padding: 0; margin: 0;
        display: flex; flex-wrap: wrap; gap: 6px;
    }}
    .materials-list li {{
        background: white;
        border: 1.5px solid #f39c12;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 12px;
        color: #555;
    }}
    .steps-box {{
        background: #f8f9fa;
        border: 2px solid {c['border']};
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 14px;
        page-break-inside: avoid;
    }}
    .steps-box-title {{
        font-weight: 700;
        font-size: 13px;
        color: {c['primary']};
        margin-bottom: 8px;
    }}
    .steps-list {{
        list-style: none;
        padding: 0; margin: 0;
        counter-reset: step-counter;
    }}
    .steps-list li {{
        counter-increment: step-counter;
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 8px;
        font-size: 13px;
    }}
    .steps-list li::before {{
        content: counter(step-counter);
        background: {c['primary']};
        color: white;
        border-radius: 50%;
        min-width: 22px;
        height: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 700;
        flex-shrink: 0;
    }}
    .word-cards-print {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-top: 10px;
    }}
    .word-card-print {{
        border: 2.5px dashed {c['border']};
        border-radius: 8px;
        padding: 10px 8px;
        text-align: center;
        background: {c['light']};
        page-break-inside: avoid;
    }}
    .word-card-term {{
        font-weight: 800;
        font-size: 14px;
        color: {c['primary']};
        margin-bottom: 4px;
    }}
    .word-card-def {{
        font-size: 10.5px;
        color: #666;
        border-top: 1px dashed #ccc;
        padding-top: 4px;
        margin-top: 4px;
    }}
    """


def render_header(title: str, round_num: int, station: str,
                  include_student_bar: bool = True, english_mode: bool = False) -> str:
    c = STATION_COLORS[station]
    if english_mode:
        en = ENGLISH_STATION_NAMES.get(station, {"name": c['name'], "emoji": c['emoji']})
        station_name = en['name']
        station_emoji = en['emoji']
        lbl = ENGLISH_LABELS
        round_label = f"{lbl['round']} {round_num}"
    else:
        station_name = c['name']
        station_emoji = c['emoji']
        round_label = f"סבב {round_num}"

    student_bar = ""
    if include_student_bar:
        if english_mode:
            student_bar = f"""
            <div class="student-bar">
                <div class="student-field"><label>{ENGLISH_LABELS['student_name']}</label><div class="student-line"></div></div>
                <div class="student-field"><label>{ENGLISH_LABELS['student_class']}</label><div class="student-line"></div></div>
                <div class="student-field"><label>{ENGLISH_LABELS['student_date']}</label><div class="student-line"></div></div>
            </div>
            """
        else:
            student_bar = """
            <div class="student-bar">
                <div class="student-field"><label>שם:</label><div class="student-line"></div></div>
                <div class="student-field"><label>כיתה:</label><div class="student-line"></div></div>
                <div class="student-field"><label>תאריך:</label><div class="student-line"></div></div>
            </div>
            """
    return f"""
    <div class="page-header">
        <div class="header-left">
            <div class="header-icon">{station_emoji}</div>
            <div>
                <div class="header-title">{station_name}</div>
                <div class="header-subtitle">{title}</div>
            </div>
        </div>
        <div class="header-badge">{round_label}</div>
    </div>
    {student_bar}
    """


def render_comprehension(title: str, round_num: int, data: Dict, grade: str,
                          english_mode: bool = False) -> str:
    gl = get_grade_level(grade)

    paras_html = ""
    for p in data.get('paragraphs', []):
        text = p.get('text', '')
        for term in p.get('key_terms', []):
            if term and len(term) > 1:
                text = text.replace(term, f'<span class="key-term">{term}</span>', 1)
        paras_html += f"""
        <div style="margin-bottom: 14px;">
            <div style="font-weight: 700; color: #c0392b; font-size: 14px; margin-bottom: 4px;">{p.get('subtitle', '')}</div>
            <div style="font-size: 13.5px; line-height: 1.9; text-align: justify;">{text}</div>
        </div>
        """

    pills = "".join([f'<span class="word-pill">{t}</span>' for t in data.get('all_key_terms', [])])

    disc_items = "".join([f'<li style="margin-bottom:5px;">{q}</li>' for q in data.get('discussion_starters', [])])

    if english_mode:
        lbl = ENGLISH_LABELS
        disc_box = f"""
        <div class="section-block" style="background:#fadbd8; border:2px solid #e74c3c; border-radius:8px; padding:10px 14px; margin-top:14px;">
            <div style="font-weight:700; color:#c0392b; margin-bottom:6px;">{lbl['discussion']}</div>
            <ul style="margin:0; padding-left:20px; font-size:13px;">{disc_items}</ul>
            <div style="font-size:11px; color:#888; margin-top:6px; font-style:italic;">{lbl['discussion_note']}</div>
        </div>
        """
        reading_instruction = lbl['reading_instr']
        key_terms_label = lbl['key_terms']
        html_dir = "ltr"
        html_lang = "en"
        page_title = f"Comprehension Station - {title} - Round {round_num}"
        footer_text = f"Al-HaSadeh | Comprehension Station | {title} | Round {round_num} — {lbl['footer_copy']}"
    else:
        disc_box = f"""
        <div class="section-block" style="background:#fadbd8; border:2px solid #e74c3c; border-radius:8px; padding:10px 14px; margin-top:14px;">
            <div style="font-weight:700; color:#c0392b; margin-bottom:6px;">💬 לדיון בעל פה עם הקבוצה:</div>
            <ul style="margin:0; padding-right:20px; font-size:13px;">{disc_items}</ul>
            <div style="font-size:11px; color:#888; margin-top:6px; font-style:italic;">* שאלות לדיון בעל פה בלבד — אין צורך לכתוב!</div>
        </div>
        """
        key_terms_label = "📌 מונחי מפתח:"
        html_dir = "rtl"
        html_lang = "he"
        page_title = f"תחנת הבנה - {title} - סבב {round_num}"

    is_steam = data.get('is_steam', False)
    input_type_labels = {
        'text': '📄 קרא/י את הטקסט המדעי',
        'video': '🎬 צפה/י בסרטון + ענה/י על שאלות ההכוונה',
        'observation': '🔬 בצע/י תצפית מונחת ותעד/י',
        'experiment': '⚗️ בצע/י את הניסוי הקצר + שוחח/י על מה שראית',
        'multi_source': '📊 קרא/י את החומרים + נתח/י את הגרפים',
    }
    if english_mode:
        reading_instruction = ENGLISH_LABELS['reading_instr']
    elif is_steam:
        input_type = data.get('input_type', 'text')
        reading_instruction = input_type_labels.get(input_type, f"📌 {gl['reading_mode']}")
    else:
        reading_instruction = f"📌 {gl['reading_mode']}"

    if not english_mode:
        footer_text = f"א\"ל השד\"ה{' STEAM' if is_steam else ''} | תחנת הבנה | {title} | סבב {round_num} — © כל הזכויות שמורות"

    # KWL table (STEAM only)
    kwl = data.get('kwl_table', {})
    kwl_html = ""
    if kwl and not english_mode:
        know_items = "".join([f'<div class="answer-line" style="margin-bottom:4px;"></div>' for _ in range(len(kwl.get('know_prompts', [])) + 1)])
        wonder_items = "".join([f'<div class="answer-line" style="margin-bottom:4px;"></div>' for _ in range(len(kwl.get('wonder_prompts', [])) + 1)])
        know_prompts = "".join([f'<div style="font-size:11px;color:#888;font-style:italic;margin-bottom:2px;">{p}</div>' for p in kwl.get('know_prompts', [])])
        wonder_prompts = "".join([f'<div style="font-size:11px;color:#888;font-style:italic;margin-bottom:2px;">{p}</div>' for p in kwl.get('wonder_prompts', [])])
        kwl_html = f"""
        <div class="section-block" style="margin-bottom:14px;">
            <div class="section-title">📋 טבלת KWL — לפני הקריאה</div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-top:8px;">
                <div style="background:#d5f5e3; border:1.5px solid #27ae60; border-radius:8px; padding:10px;">
                    <div style="font-weight:800; color:#1e8449; margin-bottom:6px; font-size:12px;">✅ יודע/ת</div>
                    {know_prompts}{know_items}
                </div>
                <div style="background:#d6eaf8; border:1.5px solid #2980b9; border-radius:8px; padding:10px;">
                    <div style="font-weight:800; color:#1a5276; margin-bottom:6px; font-size:12px;">❓ רוצה לדעת</div>
                    {wonder_prompts}{wonder_items}
                </div>
                <div style="background:#fef9e7; border:1.5px solid #f1c40f; border-radius:8px; padding:10px;">
                    <div style="font-weight:800; color:#7d6608; margin-bottom:6px; font-size:12px;">💡 למדתי</div>
                    <div style="font-size:11px; color:#888; font-style:italic; margin-bottom:4px;">— ימולא לאחר הפעילות —</div>
                    <div class="answer-line"></div><div class="answer-line"></div><div class="answer-line"></div>
                </div>
            </div>
        </div>"""

    # Short written response (STEAM only)
    wr = data.get('written_response', {})
    written_response_html = ""
    if wr and not english_mode:
        written_response_html = f"""
        <div class="section-block" style="margin-bottom:14px; background:#eafaf1; border:2px solid #27ae60; border-radius:8px; padding:12px 14px;">
            <div style="font-weight:700; color:#1e8449; margin-bottom:6px;">✍️ {wr.get('instruction', 'כתוב/כתבי תשובה קצרה (1-3 משפטים)')}</div>
            <div style="font-size:13px; font-weight:600; margin-bottom:8px;">{wr.get('question', '')}</div>
            <div style="font-size:11.5px; color:#888; font-style:italic; margin-bottom:8px;">פיגום: {wr.get('scaffold', '')}</div>
            <div class="answer-line"></div><div class="answer-line"></div><div class="answer-line"></div>
        </div>"""

    return f"""<!DOCTYPE html>
<html dir="{html_dir}" lang="{html_lang}">
<head><meta charset="UTF-8"><title>{page_title}</title>
<style>{get_css('comprehension')}</style></head>
<body>
{render_header(title, round_num, 'comprehension', english_mode=english_mode)}
<div class="instruction-box">{reading_instruction}</div>
{kwl_html}
<div style="background:#fafafa; border:1px solid #ddd; border-radius:10px; padding:18px 22px;">
    <div style="font-size:22px; font-weight:800; color:#c0392b; text-align:center; margin-bottom:6px;">{data.get('section_title', '')}</div>
    <div style="font-size:14px; font-style:italic; text-align:center; color:#555; border-bottom:1px solid #eee; padding-bottom:10px; margin-bottom:14px;">{data.get('intro_sentence') or data.get('intro_question', '')}</div>
    {paras_html}
    <div style="background:#fadbd8; border:1.5px solid #e74c3c; border-radius:6px; padding:8px 12px; margin-top:12px; font-size:12px;">
        <strong style="color:#c0392b;">{key_terms_label}</strong><br>{pills}
    </div>
</div>
{written_response_html}
{disc_box}
<div class="page-footer">{footer_text}</div>
</body></html>"""


def render_methods(title: str, round_num: int, data: Dict, english_mode: bool = False) -> str:
    lines_html = "".join([f'<div class="writing-line"></div>' for _ in range(data.get('lines_needed', 10))])

    dl = data.get('difficulty_levels', {})
    if english_mode:
        lbl = ENGLISH_LABELS
        traffic = f"""
        <div class="traffic-light">
            <div class="tl-green"><div class="tl-label">{lbl['traffic_green']}</div>{dl.get('green', '')}</div>
            <div class="tl-yellow"><div class="tl-label">{lbl['traffic_yellow']}</div>{dl.get('yellow', '')}</div>
            <div class="tl-red"><div class="tl-label">{lbl['traffic_red']}</div>{dl.get('red', '')}</div>
        </div>
        """
        scaffold_title = "📝 Writing Structure (scaffold)"
        write_title = "✏️ Write here:"
        guiding_title = "❓ Guiding Questions"
        scope_label = "Scope:"
        footer_text = f"Al-HaSadeh | Methods Station | {title} | Round {round_num} — {lbl['footer_copy']}"
        html_dir = "ltr"
        html_lang = "en"
        page_title = f"Methods Station - {title} - Round {round_num}"
        list_padding = "padding-left:20px;"
    else:
        traffic = f"""
        <div class="traffic-light">
            <div class="tl-green"><div class="tl-label">🟢 בסיסי</div>{dl.get('green', '')}</div>
            <div class="tl-yellow"><div class="tl-label">🟡 רגיל</div>{dl.get('yellow', '')}</div>
            <div class="tl-red"><div class="tl-label">🔴 מאתגר</div>{dl.get('red', '')}</div>
        </div>
        """
        scope_label = "היקף:"
        guiding_title = "❓ שאלות מנחות"
        html_dir = "rtl"
        html_lang = "he"
        page_title = f"תחנת שיטות - {title} - סבב {round_num}"
        list_padding = "padding-right:20px;"

    guiding = "".join([f'<li style="margin-bottom:4px;">{q}</li>' for q in data.get('guiding_questions', [])])
    scaffold = data.get('scaffold_template', '').replace('\n', '<br>')

    # STEAM: framework steps + context data
    framework_steps = data.get('framework_steps', [])
    fw_steps_html = ""
    if framework_steps:
        fw_label = {
            'scientific_method': '🔬 מתודה מדעית',
            'EDP': '🏗️ תהליך תיכון הנדסי (EDP)',
            'data_analysis': '📊 ניתוח נתונים',
            'mathematical_thinking': '📐 חשיבה מתמטית',
            'art_design': '🎨 חשיבה עיצובית',
        }.get(data.get('thinking_framework', ''), '🔬 מסגרת חשיבה')
        steps_li = "".join([f"<li>{s}</li>" for s in framework_steps])
        fw_steps_html = f"""
        <div class="section-block" style="margin-bottom:12px;">
            <div class="section-title">{fw_label} — שלבי העבודה</div>
            <ol style="font-size:12.5px; padding-right:20px; margin-top:6px;">{steps_li}</ol>
        </div>"""

    context_data = data.get('context_data', '')
    context_html = ""
    if context_data:
        context_html = f"""
        <div class="section-block" style="margin-bottom:12px; background:#fef9e7; border:2px solid #f39c12; border-radius:8px; padding:10px 14px;">
            <div style="font-weight:700; color:#e67e22; margin-bottom:6px;">📊 נתונים / הקשר לניתוח:</div>
            <div style="font-size:12.5px; line-height:1.8;">{context_data.replace(chr(10), '<br>')}</div>
        </div>"""

    is_steam = bool(framework_steps or context_data)
    if english_mode:
        scaffold_title = "📝 Writing Structure (scaffold)"
        write_title = "✏️ Write here:"
    elif is_steam:
        scaffold_title = "📝 מסגרת / פיגום לחשיבה"
        write_title = "✏️ כתוב/כתבי את הניתוח/הדוח/הפתרון:"
        footer_text = f"א\"ל השד\"ה STEAM | תחנת שיטות | {title} | סבב {round_num} — © כל הזכויות שמורות"
    else:
        scaffold_title = "📝 מבנה הכתיבה (פיגום)"
        write_title = "✏️ כתוב/כתבי כאן:"
        footer_text = f"א\"ל השד\"ה | תחנת שיטות | {title} | סבב {round_num} — © כל הזכויות שמורות"

    return f"""<!DOCTYPE html>
<html dir="{html_dir}" lang="{html_lang}">
<head><meta charset="UTF-8"><title>{page_title}</title>
<style>{get_css('methods')}</style></head>
<body>
{render_header(title, round_num, 'methods', english_mode=english_mode)}
<div class="instruction-box">📌 {data.get('main_instruction', '')}</div>

<div style="background:#d6eaf8; border:2px solid #2980b9; border-radius:8px; padding:10px 14px; margin-bottom:12px;">
    <div style="font-weight:700; font-size:14px; color:#1a5276; margin-bottom:6px;">✏️ {data.get('context_prompt', '')}</div>
    <div style="font-size:12px; color:#555;">{scope_label} {data.get('words_range', '')}</div>
</div>

{fw_steps_html}
{context_html}
{traffic}

<div class="section-block" style="margin-bottom:12px;">
    <div class="section-title">{guiding_title}</div>
    <ul style="font-size:13px; {list_padding} margin-top:6px;">{guiding}</ul>
</div>

<div class="section-block" style="margin-bottom:10px;">
    <div class="section-title">{scaffold_title}</div>
    <div style="background:#eaf3fb; border:1px solid #2980b9; border-radius:6px; padding:10px; font-size:12.5px; margin-top:6px; line-height:1.7;">{scaffold}</div>
</div>

<div class="section-block">
    <div class="section-title">{write_title}</div>
    <div class="writing-box">{lines_html}</div>
</div>

<div class="page-footer">{footer_text}</div>
</body></html>"""


def render_precision(title: str, round_num: int, data: Dict, english_mode: bool = False) -> str:
    # ── STEAM HANDS-ON branch ──────────────────────────────────────
    if data.get('is_hands_on'):
        return _render_stem_precision(title, round_num, data)

    # ── Language / English grammar branch ─────────────────────────
    if english_mode:
        lbl = ENGLISH_LABELS
        diff_color = {"easy": "#d5f5e3", "medium": "#fef9e7", "hard": "#fadbd8",
                      "קל": "#d5f5e3", "בינוני": "#fef9e7", "קשה": "#fadbd8"}
        dictation_title = lbl['dictation_title']
        dictation_note = lbl['dictation_note']
        word_th = lbl['word']
        spelling_th = lbl['spelling']
        sentences_title = lbl['sentences_title']
        instruction_suffix = "Work in pairs: one dictates, the other writes — then swap."
        html_dir = "ltr"
        html_lang = "en"
        page_title = f"Precision Station - {title} - Round {round_num}"
        footer_text = f"Al-HaSadeh | Precision Station | {title} | Round {round_num} — {lbl['footer_copy']}"
        list_padding = "padding-left:20px;"
    else:
        diff_color = {"קל": "#d5f5e3", "בינוני": "#fef9e7", "קשה": "#fadbd8"}
        dictation_title = "✏️ הכתבה ({n} מילים)"
        dictation_note = "* עמית/ה מכתיב/ה, אתה/את כותב/ת בשורה הריקה"
        word_th = "מילה"
        spelling_th = "הכתבה"
        sentences_title = "📝 הכתבת משפטים (למורה)"
        instruction_suffix = "עבוד/י בזוגות: אחד/ת מכתיב/ה, השני/ה כותב/ת ומחליפים."
        html_dir = "rtl"
        html_lang = "he"
        page_title = f"תחנת דיוק - {title} - סבב {round_num}"
        footer_text = f"א\"ל השד\"ה | תחנת דיוק | {title} | סבב {round_num} — © כל הזכויות שמורות"
        list_padding = "padding-right:20px;"

    dict_items = data.get('dictation_list', [])
    dict_rows = ""
    for i in range(0, len(dict_items), 2):
        w1 = dict_items[i] if i < len(dict_items) else {}
        w2 = dict_items[i + 1] if i + 1 < len(dict_items) else {}
        c1 = diff_color.get(w1.get('difficulty', 'בינוני'), '#fff')
        c2 = diff_color.get(w2.get('difficulty', 'בינוני'), '#fff')
        note1 = f"<br><span style='font-size:10px;color:#888;'>{w1.get('note', '')}</span>" if w1.get('note') else ""
        note2 = f"<br><span style='font-size:10px;color:#888;'>{w2.get('note', '')}</span>" if w2.get('note') else ""
        dict_rows += f"""
        <tr>
            <td style="text-align:center; background:{c1}; font-weight:700;">{i + 1}. {w1.get('word', '')}{note1}</td>
            <td style="min-width:120px;"></td>
            <td style="text-align:center; background:{c2}; font-weight:700;">{i + 2}. {w2.get('word', '')}{note2}</td>
            <td style="min-width:120px;"></td>
        </tr>
        """

    dictation_html = f"""
    <div class="section-block">
    <div class="section-title">✏️ {dictation_title.format(n=len(dict_items))}</div>
    <div style="font-size:11px; color:#888; margin-bottom:6px;">{dictation_note}</div>
    <table><tr><th>{word_th}</th><th>{spelling_th}</th><th>{word_th}</th><th>{spelling_th}</th></tr>{dict_rows}</table>
    </div>
    """ if dict_items else ""

    exercises_html = ""
    for ex in data.get('exercises', []):
        items_html = ""
        for item in ex.get('items', []):
            items_html += f"""
            <div style="display:flex; align-items:flex-start; gap:8px; margin-bottom:10px;">
                <div style="font-size:13px; flex:1; font-weight:600;">{item.get('question', '')}</div>
                <div style="flex:2; border-bottom:1.5px solid #aaa; min-height:20px;"></div>
            </div>
            """
        exercises_html += f"""
        <div class="section-block" style="margin-bottom:16px;">
            <div class="section-title">{ex.get('title', '')}</div>
            <div style="font-size:12.5px; color:#555; margin:6px 0 10px 0; font-style:italic;">{ex.get('instruction', '')}</div>
            {items_html}
        </div>
        """

    sent_html = ""
    if data.get('sentences_for_dictation'):
        sents = "".join([f'<li style="margin-bottom:3px;">{s}</li>' for s in data.get('sentences_for_dictation', [])])
        sent_html = f"""
        <div style="margin-top:14px;">
            <div class="section-title">📝 {sentences_title}</div>
            <ol style="font-size:12.5px; {list_padding} color:#555;">{sents}</ol>
        </div>
        """

    return f"""<!DOCTYPE html>
<html dir="{html_dir}" lang="{html_lang}">
<head><meta charset="UTF-8"><title>{page_title}</title>
<style>{get_css('precision')}</style></head>
<body>
{render_header(title, round_num, 'precision', english_mode=english_mode)}
<div class="instruction-box">📌 {data.get('title', '')} — {instruction_suffix}</div>
{dictation_html}
{exercises_html}
{sent_html}
<div class="page-footer">{footer_text}</div>
</body></html>"""


def _render_stem_precision(title: str, round_num: int, data: Dict) -> str:
    """Renders the STEAM HANDS-ON lab card for the precision station."""
    c = STATION_COLORS['precision']

    type_badges = {
        'science_experiment': ('🔬', 'ניסוי מדעי'),
        'measurement_data': ('📏', 'מדידות ואיסוף נתונים'),
        'engineering_building': ('🏗️', 'בנייה הנדסית'),
        'math_hands_on': ('📐', 'מתמטיקה מוחשית'),
        'art_design': ('🎨', 'יצירה ועיצוב מדעי'),
    }
    emoji, label = type_badges.get(data.get('hands_on_type', ''), ('🔬', 'פעילות מדעית'))

    # Background box
    bg_html = ""
    if data.get('background_mini'):
        bg_html = f"""
        <div style="background:#eafaf1; border:1.5px solid #27ae60; border-radius:8px; padding:10px 14px; margin-bottom:12px; font-size:12.5px;">
            <strong style="color:#1e8449;">📖 רקע קצר:</strong> {data['background_mini']}
        </div>"""

    # Research question + hypothesis
    rq_html = f"""
    <div class="section-block" style="margin-bottom:12px;">
        <div class="section-title">❓ שאלת החקירה</div>
        <div style="font-size:14px; font-weight:700; color:#1e8449; padding:8px 0;">{data.get('research_question', '')}</div>
        <div style="font-size:12.5px; color:#555; font-style:italic;">ההשערה שלי: {data.get('hypothesis_scaffold', '_____ כי _____')}</div>
        <div class="answer-line" style="margin-top:6px;"></div>
    </div>"""

    # Materials
    materials = data.get('materials_needed', [])
    safety = data.get('safety_notes', [])
    mat_items = "".join([f"<li>{m}</li>" for m in materials])
    safety_items = "".join([f"<li style='color:#c0392b;'>⚠️ {s}</li>" for s in safety])
    mat_html = ""
    if materials:
        mat_html = f"""
        <div class="materials-box">
            <div class="materials-box-title">🎒 מה צריך להכין:</div>
            <ul class="materials-list">{mat_items}</ul>
            {f'<ul style="padding:6px 0 0 0; margin:0; list-style:none; font-size:11.5px;">{safety_items}</ul>' if safety else ''}
        </div>"""

    # Steps
    steps = data.get('steps', [])
    steps_li = "".join([f"<li>{s}</li>" for s in steps])
    steps_html = f"""
    <div class="steps-box">
        <div class="steps-box-title">📋 שלבי הפעילות:</div>
        <ol class="steps-list">{steps_li}</ol>
    </div>""" if steps else ""

    # Data table
    dt = data.get('data_table', {})
    headers = dt.get('headers', [])
    rows = dt.get('rows', [])
    table_html = ""
    if headers:
        th_html = "".join([f"<th>{h}</th>" for h in headers])
        tr_html = "".join([
            "<tr>" + "".join([f"<td style='min-height:28px; height:28px;'>{cell}</td>" for cell in row]) + "</tr>"
            for row in rows
        ])
        table_html = f"""
        <div class="section-block" style="margin-bottom:12px;">
            <div class="section-title">📊 טבלת תיעוד תוצאות</div>
            <table style="margin-top:8px;"><tr>{th_html}</tr>{tr_html}</table>
        </div>"""

    # Analysis questions
    analysis = data.get('analysis_questions', [])
    analysis_html = ""
    if analysis:
        q_items = "".join([f"""
        <div style="margin-bottom:12px;">
            <div style="font-size:13px; font-weight:600; color:#1e8449;">{q.get('question', '')}</div>
            <div class="answer-line"></div><div class="answer-line"></div>
        </div>""" for q in analysis])
        analysis_html = f"""
        <div class="section-block" style="margin-bottom:12px;">
            <div class="section-title">🔍 שאלות ניתוח</div>
            {q_items}
        </div>"""

    # Conclusion scaffold
    conc = data.get('conclusion_scaffold', '')
    conc_html = f"""
    <div class="section-block" style="margin-bottom:12px;">
        <div class="section-title">💡 מסקנה</div>
        <div style="font-size:12.5px; color:#555; margin:6px 0 8px; font-style:italic;">{conc}</div>
        <div class="answer-line"></div><div class="answer-line"></div>
    </div>""" if conc else ""

    # Difficulty levels
    dl = data.get('difficulty_levels', {})
    traffic_html = f"""
    <div class="traffic-light">
        <div class="tl-green"><div class="tl-label">🟢 בסיסי</div>{dl.get('green', '')}</div>
        <div class="tl-yellow"><div class="tl-label">🟡 רגיל</div>{dl.get('yellow', '')}</div>
        <div class="tl-red"><div class="tl-label">🔴 מאתגר</div>{dl.get('red', '')}</div>
    </div>""" if dl else ""

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head><meta charset="UTF-8"><title>תחנת דיוק STEAM - {title} - סבב {round_num}</title>
<style>{get_css('precision')}</style></head>
<body>
{render_header(title, round_num, 'precision')}
<div class="instruction-box">
    <span style="background:{c['primary']}; color:white; padding:3px 10px; border-radius:12px; font-size:12px; margin-left:8px;">{emoji} {label}</span>
    📌 {data.get('title', '')} — תחנת HANDS-ON: בצע/י את הפעילות ותעד/י את הממצאים
</div>
{bg_html}
{rq_html}
{mat_html}
{steps_html}
{table_html}
{analysis_html}
{conc_html}
{traffic_html}
<div class="page-footer">א"ל השד"ה STEAM | תחנת דיוק HANDS-ON | {title} | סבב {round_num} — © כל הזכויות שמורות</div>
</body></html>"""


def render_vocabulary(title: str, round_num: int, data: Dict, english_mode: bool = False) -> str:
    # ── STEAM bilingual game branch ────────────────────────────────
    activity_type = data.get('activity_type') or data.get('game_type', 'matching_cards')
    if activity_type.startswith('stem_') or data.get('bilingual'):
        return _render_stem_vocabulary(title, round_num, data)
    # ── Language / English vocabulary branch ──────────────────────
    words = data.get('words', [])
    word_bank = data.get('word_bank', [w.get('word', '') for w in words[:8]])
    left_col = data.get('left_column', [])
    right_col = data.get('right_column', []).copy()
    categories = data.get('categories', [])

    # Localised labels
    if english_mode:
        lbl = ENGLISH_LABELS
        html_dir = "ltr"
        html_lang = "en"
        page_title = f"Vocabulary Station - {title} - Round {round_num}"
        footer_text = f"Al-HaSadeh | Vocabulary Station | {title} | Round {round_num} — {lbl['footer_copy']}"
        cards_title = "✂️ Word Cards (cut out)"
        defs_title = "✂️ Definition Cards (cut out — shuffled!)"
        scissors_hint = lbl['scissors']
        clothesline_hint = "💡 Draw a line to connect each word (right column) to its definition/opposite/synonym (left column)"
        sort_words_title = "✂️ Words to Sort (cut out)"
        sort_paste_title = "📋 Paste each word in the correct category:"
        word_bank_label = lbl['word_bank']
        def_table_headers = "<tr><th>Word</th><th>Definition</th><th>Write your own sentence</th></tr>"
        crossword_across = "↔️ Across"
        crossword_down = "↕️ Down"
        crossword_placeholder = "[Crossword grid — draw or print manually]"
        physical_labels = {
            'physical_plasticine': ('🧱', 'Clay Sculpting'),
            'physical_model':      ('🏗️', 'Model Building'),
            'physical_game':       ('🃏', 'Card / Board Game'),
            'physical_poster':     ('🖼️', 'Poster / Display'),
            'physical_simulation': ('🎭', 'Role Play / Simulation'),
            'physical_clothesline':('🪢', 'Washing Line — Pair Matching'),
        }
        physical_badge_prefix = "Hands-on Activity"
        materials_title = lbl['materials_title']
        steps_title = lbl['steps_title']
        word_cards_title = "✂️ Word Cards for Printing and Cutting"
        cut_hint = lbl['cut_hint']
        dominoes_hint = "✂️ Cut out the cards and connect the end of one card to the start of the next (word → definition)"
        list_padding = "padding-left:18px;"
    else:
        html_dir = "rtl"
        html_lang = "he"
        page_title = f"תחנת אוצר מילים - {title} - סבב {round_num}"
        footer_text = f"א\"ל השד\"ה | תחנת הרחבת אוצר מילים | {title} | סבב {round_num} — © כל הזכויות שמורות"
        cards_title = "✂️ קלפי מושגים (גזור)"
        defs_title = "✂️ קלפי הגדרות (גזור — מעורבבים!)"
        scissors_hint = "✂️ גזור את כל הקלפים, ערבב, וחבר כל מושג להגדרה שלו"
        clothesline_hint = "💡 חבר/י בקו כל מושג (עמודה ימין) להגדרה/הפך/נרדפת שלו (עמודה שמאל)"
        sort_words_title = "✂️ מילים למיון (גזור)"
        sort_paste_title = "📋 הדבק כל מילה בקטגוריה הנכונה:"
        word_bank_label = "📚 בנק מילים:"
        def_table_headers = "<tr><th>מילה</th><th>הגדרה</th><th>כתוב משפט משלך</th></tr>"
        crossword_across = "↔️ מאוזן"
        crossword_down = "↕️ מאונך"
        crossword_placeholder = "[תשבץ — ציירו/הדפיסו ידנית]"
        physical_labels = {
            'physical_plasticine': ('🧱', 'פיסול בפלסטלינה / בצק'),
            'physical_model':      ('🏗️', 'בניית מודל / דיאגרמה'),
            'physical_game':       ('🃏', 'משחק קלפים / זכרון / לוח'),
            'physical_poster':     ('🖼️', 'בניית כרזה / תערוכה'),
            'physical_simulation': ('🎭', 'משחק תפקידים / סימולציה'),
            'physical_clothesline':('🪢', 'חבל כביסה — התאמת זוגות'),
        }
        physical_badge_prefix = "פעילות חווייתית"
        materials_title = "🎒 מה צריך להכין:"
        steps_title = "📋 שלבי הפעילות:"
        word_cards_title = "✂️ קלפי מילים להדפסה וגזירה"
        cut_hint = "גזרו את הקלפים לפני הפעילות"
        dominoes_hint = "✂️ גזור את הקלפים וחבר סוף קלף אחד לתחילת הקלף הבא (מושג → הגדרה)"
        list_padding = "padding-right:18px;"

    body_html = ""

    if activity_type in ("matching_cards", "idiom_cards"):
        term_cards = "".join([
            f'<div class="cut-card cut-card-term">{w.get("word", "")}\n'
            f'<div style="font-size:10px;color:#888;font-weight:400;">{w.get("example", "")[:40]}</div></div>'
            for w in words
        ])
        def_cards_shuffled = words.copy()
        random.shuffle(def_cards_shuffled)
        def_cards = "".join([f'<div class="cut-card cut-card-def">{w.get("definition", "")}</div>' for w in def_cards_shuffled])
        body_html = f"""
        <div class="section-title">{cards_title}</div>
        <div class="cards-grid">{term_cards}</div>
        <div class="section-title" style="margin-top:12px;">{defs_title}</div>
        <div class="cards-grid">{def_cards}</div>
        <div class="scissors-hint">{scissors_hint}</div>
        """

    elif activity_type == "clothesline":
        if not left_col:
            left_col = [w.get('word', '') for w in words]
        if not right_col:
            right_col = [w.get('partner', w.get('definition', '')) for w in words]
        random.shuffle(right_col)
        match_html = ""
        for i in range(min(len(left_col), len(right_col))):
            match_html += f"""
            <div class="match-container">
                <div class="match-left">{left_col[i]}</div>
                <div class="match-line-area">—</div>
                <div class="match-right">{right_col[i]}</div>
            </div>
            """
        body_html = f"""
        <div style="font-size:12px; color:#888; margin-bottom:10px; background:#fffde7; padding:8px; border-radius:6px;">
            {clothesline_hint}
        </div>
        {match_html}
        """

    elif activity_type == "sorting_table":
        pills = "".join([f'<span class="word-pill">{w.get("word", "")} ✂️</span>' for w in words])
        sort_boxes = "".join([
            f'<div class="sort-box"><div class="sort-box-title">{cat}</div></div>'
            for cat in categories[:4]
        ])
        body_html = f"""
        <div style="margin-bottom:10px;">
            <div class="section-title">{sort_words_title}</div>
            <div style="margin-top:8px;">{pills}</div>
        </div>
        <div class="section-title">{sort_paste_title}</div>
        <div class="sort-categories">{sort_boxes}</div>
        """

    elif activity_type == "fill_in_poster":
        sentences = data.get('fill_sentences', [])
        pills = "".join([f'<span class="word-pill">{w}</span>' for w in word_bank])
        sents_html = "".join([f"""
        <div style="display:flex; align-items:center; gap:6px; margin-bottom:12px; font-size:13.5px;">
            <strong>{i + 1}.</strong>
            {s.get('sentence', '').replace('_____', '<span style="border-bottom:2px solid #f1c40f; min-width:80px; display:inline-block;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>')}
        </div>
        """ for i, s in enumerate(sentences)])
        body_html = f"""
        <div class="word-bank">{word_bank_label} {pills}</div>
        {sents_html}
        """

    elif activity_type == "definition_table":
        rows = "".join([
            f"<tr><td><strong>{w.get('word', '')}</strong></td><td>{w.get('definition', '')}</td><td style='min-width:150px;'></td></tr>"
            for w in words
        ])
        body_html = f"<table>{def_table_headers}{rows}</table>"

    elif activity_type == "crossword_mini":
        clues = data.get('crossword_clues', [])
        across = [c for c in clues if c.get('direction') in ('מאוזן', 'across')]
        down = [c for c in clues if c.get('direction') in ('מאונך', 'down')]
        across_html = "".join([f'<li><strong>{c["number"]}.</strong> {c["clue"]}</li>' for c in across])
        down_html = "".join([f'<li><strong>{c["number"]}.</strong> {c["clue"]}</li>' for c in down])
        body_html = f"""
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
            <div>
                <div class="section-title">{crossword_across}</div>
                <ol style="font-size:13px; {list_padding}">{across_html}</ol>
                <div class="section-title" style="margin-top:10px;">{crossword_down}</div>
                <ol style="font-size:13px; {list_padding}">{down_html}</ol>
            </div>
            <div style="background:#fafafa; border:2px solid #f1c40f; border-radius:8px; min-height:200px; display:flex; align-items:center; justify-content:center; font-size:12px; color:#888;">
                {crossword_placeholder}
            </div>
        </div>
        """

    elif activity_type.startswith("physical_"):
        materials = data.get('materials_needed', [])
        steps = data.get('physical_steps', [])

        emoji, label = physical_labels.get(activity_type, ('✋', 'Hands-on Activity' if english_mode else 'פעילות ידנית'))

        materials_html = ""
        if materials:
            items_html = "".join([f"<li>{m}</li>" for m in materials])
            materials_html = f"""
            <div class="materials-box">
                <div class="materials-box-title">{materials_title}</div>
                <ul class="materials-list">{items_html}</ul>
            </div>
            """

        steps_html = ""
        if steps:
            steps_li = "".join([f"<li>{s}</li>" for s in steps])
            steps_html = f"""
            <div class="steps-box">
                <div class="steps-box-title">{steps_title}</div>
                <ol class="steps-list">{steps_li}</ol>
            </div>
            """

        # Word cards for cutting/use
        cards_html = ""
        if words:
            cards = "".join([f"""
            <div class="word-card-print">
                <div class="word-card-term">{w.get('word', '')}</div>
                <div class="word-card-def">{w.get('definition', '')}</div>
            </div>""" for w in words])
            cards_html = f"""
            <div class="section-title" style="margin-top:14px;">{word_cards_title}</div>
            <div class="scissors-hint" style="margin-bottom:8px;">{cut_hint}</div>
            <div class="word-cards-print">{cards}</div>
            """

        body_html = f"""
        <div class="physical-badge">{emoji} {physical_badge_prefix} — {label}</div>
        {materials_html}
        {steps_html}
        {cards_html}
        """

    else:  # dominoes or fallback
        dom_cards = ""
        shuffled = words.copy()
        random.shuffle(shuffled)
        for i in range(len(words)):
            left = words[i].get('word', '')
            right_idx = (i + 1) % len(shuffled)
            right = shuffled[right_idx].get('definition', '') if shuffled else ''
            dom_cards += f"""
            <div style="border:2.5px dashed #f1c40f; border-radius:8px; display:grid; grid-template-columns:1fr 4px 1fr; min-height:60px; overflow:hidden; break-inside:avoid;">
                <div style="background:#fef9e7; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:13px; padding:6px; text-align:center;">{left}</div>
                <div style="background:#7d6608;"></div>
                <div style="background:white; display:flex; align-items:center; justify-content:center; font-size:11px; padding:6px; text-align:center; color:#444;">{right}</div>
            </div>
            """
        body_html = f"""
        <div class="scissors-hint" style="margin-bottom:8px;">{dominoes_hint}</div>
        <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:8px;">{dom_cards}</div>
        """

    return f"""<!DOCTYPE html>
<html dir="{html_dir}" lang="{html_lang}">
<head><meta charset="UTF-8"><title>{page_title}</title>
<style>{get_css('vocabulary')}</style></head>
<body>
{render_header(title, round_num, 'vocabulary', english_mode=english_mode)}
<div class="instruction-box">📌 {data.get('instruction', '')}</div>
{body_html}
<div class="page-footer">{footer_text}</div>
</body></html>"""


def _render_stem_vocabulary(title: str, round_num: int, data: Dict) -> str:
    """Renders bilingual STEAM vocabulary game cards."""
    c = STATION_COLORS['vocabulary']
    game_type = data.get('game_type') or data.get('activity_type', 'stem_memory')
    words = data.get('words', [])

    game_labels = {
        'stem_memory':         ('🃏', 'זיכרון מושגים (Memory Match)', 'מצא זוגות: עברית↔אנגלית'),
        'stem_alias':          ('🗣️', 'אליאס מדעי (Science Alias)', 'הסבר את המושג ללא לומר אותו — הצוות מנחש'),
        'stem_taboo':          ('🚫', 'טאבו מדעי (Science Taboo)', 'הסבר ללא שימוש במילים האסורות'),
        'stem_quartets':       ('♦️', 'רביעיות מדעיות (Quartets)', 'אסוף 4 קלפים מאותה קטגוריה STEAM'),
        'stem_bingo':          ('🎯', 'Bingo מדעי (STEAM Bingo)', 'המורה קוראת הגדרות — מי שמזהה סומן'),
        'stem_snakes':         ('🐍', 'סולמות ונחשים STEAM', 'שאלת מושג בכל ריבוע — נכון=עלה, טעות=ירד'),
        'stem_quiz':           ('❓', 'שאלות ותשובות (Quiz Bowl)', 'תחרות קבוצתית — קלפי שאלות STEAM'),
        'stem_who_am_i':       ('🤔', 'מי אני? (Who Am I? Science)', 'כרטיס מושג על המצח — שאלות כן/לא'),
        'stem_dominoes':       ('🁣', 'דומינו STEAM', 'הנח קלף כך שמושג פוגש את הגדרתו'),
        'stem_flashcard':      ('⚡', 'כרטיסיות אוצר (Flashcard Battle)', 'מי עונה על ההגדרה מהר יותר — מנצח'),
        'stem_concept_puzzle': ('🧩', 'פאזל מושגים (Concept Puzzle)', 'חתוך ל-4 חלקים: שם/הגדרה/דוגמה/ציור'),
        'stem_word_chain':     ('🔗', 'שרשרת מדעית (Word Chain)', 'מושג שמתחיל באות האחרונה + הסבר הקשר'),
        'stem_matching_board': ('🗺️', 'התאמת מושגים (Matching Board)', 'לוח גדול — חיבור מושג↔הגדרה/תמונה'),
        'stem_20_questions':   ('🔢', '20 שאלות מדעיות', 'שאלות כן/לא לגילוי המושג הנסתר'),
        'stem_track':          ('🏁', 'מסלול מדעי (STEAM Track)', 'קלפי ירוק/צהוב/אדום — לפי רמת הקושי'),
        'stem_catan':          ('🏰', 'קטאן מדעי (Science Catan)', 'בנה ממלכה מדעית — ענה נכון, קבל משאב'),
        'stem_monopoly':       ('🎲', 'מונופול מדעי (Science Monopoly)', 'מושגי STEAM כנכסים — ענה הגדרה, רכוש'),
    }
    emoji, game_name, mechanic = game_labels.get(game_type, ('🃏', 'משחק מושגים STEAM', 'לפי הוראות'))

    # Materials & steps
    materials = data.get('materials_needed', [])
    mat_items = "".join([f"<li>{m}</li>" for m in materials])
    mat_html = f"""
    <div class="materials-box">
        <div class="materials-box-title">🎒 מה צריך להכין:</div>
        <ul class="materials-list">{mat_items}</ul>
    </div>""" if materials else ""

    steps = data.get('physical_steps', [])
    steps_li = "".join([f"<li>{s}</li>" for s in steps])
    steps_html = f"""
    <div class="steps-box">
        <div class="steps-box-title">📋 הוראות המשחק:</div>
        <ol class="steps-list">{steps_li}</ol>
    </div>""" if steps else ""

    # Bilingual concept cards
    cards_html = ""
    if words:
        cards = "".join([f"""
        <div class="word-card-print" style="background:{c['light']}; border-color:{c['border']};">
            <div class="word-card-term" style="color:{c['primary']};">{w.get('word', '')}</div>
            <div style="font-size:11px; color:#888; font-style:italic; margin:2px 0 4px;">{w.get('english', '')}</div>
            <div class="word-card-def">{w.get('definition', '')}</div>
            {f'<div style="font-size:10px; color:#aaa; margin-top:3px; border-top:1px dashed #eee; padding-top:3px;">{w.get("category", "")}</div>' if w.get('category') else ''}
        </div>""" for w in words])

        # Also create matching pairs cards (Hebrew on one side, English on other)
        heb_cards = "".join([f'<div class="cut-card cut-card-term" style="background:{c["light"]}; border-color:{c["border"]};">'
                              f'<span style="color:{c["primary"]}; font-weight:800;">{w.get("word", "")}</span>'
                              f'<div style="font-size:9px;color:#888;">{w.get("example","")[:35]}</div></div>'
                              for w in words])
        eng_cards_shuffled = words.copy()
        random.shuffle(eng_cards_shuffled)
        eng_cards = "".join([f'<div class="cut-card cut-card-def">'
                              f'<strong style="font-size:12px;">{w.get("english","")}</strong>'
                              f'<div style="font-size:10px;color:#666;margin-top:3px;">{w.get("definition","")[:50]}</div></div>'
                              for w in eng_cards_shuffled])

        cards_html = f"""
        <div class="section-title" style="margin-top:14px;">✂️ קלפי מושגים מלאים (להדפסה)</div>
        <div class="scissors-hint">כרטיס לכל מושג: עברית + אנגלית + הגדרה + קטגוריה</div>
        <div class="word-cards-print">{cards}</div>
        <div class="section-title" style="margin-top:14px;">✂️ קלפי התאמה — עברית (גזור)</div>
        <div class="cards-grid">{heb_cards}</div>
        <div class="section-title" style="margin-top:10px;">✂️ קלפי התאמה — English (גזור — מעורבב!)</div>
        <div class="cards-grid">{eng_cards}</div>
        <div class="scissors-hint">✂️ גזור את כל הקלפים, ערבב, וחבר כל מושג לתרגומו/הגדרתו</div>
        """

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head><meta charset="UTF-8"><title>תחנת אוצר מילים STEAM - {title} - סבב {round_num}</title>
<style>{get_css('vocabulary')}</style></head>
<body>
{render_header(title, round_num, 'vocabulary')}
<div class="instruction-box">
    <span style="background:{c['primary']}; color:white; padding:3px 10px; border-radius:12px; font-size:12px; margin-left:8px;">{emoji} {game_name}</span>
    📌 {mechanic}
</div>
<div style="background:#fef9e7; border:1.5px solid #f1c40f; border-radius:6px; padding:8px 12px; margin-bottom:12px; font-size:12px; color:#7d6608;">
    📌 {data.get('instruction', '')}
</div>
{mat_html}
{steps_html}
{cards_html}
<div class="page-footer">א"ל השד"ה STEAM | תחנת אוצר מילים | {title} | סבב {round_num} — © כל הזכויות שמורות</div>
</body></html>"""


def render_teacher_prep(title: str, round_num: int, data: Dict, content: Dict,
                         english_mode: bool = False) -> str:
    objectives = data.get('objectives', {})
    materials = data.get('materials', {})
    timing = data.get('timing', {})
    notes = data.get('teacher_notes', [])
    diff = data.get('differentiation', {})

    def list_html(items):
        return "".join([f'<li style="margin-bottom:4px;">{i}</li>' for i in items])

    if english_mode:
        lbl = ENGLISH_LABELS
        html_dir = "ltr"
        html_lang = "en"
        page_title = f"Teacher Preparation - {title} - Round {round_num}"
        footer_text = f"Al-HaSadeh | Teacher Preparation | {title} | Round {round_num} — {lbl['footer_copy']}"
        teacher_only_msg = lbl['teacher_only']
        objectives_title = "🎯 Round Objectives"
        knowledge_label = "Knowledge:"
        skills_label = "Skills:"
        values_label = "Values:"
        timing_title = "⏱️ Recommended Timing"
        materials_title = "🗃️ Materials for Each Station"
        notes_title = "📌 Notes and Key Points"
        diff_title = "🎯 Differentiation"
        struggling_label = "🟢 Struggling students:"
        advanced_label = "🔴 Advanced students:"
        special_label = "♿ Special education:"
        list_pad = "padding-left:16px;"
        notes_pad = "padding-left:18px;"
        station_name_fn = lambda k: ENGLISH_STATION_NAMES.get(k, {}).get('name', k)
    else:
        html_dir = "rtl"
        html_lang = "he"
        page_title = f"הכנה למורה - {title} - סבב {round_num}"
        footer_text = f"א\"ל השד\"ה | הכנה למורה | {title} | סבב {round_num} — © כל הזכויות שמורות"
        teacher_only_msg = "⚠️ דף זה מיועד למורה בלבד — אין להעביר לתלמידים"
        objectives_title = "🎯 מטרות הסבב (ימ\"ה)"
        knowledge_label = "ידע:"
        skills_label = "מיומנויות:"
        values_label = "ערכים:"
        timing_title = "⏱️ תזמון מומלץ"
        materials_title = "🗃️ ציוד וחומרים לכל תחנה"
        notes_title = "📌 הערות ונקודות לתשומת לב"
        diff_title = "🎯 דיפרנציאציה"
        struggling_label = "🟢 תלמידים מתקשים:"
        advanced_label = "🔴 תלמידים מתקדמים:"
        special_label = "♿ חינוך מיוחד:"
        list_pad = "padding-right:16px;"
        notes_pad = "padding-right:18px;"
        station_name_fn = lambda k: STATION_COLORS.get(k, {}).get('name', k)

    mat_html = ""
    for station, mat_list in materials.items():
        c = STATION_COLORS.get(station, STATION_COLORS['teacher'])
        items = "".join([f'<li>{m}</li>' for m in mat_list])
        sname = station_name_fn(station)
        mat_html += f"<div style='margin-bottom:8px;'><strong style='color:{c['primary']};'>{c['emoji']} {sname}:</strong><ul style='margin:3px 0; {list_pad}'>{items}</ul></div>"

    timing_html = "".join([
        f'<div style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #eee;">'
        f'<span><strong>{STATION_COLORS.get(k, {}).get("emoji", "")} {station_name_fn(k)}</strong></span>'
        f'<span style="color:#666;">{v}</span></div>'
        for k, v in timing.items()
    ])

    return f"""<!DOCTYPE html>
<html dir="{html_dir}" lang="{html_lang}">
<head><meta charset="UTF-8"><title>{page_title}</title>
<style>{get_css('teacher')}</style></head>
<body>
{render_header(title, round_num, 'teacher', include_student_bar=False, english_mode=english_mode)}

<div style="background:#f5eef8; border:2px solid #8e44ad; border-radius:8px; padding:12px 16px; margin-bottom:14px; font-size:12px; color:#4a235a; font-weight:600;">
    {teacher_only_msg}
</div>

<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:14px;">
    <div style="background:#f5eef8; border:1.5px solid #8e44ad; border-radius:8px; padding:12px;">
        <div style="font-weight:800; color:#4a235a; margin-bottom:8px;">{objectives_title}</div>
        <div style="font-size:12px;">
            <strong style="color:#1a5276;">{knowledge_label}</strong><ul style="{list_pad} margin:3px 0 6px 0; font-size:11.5px;">{list_html(objectives.get('knowledge', []))}</ul>
            <strong style="color:#1e8449;">{skills_label}</strong><ul style="{list_pad} margin:3px 0 6px 0; font-size:11.5px;">{list_html(objectives.get('skills', []))}</ul>
            <strong style="color:#7d6608;">{values_label}</strong><ul style="{list_pad} margin:3px 0; font-size:11.5px;">{list_html(objectives.get('values', []))}</ul>
        </div>
    </div>
    <div style="background:#f0f5ff; border:1.5px solid #2980b9; border-radius:8px; padding:12px;">
        <div style="font-weight:800; color:#1a5276; margin-bottom:8px;">{timing_title}</div>
        <div style="font-size:12px;">{timing_html}</div>
    </div>
</div>

<div style="background:#eafaf1; border:1.5px solid #27ae60; border-radius:8px; padding:12px; margin-bottom:14px;">
    <div style="font-weight:800; color:#1e8449; margin-bottom:8px;">{materials_title}</div>
    <div style="font-size:12px;">{mat_html}</div>
</div>

<div style="background:#fef9e7; border:1.5px solid #f1c40f; border-radius:8px; padding:12px; margin-bottom:14px;">
    <div style="font-weight:800; color:#7d6608; margin-bottom:8px;">{notes_title}</div>
    <ul style="font-size:12px; {notes_pad}">{list_html(notes)}</ul>
</div>

<div style="background:#fadbd8; border:1.5px solid #e74c3c; border-radius:8px; padding:12px;">
    <div style="font-weight:800; color:#c0392b; margin-bottom:8px;">{diff_title}</div>
    <div style="font-size:12px;">
        <div style="margin-bottom:6px;"><strong>{struggling_label}</strong> {diff.get('struggling', '')}</div>
        <div style="margin-bottom:6px;"><strong>{advanced_label}</strong> {diff.get('advanced', '')}</div>
        <div><strong>{special_label}</strong> {diff.get('special_needs', '')}</div>
    </div>
</div>

<div class="page-footer">{footer_text}</div>
</body></html>"""


def render_answer_key(title: str, round_num: int, precision_data: Dict, vocab_data: Dict,
                       methods_data: Dict, english_mode: bool = False) -> str:
    is_steam_prec = precision_data.get('is_hands_on', False)

    if english_mode:
        html_dir = "ltr"
        html_lang = "en"
        page_title = f"Answer Key - {title} - Round {round_num}"
        answers_only_msg = "⚠️ Answer Key — for teacher only"
        prec_title_steam = "🟢 Precision Station HANDS-ON — Expected Results"
        expected_label = "Expected results:"
        q_label = "Q:"
        a_label = "A:"
        prec_title_lang = "🟢 Precision Station — Answer Key"
        spelling_label = "Spelling words:"
        extra_key_label = "Additional answer key:"
        vocab_title = "🟡 Vocabulary Station — Answer Key"
        methods_title = "🔵 Success Criteria — Methods Station"
        criteria_label = "Assessment criteria:"
        list_pad = "padding-left:18px;"
        footer_text = f"Al-HaSadeh | Answer Key | {title} | Round {round_num} — © All rights reserved"
    else:
        html_dir = "rtl"
        html_lang = "he"
        page_title = f"פתרונות - {title} - סבב {round_num}"
        answers_only_msg = "⚠️ דף פתרונות — למורה בלבד"
        prec_title_steam = "🟢 תחנת דיוק HANDS-ON — תוצאות צפויות"
        expected_label = "תוצאות צפויות:"
        q_label = "ש:"
        a_label = "ת:"
        prec_title_lang = "🟢 פתרונות תחנת דיוק"
        spelling_label = "מילות ההכתבה:"
        extra_key_label = "מפתח תשובות נוסף:"
        vocab_title = "🟡 פתרונות תחנת אוצר מילים"
        methods_title = "🔵 מדדי הצלחה — תחנת שיטות"
        criteria_label = "קריטריונים להערכה:"
        list_pad = "padding-right:18px;"
        is_steam = is_steam_prec or vocab_data.get('bilingual', False)
        footer_text = f"א\"ל השד\"ה{' STEAM' if is_steam else ''} | פתרונות ומדדי הצלחה | {title} | סבב {round_num} — © כל הזכויות שמורות"

    if is_steam_prec:
        # STEAM precision answer section: expected results + analysis answers
        analysis_html = ""
        for q in precision_data.get('analysis_questions', []):
            analysis_html += (f'<div style="margin-bottom:8px;"><strong style="color:#1e8449;">{q_label}</strong> {q.get("question","")}'
                              f' → <strong style="color:#c0392b;">{a_label} {q.get("answer","")}</strong></div>')
        prec_section = f"""
        <div style="margin-bottom:16px;">
            <div class="section-title" style="background:#1e8449;">{prec_title_steam}</div>
            <div style="background:#d5f5e3; border-radius:6px; padding:8px; margin-top:8px; font-size:12.5px;">
                <strong>{expected_label}</strong><br>{precision_data.get('expected_results', '')}
            </div>
            <div style="margin-top:10px; font-size:12.5px;">{analysis_html}</div>
        </div>"""
    else:
        # Language / English precision answer section: dictation + exercises
        dict_answers = "".join([
            f'<span class="word-pill">{d.get("word", "")}</span>'
            for d in precision_data.get('dictation_list', [])
        ])
        exercises_answers = ""
        for ex in precision_data.get('exercises', []):
            items = "".join([
                f'<li><strong>{q_label}</strong> {item.get("question", "")} → '
                f'<strong style="color:#1e8449;">{a_label} {item.get("answer", "")}</strong></li>'
                for item in ex.get('items', [])
            ])
            exercises_answers += f"<div style='margin-bottom:10px;'><strong>{ex.get('title', '')}</strong><ul style='{list_pad} font-size:12px;'>{items}</ul></div>"
        prec_section = f"""
        <div style="margin-bottom:16px;">
            <div class="section-title" style="background:#1e8449;">{prec_title_lang}</div>
            <div style="margin-top:8px; font-size:12.5px;">
                <strong>{spelling_label}</strong><br><div style="margin-top:5px;">{dict_answers}</div>
            </div>
            <div style="margin-top:10px;">{exercises_answers}</div>
            <div style="background:#d5f5e3; border-radius:6px; padding:8px; margin-top:6px; font-size:12px;">
                <strong>{extra_key_label}</strong> {precision_data.get('answer_key', '')}
            </div>
        </div>"""

    if english_mode:
        footer_text = f"Al-HaSadeh | Answer Key | {title} | Round {round_num} — © All rights reserved"

    return f"""<!DOCTYPE html>
<html dir="{html_dir}" lang="{html_lang}">
<head><meta charset="UTF-8"><title>{page_title}</title>
<style>{get_css('answers')}</style></head>
<body>
{render_header(title, round_num, 'answers', include_student_bar=False, english_mode=english_mode)}

<div style="background:#eaf2ff; border:2px solid #2c5aa0; border-radius:8px; padding:8px 14px; margin-bottom:14px; font-size:12px; font-weight:600; color:#1a3a6b;">
    {answers_only_msg}
</div>

{prec_section}

<div style="margin-bottom:16px;">
    <div class="section-title" style="background:#7d6608;">{vocab_title}</div>
    <div style="background:#fef9e7; border:1px solid #f1c40f; border-radius:6px; padding:10px; margin-top:8px; font-size:12.5px;">
        {vocab_data.get('answer_key', '')}
    </div>
</div>

<div style="margin-bottom:16px;">
    <div class="section-title" style="background:#1a5276;">{methods_title}</div>
    <div style="margin-top:8px; font-size:12.5px;">
        <strong>{criteria_label}</strong>
        <ul style="{list_pad}">{"".join([f"<li>{c}</li>" for c in methods_data.get('success_criteria', [])])}</ul>
    </div>
</div>

<div class="page-footer">{footer_text}</div>
</body></html>"""


def render_roadmap(title: str, roadmap: Dict, english_mode: bool = False) -> str:
    is_steam = roadmap.get('is_steam', False)
    goals_raw = roadmap.get('learning_goals', [])
    # learning_goals can be a list or a dict with knowledge/skills/values
    if isinstance(goals_raw, dict):
        goals_flat = goals_raw.get('knowledge', []) + goals_raw.get('skills', []) + goals_raw.get('values', [])
    else:
        goals_flat = goals_raw
    goals = "".join([
        f'<span class="word-pill" style="background:#eaf2ff; border-color:#2c5aa0; color:#1a3a6b;">{g}</span>'
        for g in goals_flat
    ])

    # Adapt column headers + central line based on mode
    if english_mode:
        col1_header = "Round"
        col2_header = "🔵 Methods Station<br><small>(structured writing)</small>"
        col3_header = "🟢 Precision Station<br><small>(spelling & grammar)</small>"
        col4_header = "🟡 Vocabulary Station<br><small>(printed/hands-on activity)</small>"
        comp_header = "🔴 Comprehension Station<br><small>(text + oral discussion)</small>"
        central_line = f"<strong>Central text type:</strong> {roadmap.get('central_text_type', '')} | <strong>Language focus:</strong> {roadmap.get('language_focus', '')}"
        mode_badge = '<span style="background:#1a5276; color:white; padding:3px 12px; border-radius:14px; font-size:12px; margin-right:8px;">🇬🇧 English Edition</span>'
        iron_rule = "All 4 stations in every round are <strong>fully independent (STAND-ALONE)</strong> — a student can start at any station without depending on the others."
        goals_label = "Learning Goals:"
        rounds_label = "Round"
        iron_label = "⚡ Iron Rule:"
        html_dir = "ltr"
        html_lang = "en"
        page_title = f"Unit Roadmap - {title}"
        footer_text = f"Al-HaSadeh | Unit Roadmap | {title} — © All rights reserved"
        method_label = "שיטת א\"ל השד\"ה"
        rounds_count_label = "rounds"
    elif is_steam:
        col1_header = "סבב"
        col3_header = "🟢 תחנת דיוק<br><small>(HANDS-ON ניסוי/בנייה)</small>"
        col4_header = "🟡 תחנת אוצר מילים<br><small>(מושגי STEAM + עברית/אנגלית)</small>"
        col2_header = "🔵 תחנת שיטות<br><small>(חשיבה תהליכית-מדעית)</small>"
        comp_header = "🔴 תחנת הבנה<br><small>(ערוצי קלט מגוונים)</small>"
        central_line = f"<strong>התופעה המרכזית:</strong> {roadmap.get('central_phenomenon', roadmap.get('central_text_type', ''))}"
        mode_badge = '<span style="background:#e74c3c; color:white; padding:3px 12px; border-radius:14px; font-size:12px; margin-right:8px;">🔬 STEAM Edition</span>'
        iron_rule = "כל 4 תחנות בכל סבב הן <strong>עצמאיות לחלוטין (STAND-ALONE)</strong> — גם בגרסת STEAM! אם תחנה צריכה תוצר מתחנה אחרת — הכניסי אותו ישירות."
        goals_label = "מטרות הלמידה:"
        rounds_label = "סבב"
        iron_label = "⚡ עקרון ברזל:"
        html_dir = "rtl"
        html_lang = "he"
        page_title = f"מפת דרכים - {title}"
        footer_text = f"א\"ל השד\"ה STEAM | מפת דרכים | {title} — © כל הזכויות שמורות"
        method_label = "שיטת א\"ל השד\"ה"
        rounds_count_label = "סבבים"
    else:
        col1_header = "סבב"
        col3_header = "🟢 תחנת דיוק<br><small>(לשון ודקדוק)</small>"
        col4_header = "🟡 תחנת אוצר מילים<br><small>(פעילות מודפסת)</small>"
        col2_header = "🔵 תחנת שיטות<br><small>(כתיבה מובנית)</small>"
        comp_header = "🔴 תחנת הבנה<br><small>(טקסט + דיון בע\"פ)</small>"
        central_line = f"<strong>טקסט מרכזי:</strong> {roadmap.get('central_text_type', '')}"
        mode_badge = ""
        iron_rule = "כל 4 תחנות בכל סבב הן <strong>עצמאיות לחלוטין</strong> — תלמיד יכול להתחיל בכל תחנה ולעבור לכל תחנה בלי תלות בתחנות אחרות."
        goals_label = "מטרות הלמידה:"
        rounds_label = "סבב"
        iron_label = "⚡ עקרון ברזל:"
        html_dir = "rtl"
        html_lang = "he"
        page_title = f"מפת דרכים - {title}"
        footer_text = f"א\"ל השד\"ה | מפת דרכים | {title} — © כל הזכויות שמורות"
        method_label = "שיטת א\"ל השד\"ה"
        rounds_count_label = "סבבים"

    # Per-round rows
    rounds_html = ""
    for r in roadmap.get('rounds', []):
        rn = r.get('round', '')
        comp = r.get('comprehension', {})
        meth = r.get('methods', {})
        prec = r.get('precision', {})
        vocab = r.get('vocabulary', {})

        comp_type = comp.get('input_type') or comp.get('text_type', '')
        meth_type = meth.get('thinking_framework') or meth.get('writing_type', '')
        prec_type = prec.get('hands_on_type') or prec.get('activity_type', '')
        vocab_type = vocab.get('game_type') or vocab.get('activity_type', '')

        rounds_html += f"""
        <tr>
            <td style="font-weight:800; text-align:center; background:#f8f9fa; font-size:14px;">{rounds_label} {rn}</td>
            <td style="background:#fadbd8;">
                <div style="font-weight:700; color:#c0392b; font-size:11px;">🔴 {comp_type}</div>
                <div style="font-size:11.5px; margin-top:3px;">{comp.get('description', '')}</div>
            </td>
            <td style="background:#d6eaf8;">
                <div style="font-weight:700; color:#1a5276; font-size:11px;">🔵 {meth_type}</div>
                <div style="font-size:11.5px; margin-top:3px;">{meth.get('description', '')}</div>
            </td>
            <td style="background:#d5f5e3;">
                <div style="font-weight:700; color:#1e8449; font-size:11px;">🟢 {prec_type}</div>
                <div style="font-size:11.5px; margin-top:3px;">{prec.get('description', '')}</div>
            </td>
            <td style="background:#fef9e7;">
                <div style="font-weight:700; color:#7d6608; font-size:11px;">🟡 {vocab_type}</div>
                <div style="font-size:11.5px; margin-top:3px;">{vocab.get('description', '')}</div>
            </td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html dir="{html_dir}" lang="{html_lang}">
<head><meta charset="UTF-8"><title>{page_title}</title>
<style>{get_css('teacher')}
.roadmap-table {{ width:100%; border-collapse:collapse; }}
.roadmap-table th {{ background:#4a235a; color:white; padding:10px 12px; font-size:13px; }}
.roadmap-table td {{ border:1.5px solid #ddd; padding:10px 12px; vertical-align:top; }}
</style></head>
<body>
<div style="background:linear-gradient(135deg, #4a235a, #8e44ad); color:white; padding:16px; border-radius:10px; margin-bottom:16px;">
    <div style="font-size:22px; font-weight:800; text-align:center; margin-bottom:4px;">{mode_badge}📋 {'Unit Roadmap' if english_mode else 'מפת דרכים'} — {roadmap.get('unit_title', title)}</div>
    <div style="font-size:13px; text-align:center; opacity:0.9;">{method_label} | {len(roadmap.get('rounds', []))} {rounds_count_label}</div>
</div>

<div style="margin-bottom:14px; font-size:12.5px;">
    <strong>{goals_label}</strong> {goals}<br>
    <span style="margin-top:6px; display:inline-block;">{central_line}</span>
</div>

<table class="roadmap-table">
    <tr>
        <th>{col1_header}</th>
        <th>{comp_header}</th>
        <th>{col2_header}</th>
        <th>{col3_header}</th>
        <th>{col4_header}</th>
    </tr>
    {rounds_html}
</table>

<div style="margin-top:14px; background:#fef9e7; border:1.5px solid #f1c40f; border-radius:8px; padding:10px; font-size:12px;">
    <strong>{iron_label}</strong> {iron_rule}
</div>

<div class="page-footer">{footer_text}</div>
</body></html>"""
