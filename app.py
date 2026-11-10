import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import get_db_connection, init_db

def ensure_db():
    try:
        conn = get_db_connection()
        count = conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
        conn.close()
        if count == 0:
            from seed_data import seed
            seed()
    except Exception:
        from seed_data import seed
        seed()

ensure_db()

app = Flask(__name__)
app.secret_key = "mysterybox-detective-classified-secret"

@app.route("/")
def index():
    conn = get_db_connection()
    cases = conn.execute("SELECT * FROM cases").fetchall()
    conn.close()
    return render_template("index.html", cases=cases)

@app.route("/case/<case_id>")
def case_view(case_id):
    conn = get_db_connection()
    case = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
    if not case:
        conn.close()
        return redirect(url_for("index"))

    scenes = conn.execute("SELECT * FROM crime_scenes WHERE case_id = ?", (case_id,)).fetchall()
    suspects = conn.execute("SELECT * FROM suspects WHERE case_id = ?", (case_id,)).fetchall()
    clues = conn.execute("SELECT * FROM clues WHERE case_id = ?", (case_id,)).fetchall()
    notes = conn.execute("SELECT * FROM detective_notes WHERE case_id = ? ORDER BY created_at DESC", (case_id,)).fetchall()
    conn.close()

    return render_template("case.html", case=case, scenes=scenes, suspects=suspects, clues=clues, notes=notes)

@app.route("/api/case/<case_id>")
def api_case_data(case_id):
    conn = get_db_connection()
    case = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
    if not case:
        conn.close()
        return jsonify({"error": "Case not found"}), 404

    scenes = conn.execute("SELECT * FROM crime_scenes WHERE case_id = ?", (case_id,)).fetchall()
    suspects = conn.execute("SELECT id, case_id, name, role, age, avatar_svg, bio, initial_statement, motive_hint, alibi_claim FROM suspects WHERE case_id = ?", (case_id,)).fetchall()
    clues = conn.execute("SELECT * FROM clues WHERE case_id = ?", (case_id,)).fetchall()
    
    # Dialogues indexed by suspect
    dialogues_raw = conn.execute("""
        SELECT d.id, d.suspect_id, d.topic, d.question, d.answer, d.reaction_mood, d.unlocks_clue_id
        FROM suspect_dialogues d
        JOIN suspects s ON d.suspect_id = s.id
        WHERE s.case_id = ?
    """, (case_id,)).fetchall()

    conn.close()

    scenes_list = [dict(s) for s in scenes]
    suspects_list = [dict(s) for s in suspects]
    clues_list = [dict(c) for c in clues]
    
    dialogues_map = {}
    for d in dialogues_raw:
        s_id = d["suspect_id"]
        if s_id not in dialogues_map:
            dialogues_map[s_id] = []
        dialogues_map[s_id].append(dict(d))

    return jsonify({
        "case": dict(case),
        "scenes": scenes_list,
        "suspects": suspects_list,
        "clues": clues_list,
        "dialogues": dialogues_map
    })

@app.route("/api/interrogate", methods=["POST"])
def api_interrogate():
    data = request.get_json() or {}
    dialogue_id = data.get("dialogue_id")
    if not dialogue_id:
        return jsonify({"error": "Missing dialogue_id"}), 400

    conn = get_db_connection()
    dialogue = conn.execute("SELECT * FROM suspect_dialogues WHERE id = ?", (dialogue_id,)).fetchone()
    if not dialogue:
        conn.close()
        return jsonify({"error": "Dialogue not found"}), 404

    unlocked_clue = None
    if dialogue["unlocks_clue_id"]:
        unlocked_clue_row = conn.execute("SELECT * FROM clues WHERE id = ?", (dialogue["unlocks_clue_id"],)).fetchone()
        if unlocked_clue_row:
            unlocked_clue = dict(unlocked_clue_row)

    conn.close()

    return jsonify({
        "success": True,
        "answer": dialogue["answer"],
        "reaction_mood": dialogue["reaction_mood"],
        "unlocked_clue": unlocked_clue
    })

@app.route("/api/present-evidence", methods=["POST"])
def api_present_evidence():
    data = request.get_json() or {}
    suspect_id = data.get("suspect_id")
    clue_id = data.get("clue_id")

    if not suspect_id or not clue_id:
        return jsonify({"error": "Missing suspect_id or clue_id"}), 400

    conn = get_db_connection()
    contradiction = conn.execute("""
        SELECT * FROM contradictions 
        WHERE suspect_id = ? AND clue_id = ?
    """, (suspect_id, clue_id)).fetchone()

    suspect = conn.execute("SELECT * FROM suspects WHERE id = ?", (suspect_id,)).fetchone()
    clue = conn.execute("SELECT * FROM clues WHERE id = ?", (clue_id,)).fetchone()

    if contradiction:
        result = {
            "is_contradiction": True,
            "callout_text": contradiction["callout_text"],
            "suspect_response": contradiction["suspect_response"],
            "breaks_alibi": bool(contradiction["breaks_alibi"]),
            "suspect_name": suspect["name"] if suspect else "Suspect"
        }
    else:
        # Default dismissal response
        generic_responses = [
            f"\"{clue['title'] if clue else 'That piece of evidence'}? What does that have to do with me, Inspector? You're grasping at straws.\"",
            "\"I fail to see the relevance. Is this your best attempt at intimidation?\"",
            "\"I've never laid eyes on that item in my life. Try finding some real proof.\""
        ]
        import random
        result = {
            "is_contradiction": False,
            "callout_text": f"Detective presents '{clue['title'] if clue else 'evidence'}' to {suspect['name'] if suspect else 'the suspect'}.",
            "suspect_response": random.choice(generic_responses),
            "breaks_alibi": False,
            "suspect_name": suspect["name"] if suspect else "Suspect"
        }

    conn.close()
    return jsonify(result)

@app.route("/api/accuse", methods=["POST"])
def api_accuse():
    data = request.get_json() or {}
    case_id = data.get("case_id")
    suspect_id = data.get("suspect_id")
    weapon_clue_id = data.get("weapon_clue_id")
    proof_clue_id = data.get("proof_clue_id")
    motive_statement = data.get("motive_statement", "").strip()

    if not all([case_id, suspect_id, weapon_clue_id, proof_clue_id]):
        return jsonify({"error": "Incomplete accusation. You must select suspect, method/weapon, and decisive proof."}), 400

    conn = get_db_connection()
    solution = conn.execute("SELECT * FROM case_solutions WHERE case_id = ?", (case_id,)).fetchone()
    accused_suspect = conn.execute("SELECT * FROM suspects WHERE id = ?", (suspect_id,)).fetchone()
    
    if not solution or not accused_suspect:
        conn.close()
        return jsonify({"error": "Invalid case or suspect."}), 404

    correct_suspect = (suspect_id == solution["culprit_suspect_id"])
    correct_weapon = (weapon_clue_id == solution["weapon_clue_id"])
    correct_proof = (proof_clue_id == solution["key_proof_clue_id"])

    # Score calculation
    score = 0
    if correct_suspect:
        score += 500
    if correct_weapon:
        score += 250
    if correct_proof:
        score += 250

    is_flawless = (correct_suspect and correct_weapon and correct_proof)

    verdict_type = "flawless" if is_flawless else ("partial" if correct_suspect else "wrong_suspect")

    if is_flawless:
        title = "CASE CLOSED: MASTER SLEUTH VERDICT!"
        message = "Your deduction was razor-sharp! The suspect could not withstand the mountain of indisputable proof."
        confession = accused_suspect["confession"]
    elif correct_suspect and (not correct_weapon or not correct_proof):
        title = "INSUFFICIENT EVIDENCE: CHARGES THROWN OUT!"
        message = f"You correctly suspected {accused_suspect['name']}, but your chosen method or decisive proof was flawed. The defense attorney ripped your argument apart in front of the magistrate."
        confession = "The suspect grinned coldly as their lawyer secured an immediate bail release."
    else:
        title = "MISCARRIAGE OF JUSTICE: WRONG SUSPECT ARRESTED!"
        message = f"You arrested {accused_suspect['name']}, who is entirely innocent of the crime! The real culprit has successfully slipped away into the shadows."
        confession = f"\"{accused_suspect['innocent_statement']}\""

    conn.close()

    return jsonify({
        "success": True,
        "is_flawless": is_flawless,
        "verdict_type": verdict_type,
        "score": score,
        "title": title,
        "message": message,
        "confession": confession,
        "full_narrative": solution["full_verdict_narrative"],
        "details": {
            "correct_suspect": correct_suspect,
            "correct_weapon": correct_weapon,
            "correct_proof": correct_proof
        }
    })

@app.route("/api/notes", methods=["GET", "POST"])
def api_notes():
    conn = get_db_connection()
    if request.method == "POST":
        data = request.get_json() or {}
        case_id = data.get("case_id")
        note_text = data.get("note_text", "").strip()
        if not case_id or not note_text:
            conn.close()
            return jsonify({"error": "Missing note details"}), 400
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO detective_notes (case_id, note_text) VALUES (?, ?)", (case_id, note_text))
        conn.commit()
        note_id = cursor.lastrowid
        conn.close()
        return jsonify({"success": True, "id": note_id, "note_text": note_text})
    else:
        case_id = request.args.get("case_id")
        notes = conn.execute("SELECT * FROM detective_notes WHERE case_id = ? ORDER BY created_at DESC", (case_id,)).fetchall()
        conn.close()
        return jsonify({"notes": [dict(n) for n in notes]})

@app.route("/api/reset-notes/<case_id>", methods=["POST"])
def api_reset_notes(case_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM detective_notes WHERE case_id = ?", (case_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
