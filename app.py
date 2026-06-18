import os
import uuid
import pathlib
import streamlit as st

from database import create_tables
from auth import UserManager
from lectures import LectureManager
from search import Search

create_tables()

os.makedirs(
    "uploads/audio",
    exist_ok=True
)

os.makedirs(
    "uploads/summaries",
    exist_ok=True
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None


st.title(" آرشیو گعده ها")


if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(
        ["ورود", "ثبت نام"]
    )

    with tab1:

        username = st.text_input(
            "نام کاربری"
        )

        password = st.text_input(
            "رمز عبور",
            type="password"
        )

        if st.button("ورود"):

            user_id = UserManager.login(
                username,
                password
            )

            if user_id:

                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username

                st.rerun()

            else:

                st.error("خطا در ورود")

    with tab2:

        username = st.text_input(
            "نام کاربری جدید"
        )

        password = st.text_input(
            "رمز جدید",
            type="password"
        )

        if st.button("ثبت نام"):

            UserManager.register(
                username,
                password
            )

            st.success("ثبت شد")

else:

    st.sidebar.success(
        st.session_state.username
    )

    page = st.sidebar.radio(
        "منو",
        [
            "جستجو",
            "آپلود",
            "آرشیو"
        ]
    )

    if page == "آپلود":

        title = st.text_input(
            "عنوان"
        )

        topic = st.text_input(
            "موضوع"
        )

        description = st.text_area(
            "توضیحات"
        )

        audio_file = st.file_uploader(
            "mp3",
            type=["mp3"]
        )

        summary_file = st.file_uploader(
            "txt",
            type=["txt"]
        )

        if st.button("ذخیره"):

            audio_path = None
            summary_path = None

            if audio_file:

                ext = pathlib.Path(
                    audio_file.name
                ).suffix

                filename = (
                    f"{uuid.uuid4()}{ext}"
                )

                audio_path = (
                    f"uploads/audio/{filename}"
                )

                with open(
                    audio_path,
                    "wb"
                ) as f:

                    f.write(
                        audio_file.getbuffer()
                    )

            if summary_file:

                ext = pathlib.Path(
                    summary_file.name
                ).suffix

                filename = (
                    f"{uuid.uuid4()}{ext}"
                )

                summary_path = (
                    f"uploads/summaries/{filename}"
                )

                with open(
                    summary_path,
                    "wb"
                ) as f:

                    f.write(
                        summary_file.getbuffer()
                    )

            LectureManager.add_lecture(
                title,
                topic,
                description,
                audio_path,
                summary_path,
                st.session_state.user_id
            )

            st.success(
                "ثبت شد"
            )

    elif page == "جستجو":

        keyword = st.text_input(
            "عبارت جستجو"
        )

        if keyword:

            results = Search.search(
                keyword
            )

            for row in results:

                st.subheader(row[1])

                st.write(
                    f"موضوع: {row[2]}"
                )

                st.write(row[3])

                if row[4]:

                    st.audio(row[4])

    elif page == "آرشیو":

        data = LectureManager.get_all()

        for row in data:

            st.write(
                f"{row[1]} | {row[2]} | {row[3]}"
            )
