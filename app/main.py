from pathlib import Path
import sys
from uuid import uuid4

import streamlit as st

# Ensure package imports work both locally and on Streamlit Cloud.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config import IMAGE_DIR
from database.db import (
    authenticate_user,
    create_user,
    get_relevant_history,
    get_user_generations,
    init_db,
    save_generation,
)
from services.gemini_service import generate_text
from services.image_service import generate_image
from utils.utils import validate_prompt


def save_image_file(image_bytes: bytes) -> str:
    """
    Save generated images locally so they can be shown again and downloaded later.
    """
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    image_path = IMAGE_DIR / f"generation_{uuid4().hex}.jpg"
    image_path.write_bytes(image_bytes)
    return str(image_path)


def initialize_session() -> None:
    if "user" not in st.session_state:
        st.session_state.user = None


def render_auth_screen() -> None:
    st.title("Multimodal Hospitality Creator")
    st.write("Sign up or log in to create and save hospitality concept designs.")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            login_clicked = st.form_submit_button("Login")

        if login_clicked:
            if not username.strip() or not password.strip():
                st.error("Please enter both username and password.")
            else:
                success, user = authenticate_user(username, password)
                if success:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    with signup_tab:
        with st.form("signup_form"):
            username = st.text_input("Choose a username", key="signup_username")
            password = st.text_input("Choose a password", type="password", key="signup_password")
            signup_clicked = st.form_submit_button("Create Account")

        if signup_clicked:
            if not username.strip() or not password.strip():
                st.error("Please enter both username and password.")
            else:
                success, message = create_user(username, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)


def render_generator(user: dict) -> None:
    st.title("Multimodal Hospitality Creator")
    st.write(f"Logged in as `{user['username']}`")

    with st.sidebar:
        st.header("Account")
        st.write(f"User: `{user['username']}`")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

    page = st.sidebar.radio("Navigation", ["Generate Design", "My Designs"])

    if page == "Generate Design":
        prompt = st.text_input(
            "Enter a hospitality prompt",
            placeholder="Luxury beach resort with sunset view",
        )

        if st.button("Generate"):
            is_valid, error_message = validate_prompt(prompt)

            if not is_valid:
                st.error(error_message)
            else:
                with st.spinner("Generating concept..."):
                    try:
                        personal_context = get_relevant_history(user["id"], prompt)
                        text_result = generate_text(prompt, personal_context)
                        image_result = generate_image(prompt)
                        image_path = save_image_file(image_result)
                        save_generation(user["id"], prompt, text_result, image_path)

                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Generated Text")
                            st.write(text_result)
                            if personal_context:
                                st.caption(
                                    f"Personal RAG used {len(personal_context)} related saved design(s) "
                                    "from your history to refine this text."
                                )

                        with col2:
                            st.subheader("Generated Image")
                            st.image(image_result, caption=prompt, use_container_width=True)

                        st.success("Design saved to your history.")
                    except Exception as exc:
                        st.error(str(exc))
    else:
        st.header("My Designs")
        records = get_user_generations(user["id"])

        if not records:
            st.info("No saved designs yet. Generate a concept to see it here.")
            return

        for record in records:
            st.subheader(record["prompt"])
            st.caption(f"Created at: {record['created_at']}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(record["generated_text"])

            with col2:
                image_path = Path(record["image_path"])
                if image_path.exists():
                    image_bytes = image_path.read_bytes()
                    st.image(image_bytes, caption=record["prompt"], use_container_width=True)
                    st.download_button(
                        label="Download Image",
                        data=image_bytes,
                        file_name=f"{record['prompt'].replace(' ', '_')}.jpg",
                        mime="image/jpeg",
                        key=f"download_{record['id']}",
                    )
                else:
                    st.warning("Saved image file was not found on disk.")

            st.divider()


st.set_page_config(page_title="Multimodal Hospitality Creator", layout="wide")
init_db()
initialize_session()

if st.session_state.user:
    render_generator(st.session_state.user)
else:
    render_auth_screen()
