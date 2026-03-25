import os
from typing import Dict, List

from .gemini import call_gemini

_PROVIDER_LABEL = {
    "nvidia": "NVIDIA Nemotron",
    "gemini": "Gemini",
}
from .config import is_stem, is_english
from .prompts import (
    build_roadmap_prompt,
    build_comprehension_prompt,
    build_methods_prompt,
    build_precision_prompt,
    build_vocabulary_prompt,
    build_teacher_prep_prompt,
    # STEAM edition
    build_stem_roadmap_prompt,
    build_stem_comprehension_prompt,
    build_stem_methods_prompt,
    build_stem_precision_prompt,
    build_stem_vocabulary_prompt,
    # English edition
    build_english_roadmap_prompt,
    build_english_comprehension_prompt,
    build_english_methods_prompt,
    build_english_precision_prompt,
    build_english_vocabulary_prompt,
    build_english_teacher_prep_prompt,
)
from .renderers import (
    render_roadmap,
    render_comprehension,
    render_methods,
    render_precision,
    render_vocabulary,
    render_teacher_prep,
    render_answer_key,
)
from .pdf import save_html, make_pdf


def generate_roadmap(user_input: Dict, output_dir: str = "output") -> Dict:
    subject = user_input['subject']
    topic = user_input['topic']
    grade = user_input['grade']
    rounds = user_input.get('rounds', 4)

    print(f"\n{'=' * 60}")
    print(f"📋 GENERATING ROADMAP: {topic}")
    print(f"   Subject: {subject} | Grade: {grade} | Rounds: {rounds}")
    print('=' * 60)

    provider = _PROVIDER_LABEL.get(os.environ.get("LLM_PROVIDER", "gemini").lower(), "LLM")
    steam_mode = is_stem(subject)
    english_mode = is_english(subject)
    if steam_mode:
        mode_label = "STEAM"
    elif english_mode:
        mode_label = "English"
    else:
        mode_label = "Language"
    print(f"\n🗺️ Calling {provider} for roadmap [{mode_label} mode]...")
    if steam_mode:
        roadmap_prompt_fn = build_stem_roadmap_prompt
    elif english_mode:
        roadmap_prompt_fn = build_english_roadmap_prompt
    else:
        roadmap_prompt_fn = build_roadmap_prompt
    roadmap = call_gemini(roadmap_prompt_fn(subject, topic, grade, rounds))

    os.makedirs(output_dir, exist_ok=True)
    safe_name = topic.replace(" ", "_").replace("/", "_")[:35]
    roadmap_html = render_roadmap(topic, roadmap, english_mode=english_mode)
    roadmap_path = f"{output_dir}/{safe_name}_roadmap.html"
    save_html(roadmap_html, roadmap_path)

    print(f"\n✅ ROADMAP COMPLETE")
    print(f"   {len(roadmap.get('rounds', []))} rounds planned")

    roadmap['_meta'] = {
        'subject': subject,
        'topic': topic,
        'grade': grade,
        'safe_name': safe_name,
        'output_dir': output_dir,
    }
    return roadmap


def generate_round(user_input: Dict, roadmap: Dict, round_num: int,
                   output_dir: str = "output",
                   prev_texts: List[str] = None) -> Dict:
    if prev_texts is None:
        prev_texts = []

    subject = user_input['subject']
    topic = user_input['topic']
    grade = user_input['grade']
    total_r = user_input.get('rounds', 4)
    safe_name = roadmap.get('_meta', {}).get('safe_name', topic.replace(" ", "_")[:30])

    rounds_list = roadmap.get('rounds', [])
    if round_num > len(rounds_list):
        print(f"⚠️ Round {round_num} not in roadmap (only {len(rounds_list)} rounds)")
        return {}

    round_plan = rounds_list[round_num - 1]

    steam_mode = is_stem(subject)
    english_mode = is_english(subject)
    if steam_mode:
        mode_label = "STEAM"
    elif english_mode:
        mode_label = "English"
    else:
        mode_label = "Language"

    print(f"\n{'=' * 60}")
    print(f"📖 GENERATING ROUND {round_num}/{total_r}: {topic} [{mode_label}]")
    print('=' * 60)

    os.makedirs(output_dir, exist_ok=True)
    files = {}
    content = {}

    # Station 1: Comprehension
    print(f"\n🔴 [1/4] Generating comprehension text...")
    if steam_mode:
        comp_prompt_fn = build_stem_comprehension_prompt
    elif english_mode:
        comp_prompt_fn = build_english_comprehension_prompt
    else:
        comp_prompt_fn = build_comprehension_prompt
    comp_data = call_gemini(comp_prompt_fn(
        subject, topic, grade, round_num, total_r, round_plan, prev_texts
    ))
    word_count = sum(len(p.get('text', '').split()) for p in comp_data.get('paragraphs', []))
    print(f"   ✅ {word_count} words | {len(comp_data.get('paragraphs', []))} paragraphs")
    prev_texts.append(comp_data.get('section_title', '') + ": " + comp_data.get('intro_sentence', ''))
    content['comprehension'] = comp_data
    comp_html = render_comprehension(topic, round_num, comp_data, grade, english_mode=english_mode)
    comp_path = f"{output_dir}/{safe_name}_round{round_num}_comprehension.html"
    save_html(comp_html, comp_path)
    files['comprehension'] = comp_path

    # Station 2: Methods
    if steam_mode:
        meth_label = 'procedural thinking'
    elif english_mode:
        meth_label = 'English writing'
    else:
        meth_label = 'writing'
    print(f"\n🔵 [2/4] Generating {meth_label} task (methods)...")
    if steam_mode:
        meth_prompt_fn = build_stem_methods_prompt
    elif english_mode:
        meth_prompt_fn = build_english_methods_prompt
    else:
        meth_prompt_fn = build_methods_prompt
    meth_data = call_gemini(meth_prompt_fn(
        subject, topic, grade, round_num, round_plan, comp_data
    ))
    print(f"   ✅ Type: {meth_data.get('writing_type', '')} | Levels: {list(meth_data.get('difficulty_levels', {}).keys())}")
    content['methods'] = meth_data
    meth_html = render_methods(topic, round_num, meth_data, english_mode=english_mode)
    meth_path = f"{output_dir}/{safe_name}_round{round_num}_methods.html"
    save_html(meth_html, meth_path)
    files['methods'] = meth_path

    # Station 3: Precision (language grammar / STEM hands-on / English accuracy)
    if steam_mode:
        prec_label = 'hands-on lab'
    elif english_mode:
        prec_label = 'English language accuracy tasks'
    else:
        prec_label = 'precision tasks (language)'
    print(f"\n🟢 [3/4] Generating {prec_label}...")
    key_terms = comp_data.get('all_key_terms', [])
    if steam_mode:
        prec_prompt_fn = build_stem_precision_prompt
    elif english_mode:
        prec_prompt_fn = build_english_precision_prompt
    else:
        prec_prompt_fn = build_precision_prompt
    prec_data = call_gemini(prec_prompt_fn(
        subject, topic, grade, round_num, round_plan, key_terms
    ))
    print(f"   ✅ {len(prec_data.get('dictation_list', []))} dictation words | {len(prec_data.get('exercises', []))} exercises")
    content['precision'] = prec_data
    prec_html = render_precision(topic, round_num, prec_data, english_mode=english_mode)
    prec_path = f"{output_dir}/{safe_name}_round{round_num}_precision.html"
    save_html(prec_html, prec_path)
    files['precision'] = prec_path

    # Station 4: Vocabulary (language / STEAM bilingual games / English vocabulary)
    if steam_mode:
        vocab_label = 'game (STEAM bilingual)'
    elif english_mode:
        vocab_label = 'English vocabulary activity'
    else:
        vocab_label = 'activity'
    print(f"\n🟡 [4/4] Generating vocabulary {vocab_label}...")
    vocab_key = 'game_type' if steam_mode else 'activity_type'
    used_vocab_types = [r.get('vocabulary', {}).get(vocab_key, '') for r in rounds_list[:round_num - 1]]
    if steam_mode:
        vocab_prompt_fn = build_stem_vocabulary_prompt
    elif english_mode:
        vocab_prompt_fn = build_english_vocabulary_prompt
    else:
        vocab_prompt_fn = build_vocabulary_prompt
    vocab_data = call_gemini(vocab_prompt_fn(
        subject, topic, grade, round_num, round_plan, key_terms, used_vocab_types
    ))
    print(f"   ✅ Type: {vocab_data.get('activity_type', '')} — {vocab_data.get('title', '')}")
    content['vocabulary'] = vocab_data
    vocab_html = render_vocabulary(topic, round_num, vocab_data, english_mode=english_mode)
    vocab_path = f"{output_dir}/{safe_name}_round{round_num}_vocabulary.html"
    save_html(vocab_html, vocab_path)
    files['vocabulary'] = vocab_path

    # Teacher Prep
    print(f"\n📋 [+] Generating teacher prep doc...")
    teacher_prep_fn = build_english_teacher_prep_prompt if english_mode else build_teacher_prep_prompt
    teacher_data = call_gemini(teacher_prep_fn(subject, topic, grade, round_num, content))
    content['teacher'] = teacher_data
    teacher_html = render_teacher_prep(topic, round_num, teacher_data, content, english_mode=english_mode)
    teacher_path = f"{output_dir}/{safe_name}_round{round_num}_teacher_prep.html"
    save_html(teacher_html, teacher_path)
    files['teacher_prep'] = teacher_path

    # Answer Key
    print(f"\n🔑 [+] Generating answer key...")
    answers_html = render_answer_key(topic, round_num, prec_data, vocab_data, meth_data, english_mode=english_mode)
    answers_path = f"{output_dir}/{safe_name}_round{round_num}_answer_key.html"
    save_html(answers_html, answers_path)
    files['answer_key'] = answers_path

    # PDFs
    print(f"\n📄 Creating PDFs...")
    student_files = [files['comprehension'], files['methods'], files['precision'], files['vocabulary']]
    student_pdf = f"{output_dir}/{safe_name}_round{round_num}_STUDENT.pdf"
    make_pdf(student_files, student_pdf, topic, f"סבב {round_num} — לתלמיד")
    files['student_pdf'] = student_pdf

    teacher_files = [files['teacher_prep']] + student_files + [files['answer_key']]
    teacher_pdf = f"{output_dir}/{safe_name}_round{round_num}_TEACHER.pdf"
    make_pdf(teacher_files, teacher_pdf, topic, f"סבב {round_num} — למורה")
    files['teacher_pdf'] = teacher_pdf

    print(f"\n{'=' * 60}")
    print(f"✨ ROUND {round_num} COMPLETE!")
    print(f"   Files saved in: {output_dir}")
    print('=' * 60)

    return {'files': files, 'content': content, 'prev_texts': prev_texts}


def generate_all_rounds(user_input: Dict, roadmap: Dict, output_dir: str = "output") -> Dict:
    total = user_input.get('rounds', 4)
    all_results = []
    prev_texts = []
    all_student_files = []
    all_teacher_files = []

    for i in range(1, total + 1):
        result = generate_round(user_input, roadmap, i, output_dir, prev_texts)
        prev_texts = result.get('prev_texts', prev_texts)
        all_results.append(result)
        files = result.get('files', {})
        all_student_files.extend([
            files.get('comprehension', ''), files.get('methods', ''),
            files.get('precision', ''), files.get('vocabulary', '')
        ])
        all_teacher_files.extend([
            files.get('teacher_prep', ''), files.get('comprehension', ''),
            files.get('methods', ''), files.get('precision', ''),
            files.get('vocabulary', ''), files.get('answer_key', '')
        ])

    safe_name = roadmap.get('_meta', {}).get('safe_name', 'unit')
    topic = user_input['topic']

    print(f"\n📄 Creating FULL UNIT PDFs...")
    unit_student_pdf = f"{output_dir}/{safe_name}_FULL_STUDENT.pdf"
    make_pdf([f for f in all_student_files if f], unit_student_pdf, topic, f"יחידה מלאה — {total} סבבים — לתלמיד")

    unit_teacher_pdf = f"{output_dir}/{safe_name}_FULL_TEACHER.pdf"
    make_pdf([f for f in all_teacher_files if f], unit_teacher_pdf, topic, f"יחידה מלאה — {total} סבבים — למורה")

    print(f"\n🎉 ALL {total} ROUNDS COMPLETE! Files in: {output_dir}")

    return {
        'rounds': all_results,
        'student_pdf': unit_student_pdf,
        'teacher_pdf': unit_teacher_pdf,
    }
