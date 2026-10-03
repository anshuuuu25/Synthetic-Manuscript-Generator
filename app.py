import io
import streamlit as st
import yaml

from src.generator import SyntheticManuscriptGenerator


st.set_page_config(
    page_title="Historical Manuscript Synthetic Generator",
    layout="wide"
)


@st.cache_data
def load_config():
    with open(
        "config/config.yaml",
        "r",
        encoding="utf-8"
    ) as f:
        return yaml.safe_load(f)


cfg = load_config()

st.title(
    "Historical Manuscript Synthetic Generator"
)


with st.sidebar:

    st.header("Configuration")

    selected_script = st.selectbox(
        "Target Script",
        list(cfg["scripts"].keys())
    )

    script_cfg = cfg["scripts"][selected_script]

    bg_mode = st.radio(
        "Background Source",
        [
            "Uploaded Asset Folder",
            "Procedurally Generated"
        ]
    )

    bg_type = st.selectbox(
        "Background Type",
        [
            "Aged Handmade Paper",
            "Aged Paper",
            "Copper Plate",
            "Palm Leaf",
            "Stone Inscription"
        ]
    )

    layout_mode = st.selectbox(
        "Layout Mode",
        [
            "Single Block",
            "Multi Block",
            "Marginal"
        ]
    )

    ink_name = st.selectbox(
        "Ink Color",
        [
            "Dark Brown",
            "Black",
            "Golden Brown",
            "Dark Green"
        ]
    )

    ink_colors = {
        "Dark Brown": (45, 28, 18),
        "Black": (18, 18, 16),
        "Golden Brown": (82, 52, 18),
        "Dark Green": (25, 55, 32)
    }

    font_size = st.slider(
        "Font Size",
        30,
        90,
        int(cfg["defaults"]["font_size"])
    )

    paper_aging = st.slider(
        "Paper Aging",
        0,
        100,
        int(cfg["defaults"]["paper_aging"])
    )

    handwriting_var = st.slider(
        "Handwriting Variation",
        0,
        100,
        int(cfg["defaults"]["handwriting_var"])
    )

    artifacts = st.slider(
        "Artifacts",
        0,
        100,
        int(cfg["defaults"]["artifacts"])
    )

    page_warping = st.slider(
        "Page Warping",
        0,
        100,
        int(cfg["defaults"]["page_warping"])
    )

    seed = st.number_input(
        "Seed",
        value=42,
        step=1
    )


use_procedural = (
    bg_mode == "Procedurally Generated"
)

left, right = st.columns(
    [1, 1.35],
    gap="large"
)


with left:

    st.subheader("Enter Raw Text")

    sample_text = st.text_area(
        f"{script_cfg['display_name']} Ground Truth",
        value=script_cfg["sample_text"],
        height=430
    )

    generate = st.button(
        "Generate Manuscript Folio",
        type="primary",
        use_container_width=True
    )


if generate:

    if not sample_text.strip():

        st.error(
            "Please enter some text."
        )

    else:

        try:

            generator = SyntheticManuscriptGenerator(
                script_key=selected_script,
                font_path=script_cfg["font_path"],
                fallback_font=script_cfg.get(
                    "fallback_font"
                )
            )

            image, ground_truth = (
                generator.generate_sample(
                    text_input=sample_text,
                    bg_type=bg_type,
                    layout_mode=layout_mode.lower().replace(
                        " ",
                        "_"
                    ),
                    font_size=font_size,
                    ink_color=ink_colors[ink_name],
                    aging_val=paper_aging / 100,
                    handwriting_variation=handwriting_var,
                    artifact_value=artifacts,
                    page_warping=page_warping,
                    use_procedural=use_procedural,
                    seed=int(seed)
                )
            )

            st.session_state["image"] = image
            st.session_state["ground_truth"] = ground_truth
            st.session_state["script"] = selected_script

        except Exception as e:

            st.error(
                f"Generation failed: {e}"
            )


with right:

    st.subheader("Generated Manuscript")

    if "image" not in st.session_state:

        st.info(
            "Generated manuscript will appear here."
        )

    else:

        image = st.session_state["image"]
        ground_truth = (
            st.session_state["ground_truth"]
        )

        script = (
            st.session_state["script"]
        )

        st.image(
            image,
            use_container_width=True
        )

        image_buffer = io.BytesIO()

        image.save(
            image_buffer,
            format="PNG"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "Download PNG",
                image_buffer.getvalue(),
                f"{script}_folio.png",
                "image/png",
                use_container_width=True
            )

        with col2:

            st.download_button(
                "Download Ground Truth",
                ground_truth,
                f"{script}_gt.md",
                "text/markdown",
                use_container_width=True
            )