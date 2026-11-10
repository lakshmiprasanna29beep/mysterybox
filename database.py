import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mysterybox.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript("""
    DROP TABLE IF EXISTS case_solutions;
    DROP TABLE IF EXISTS contradictions;
    DROP TABLE IF EXISTS suspect_dialogues;
    DROP TABLE IF EXISTS clues;
    DROP TABLE IF EXISTS crime_scenes;
    DROP TABLE IF EXISTS suspects;
    DROP TABLE IF EXISTS cases;
    DROP TABLE IF EXISTS detective_notes;

    CREATE TABLE cases (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        tagline TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        case_number TEXT NOT NULL,
        location TEXT NOT NULL,
        incident_time TEXT NOT NULL,
        victim TEXT NOT NULL,
        victim_role TEXT NOT NULL,
        briefing TEXT NOT NULL,
        incident_summary TEXT NOT NULL,
        icon TEXT NOT NULL,
        badge_color TEXT NOT NULL
    );

    CREATE TABLE crime_scenes (
        id TEXT PRIMARY KEY,
        case_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        icon TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases (id)
    );

    CREATE TABLE suspects (
        id TEXT PRIMARY KEY,
        case_id TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        age INTEGER NOT NULL,
        avatar_svg TEXT NOT NULL,
        bio TEXT NOT NULL,
        initial_statement TEXT NOT NULL,
        motive_hint TEXT NOT NULL,
        alibi_claim TEXT NOT NULL,
        is_culprit INTEGER NOT NULL DEFAULT 0,
        confession TEXT NOT NULL,
        innocent_statement TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases (id)
    );

    CREATE TABLE clues (
        id TEXT PRIMARY KEY,
        case_id TEXT NOT NULL,
        scene_id TEXT,
        title TEXT NOT NULL,
        category TEXT NOT NULL, -- 'Forensic', 'Physical', 'Document', 'Testimony'
        short_desc TEXT NOT NULL,
        full_analysis TEXT NOT NULL,
        icon TEXT NOT NULL,
        is_key_evidence INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (case_id) REFERENCES cases (id),
        FOREIGN KEY (scene_id) REFERENCES crime_scenes (id)
    );

    CREATE TABLE suspect_dialogues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        suspect_id TEXT NOT NULL,
        topic TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        reaction_mood TEXT NOT NULL DEFAULT 'neutral', -- 'nervous', 'angry', 'smug', 'calm'
        unlocks_clue_id TEXT,
        FOREIGN KEY (suspect_id) REFERENCES suspects (id)
    );

    CREATE TABLE contradictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        suspect_id TEXT NOT NULL,
        clue_id TEXT NOT NULL,
        callout_text TEXT NOT NULL,
        suspect_response TEXT NOT NULL,
        breaks_alibi INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (suspect_id) REFERENCES suspects (id),
        FOREIGN KEY (clue_id) REFERENCES clues (id)
    );

    CREATE TABLE case_solutions (
        case_id TEXT PRIMARY KEY,
        culprit_suspect_id TEXT NOT NULL,
        weapon_clue_id TEXT NOT NULL,
        key_proof_clue_id TEXT NOT NULL,
        motive_summary TEXT NOT NULL,
        full_verdict_narrative TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases (id),
        FOREIGN KEY (culprit_suspect_id) REFERENCES suspects (id)
    );

    CREATE TABLE detective_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        note_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases (id)
    );
    """)

    conn.commit()
    conn.close()
    print("Database tables initialized.")

if __name__ == "__main__":
    init_db()
