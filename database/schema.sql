-- ============================================================
-- Event Meeting Minutes Manager - Database Schema (SQLite)
-- ============================================================

CREATE TABLE IF NOT EXISTS meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,          -- format: YYYY-MM-DD
    time TEXT NOT NULL,          -- format: HH:MM
    location TEXT,
    chairperson TEXT,
    participants TEXT,           -- comma separated
    agenda TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS minutes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    discussion TEXT,             -- hasil pembahasan agenda
    decisions TEXT,               -- keputusan rapat
    additional_notes TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS action_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER,
    task_name TEXT NOT NULL,
    assignee TEXT,
    priority TEXT CHECK(priority IN ('Low','Medium','High')) DEFAULT 'Medium',
    deadline TEXT,                -- format: YYYY-MM-DD
    status TEXT CHECK(status IN ('To Do','In Progress','Done')) DEFAULT 'To Do',
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE INDEX IF NOT EXISTS idx_action_items_status ON action_items(status);
CREATE INDEX IF NOT EXISTS idx_action_items_deadline ON action_items(deadline);
CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings(date);
