from database import db

def normalize_text(text: str):

    if not text:
        return ""

    text = text.replace("ي", "ی")
    text = text.replace("ك", "ک")
    text = text.replace("\u200c", " ")

    return text.strip().lower()


class Search:

    @staticmethod
    def search(keyword):

        keyword = normalize_text(keyword)

        conn = db()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                title,
                topic,
                description,
                audio_path,
                summary_path
            FROM lectures
        """)

        rows = cur.fetchall()
        conn.close()

        results = []

        for row in rows:

            text_blob = " ".join([
                str(row[1]),
                str(row[2]),
                str(row[3])
            ])

            text_blob = normalize_text(text_blob)

            if keyword in text_blob:
                results.append(row)

        return results