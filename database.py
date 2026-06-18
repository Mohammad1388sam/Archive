import os
import psycopg2



def db():
    """
    اتصال به دیتابیس PostgreSQL (Supabase)
    """
    return psycopg2.connect(
        os.getenv("DB_URL")
    )


def create_tables():

    conn = db()
    cur = conn.cursor()

    # =========================
    # USERS TABLE
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    # =========================
    # LECTURES TABLE
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS lectures (
        id BIGSERIAL PRIMARY KEY,

        title TEXT NOT NULL,
        topic TEXT,
        description TEXT,

        audio_path TEXT,
        summary_path TEXT,
        summary_content TEXT,

        uploaded_by BIGINT,

        views INT DEFAULT 0,
        downloads INT DEFAULT 0,

        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    # Foreign key (optional but recommended)
    cur.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint WHERE conname = 'fk_uploaded_by'
        ) THEN
            ALTER TABLE lectures
            ADD CONSTRAINT fk_uploaded_by
            FOREIGN KEY (uploaded_by)
            REFERENCES users(id)
            ON DELETE SET NULL;
        END IF;
    END $$;
    """)

    conn.commit()
    conn.close()