import streamlit as st

from services.gemini_service import generate_text
from services.image_service import generate_image
from utils.utils import validate_prompt


st.set_page_config(
    page_title="Hospitality Concept Visualizer",
    page_icon="🏨",
    layout="wide",
)

SAMPLE_PROMPTS = [
    "Luxury beach resort with sunset view",
    "Boutique mountain lodge with warm wood interiors and snow panorama",
    "Eco-friendly jungle retreat with treehouse villas and infinity pool",
    "Modern city business hotel with rooftop lounge and skyline views",
]

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

with st.sidebar:
    st.header("Workspace")
    st.caption("Try sample prompts quickly.")

    st.divider()
    selected_sample = st.selectbox("Sample prompt", ["Select a sample..."] + SAMPLE_PROMPTS)

    if st.button("Use Selected Sample", use_container_width=True):
        if selected_sample != "Select a sample...":
            st.session_state.prompt_input = selected_sample
            st.rerun()

    if st.button("Clear Results", use_container_width=True):
        st.session_state.generated_text = ""
        st.session_state.generated_image = None
        st.session_state.last_prompt = ""
        st.rerun()

st.title("Hospitality Concept Visualizer")
st.markdown(
    "Create a hospitality concept narrative and visual from one prompt using Gemini and Stable Diffusion."
)

with st.expander("Prompt Tips", expanded=False):
    st.markdown(
        "- Mention the setting (beach, mountain, city, desert)\n"
        "- Add design style (modern, rustic, minimalist, luxury)\n"
        "- Include mood or time (sunset, cozy evening, bright morning)\n"
        "- Note guest experience elements (spa, rooftop, fine dining, family-friendly)"
    )

with st.form("concept_form"):
    prompt = st.text_area(
        "Describe your hospitality concept",
        value=st.session_state.prompt_input,
        placeholder="Example: Luxury beach resort with sunset view, open-air dining, and private villas.",
        height=140,
        max_chars=500,
    )
    col_submit, col_reset = st.columns([2, 1])
    generate_clicked = col_submit.form_submit_button(
        "✨ Generate Concept",
        type="primary",
        use_container_width=True,
    )
    reset_prompt_clicked = col_reset.form_submit_button(
        "Reset Prompt",
        use_container_width=True,
    )

if reset_prompt_clicked:
    st.session_state.prompt_input = ""
    st.rerun()

if generate_clicked:
    st.session_state.prompt_input = prompt
    is_valid, error_message = validate_prompt(prompt)

    if not is_valid:
        st.error(error_message)
    else:
        with st.spinner("Generating concept text and image..."):
            try:
                text_result = generate_text(prompt)
                image_result = generate_image(prompt)

                st.session_state.generated_text = text_result
                st.session_state.generated_image = image_result
                st.session_state.last_prompt = prompt
            except Exception as exc:
                st.error(str(exc))

if st.session_state.last_prompt:
    prompt_length = len(st.session_state.last_prompt.strip())
    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Prompt Length", f"{prompt_length} chars")
    metric_col2.metric("Generation Status", "Ready")

if st.session_state.generated_text or st.session_state.generated_image:
    st.subheader("Generated Concept")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("#### Concept Description")
        st.write(st.session_state.generated_text)
        if st.session_state.generated_text:
            st.download_button(
                "Download Description (.txt)",
                data=st.session_state.generated_text,
                file_name="hospitality_concept_description.txt",
                mime="text/plain",
                use_container_width=True,
            )

    with col2:
        st.markdown("#### Concept Visual")
        if st.session_state.generated_image:
            st.image(
                st.session_state.generated_image,
                caption=st.session_state.last_prompt,
                use_container_width=True,
            )
            st.download_button(
                "Download Image (.png)",
                data=st.session_state.generated_image,
                file_name="hospitality_concept_visual.png",
                mime="image/png",
                use_container_width=True,
            )
else:
    st.info("Enter a prompt and click Generate Concept to see your results here.")
