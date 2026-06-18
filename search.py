from database import db


class Search:

    @staticmethod
    def search(keyword):

        conn = db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                title,
                topic,
                description,
                audio_path,
                summary_path,
                views
            FROM lectures

            WHERE
                title LIKE %s
                OR topic LIKE %s
                OR description LIKE %s
                OR summary_content LIKE %s
            """,
            (
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%"
            )
        )

        result = cur.fetchall()

        conn.close()

        return result