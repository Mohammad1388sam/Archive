import os
import uuid
import pathlib
import streamlit as st

from database import create_tables
from auth import UserManager
from lectures import LectureManager
from search import Search

create_tables()

# -------------------------
# folders
# -------------------------
os.makedirs("uploads/audio", exist_ok=True)
os.makedirs("uploads/summaries", exist_ok=True)

# -------------------------
# session state
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None

st.title("📚 آرشیو گعده‌ها")

# -------------------------
# AUTH
# -------------------------
if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["ورود", "ثبت نام"])

    with tab1:
        username = st.text_input("نام کاربری", key="login_user")
        password = st.text_input("رمز عبور", type="password", key="login_pass")

        if st.button("ورود"):
            user_id = UserManager.login(username, password)

            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.rerun()
            else:
                st.error("خطا در ورود")

    with tab2:
        username = st.text_input("نام کاربری جدید", key="reg_user")
        password = st.text_input("رمز جدید", type="password", key="reg_pass")

        if st.button("ثبت نام"):
            UserManager.register(username, password)
            st.success("ثبت شد")

# -------------------------
# MAIN APP
# -------------------------
else:

    st.sidebar.success(st.session_state.username)

    page = st.sidebar.radio("منو", ["جستجو", "آپلود", "آرشیو"])

    # =====================
    # UPLOAD
    # =====================
    if page == "آپلود":

        title = st.text_input("عنوان")
        topic = st.text_input("موضوع")
        description = st.text_area("توضیحات")

        audio_file = st.file_uploader("فایل mp3", type=["mp3"])
        summary_file = st.file_uploader("فایل txt", type=["txt"])

        if st.button("ذخیره"):

            audio_path = None
            summary_path = None

            # ---- audio ----
            if audio_file:
                ext = pathlib.Path(audio_file.name).suffix
                filename = f"{uuid.uuid4()}{ext}"
                audio_path = f"uploads/audio/{filename}"

                with open(audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())

            # ---- summary ----
            if summary_file:
                ext = pathlib.Path(summary_file.name).suffix
                filename = f"{uuid.uuid4()}{ext}"
                summary_path = f"uploads/summaries/{filename}"

                with open(summary_path, "wb") as f:
                    f.write(summary_file.getbuffer())

            LectureManager.add_lecture(
                title,
                topic,
                description,
                audio_path,
                summary_path,
                st.session_state.user_id
            )

            st.success("ثبت شد")

    # =====================
    # SEARCH
    # =====================
    elif page == "جستجو":

        keyword = st.text_input("عبارت جستجو")

        if keyword:

            results = Search.search(keyword)

            for row in results:

                st.subheader(row[1])
                st.write(f"موضوع: {row[2]}")
                st.write(row[3])

                # -------------------------
                # AUDIO (fix download)
                # -------------------------
                if row[4] and os.path.exists(row[4]):

                    st.audio(row[4])

                    try:
                        with open(row[4], "rb") as f:
                            st.download_button(
                                "⬇ دانلود فایل صوتی",
                                data=f.read(),
                                file_name=os.path.basename(row[4]),
                                mime="audio/mpeg",
                                key=f"audio_{row[0]}"
                            )
                    except Exception as e:
                        st.error(f"خطا در دانلود صوت: {e}")

                # -------------------------
                # TXT (FIXED)
                # -------------------------
                if row[5] and os.path.exists(row[5]):

                    try:
                        with open(row[5], "rb") as f:
                            st.download_button(
                                "⬇ دانلود فایل متن",
                                data=f.read(),
                                file_name=os.path.basename(row[5]),
                                mime="text/plain",
                                key=f"txt_{row[0]}"
                            )
                    except Exception as e:
                        st.error(f"خطا در دانلود متن: {e}")

    # =====================
    # ARCHIVE
    # =====================
    elif page == "آرشیو":

        data = LectureManager.get_all()

        for row in data:
            st.write(f"{row[1]} | {row[2]} | {row[3]}")