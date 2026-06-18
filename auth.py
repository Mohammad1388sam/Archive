import bcrypt

from database import mysqlconnector


class UserManager:

    @staticmethod
    def register(username, password):

        conn = mysqlconnector()
        cur = conn.cursor()

        password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        cur.execute(
            """
            INSERT INTO users
            (
                username,
                password_hash
            )
            VALUES
            (
                %s,
                %s
            )
            """,
            (
                username,
                password_hash
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def login(username, password):

        conn = mysqlconnector()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                password_hash
            FROM users
            WHERE username=%s
            """,
            (username,)
        )

        result = cur.fetchone()

        conn.close()

        if not result:
            return None

        user_id = result[0]
        password_hash = result[1]

        if bcrypt.checkpw(
            password.encode(),
            password_hash.encode()
        ):
            return user_id

        return None