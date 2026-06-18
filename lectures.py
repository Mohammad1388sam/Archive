from database import db


def read_summary_file(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    except:
        return ""


class LectureManager:

    @staticmethod
    def add_lecture(
        title,
        topic,
        description,
        audio_path,
        summary_path,
        uploaded_by
    ):

        summary_content = read_summary_file(
            summary_path
        )

        conn = db()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO lectures
            (
                title,
                topic,
                description,
                audio_path,
                summary_path,
                summary_content,
                uploaded_by
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                title,
                topic,
                description,
                audio_path,
                summary_path,
                summary_content,
                uploaded_by
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_all():

        conn = db()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            lectures.id,
            lectures.title,
            lectures.topic,
            users.username,
            lectures.views,
            lectures.downloads
        FROM lectures

        LEFT JOIN users
        ON lectures.uploaded_by = users.id

        ORDER BY lectures.created_at DESC
        """)

        result = cur.fetchall()

        conn.close()

        return result

    @staticmethod
    def increase_view(lecture_id):

        conn = db()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE lectures
            SET views = views + 1
            WHERE id=%s
            """,
            (lecture_id,)
        )

        conn.commit()
        conn.close()
