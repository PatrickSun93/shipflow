import streamlit as st
import os
from pathlib import Path
from src.orchestrator import ShipflowOrchestrator

st.set_page_config(page_title="ShipFlow Orchestrator", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS injected for polished design ---
st.markdown("""
<style>
/* Main Background and text colors */
.stApp {
    background-color: #f7f9fc;
    color: #1e293b;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Header Styling */
h1 {
    color: #0f172a;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

h2, h3 {
    color: #334155;
    font-weight: 600;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
    padding-top: 2rem;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
    padding: 10px 15px;
    border-radius: 8px 8px 0px 0px;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #2563eb;
    background-color: #eff6ff;
}
.stTabs [aria-selected="true"] {
    color: #1d4ed8 !important;
    border-bottom: 3px solid #1d4ed8 !important;
}

/* Buttons Styling */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    border: none;
    transition: background-color 0.2s ease, transform 0.1s ease;
}
.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
    border: none;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Text Input & Area styling */
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    padding: 10px;
    background-color: #ffffff;
    color: #0f172a;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 1px #2563eb;
}

/* Info, Success, Error Banners */
.stAlert {
    border-radius: 8px;
    border-left-width: 4px;
}

/* Card-like containers for content areas */
.css-1r6slb0 {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}
</style>
""", unsafe_allow_html=True)

st.title("🚢 ShipFlow Orchestrator")
st.markdown("<p style='font-size: 1.1rem; color: #475569;'>A multi-agent product team in a folder. Solo-dev workflow UI wrapper.</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state for tracking
if "target_dir" not in st.session_state:
    st.session_state.target_dir = os.getcwd()
if "shipflow_repo" not in st.session_state:
    # Default to assuming app is run from `shipflow-orchestrator` and `shipflow` is parallel to it
    default_repo = Path(os.getcwd()).parent / "shipflow"
    st.session_state.shipflow_repo = str(default_repo.resolve()) if default_repo.exists() else ""
if "current_slug" not in st.session_state:
    st.session_state.current_slug = ""
if "current_brief" not in st.session_state:
    st.session_state.current_brief = ""
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None

# Sidebar for Setup
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("Set up your directories to initialize the agents.")
    target_dir_input = st.text_input("Target Directory", value=st.session_state.target_dir, help="Where the docs/shipflow output will be created.")
    repo_dir_input = st.text_input("ShipFlow Repo Path", value=st.session_state.shipflow_repo, help="Path to the original shipflow repository containing prompts.")

    if st.button("Initialize Repo ✨"):
        st.session_state.target_dir = target_dir_input
        st.session_state.shipflow_repo = repo_dir_input

        try:
            orch = ShipflowOrchestrator(
                target_dir=st.session_state.target_dir,
                shipflow_repo_path=st.session_state.shipflow_repo
            )
            orch.sf_init()
            st.session_state.orchestrator = orch
            st.success("✅ Initialized ShipFlow directories successfully!")
        except Exception as e:
            st.error(f"Failed to initialize: {str(e)}")

# Main content
if st.session_state.orchestrator is None:
    st.info("👋 Welcome! Please set your configuration and click **Initialize Repo** in the sidebar to begin.")
else:
    # Use tabs for different phases
    tab_discover, tab_brief, tab_spec, tab_build, tab_ship = st.tabs([
        "💡 1. Discover", "📝 2. Brief", "🏗️ 3. Spec", "🛠️ 4. Build & Verify", "🚀 5. Ship"
    ])

    # 1. Discover Phase
    with tab_discover:
        st.subheader("Start Idea Discovery")
        st.markdown("Turn a raw idea into a well-formed brief by interrogating it from three independent lenses (Tech, UX, Business).")
        idea_input = st.text_area("What's your idea?", placeholder="e.g., A dark mode toggle for the main dashboard")

        if st.button("Run /sf-discover", key="btn_discover"):
            if not idea_input.strip():
                st.warning("Please enter an idea.")
            else:
                with st.spinner("🧠 Spawning Tech, UX, and Business personas... This might take a minute."):
                    try:
                        questions = st.session_state.orchestrator.sf_discover(idea_input)
                        st.session_state.current_slug = st.session_state.orchestrator._slugify(idea_input)

                        st.success(f"Discovery complete! Idea slugged as: **{st.session_state.current_slug}**")
                        st.markdown("### ❓ Questions from Personas")
                        st.markdown(f"> {questions}")

                        st.info("👉 **Next:** Answer these questions in your IDE by creating `docs/shipflow/discovery/<slug>/answers.md`, then proceed to the Brief tab.")
                    except Exception as e:
                        st.error(f"Error during discovery: {str(e)}")

    # 2. Brief Phase
    with tab_brief:
        st.subheader("Assemble Product Brief")
        st.markdown("Compile the personas' analysis and run the **Challenger** agent to stress-test your idea.")
        slug_input = st.text_input("Idea Slug", value=st.session_state.current_slug, placeholder="e.g., dark-mode-toggle")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Step A: Assemble")
            if st.button("Run /sf-brief", key="btn_brief"):
                if not slug_input.strip():
                    st.warning("Please enter a slug.")
                else:
                    with st.spinner("🛠️ Assembling brief and spawning challenger..."):
                        try:
                            st.session_state.current_slug = slug_input
                            brief_path = st.session_state.orchestrator.sf_brief(slug_input)
                            st.session_state.current_brief = brief_path
                            st.success(f"✅ Brief created at: `{brief_path}`")
                        except Exception as e:
                            st.error(f"Error during brief assembly: {str(e)}")

        with col2:
            st.markdown("#### Step B: Gate 1 Review")
            brief_input = st.text_input("Brief File Path", value=st.session_state.current_brief)
            if st.button("Run /sf-check-brief", key="btn_check_brief"):
                if not brief_input.strip():
                    st.warning("Please enter a brief file path.")
                else:
                    with st.spinner("🕵️‍♂️ Tech Lead and Product Lead are reviewing..."):
                        try:
                            st.session_state.orchestrator.sf_check_brief(brief_input)
                            st.success("✅ Review complete! Check the brief file for the Verdict.")
                        except Exception as e:
                            st.error(f"Error during check-brief: {str(e)}")

    # 3. Spec Phase
    with tab_spec:
        st.subheader("Generate Stories")
        st.markdown("Translate an approved brief into 5–10 stories, sliced by dependency, each small enough to implement in one Build pass.")
        spec_brief_input = st.text_input("Approved Brief File Path", value=st.session_state.current_brief, key="input_spec_brief")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("#### Step C: Spec Creation")
            if st.button("Run /sf-spec", key="btn_spec"):
                if not spec_brief_input.strip():
                    st.warning("Please enter an approved brief file path.")
                else:
                    with st.spinner("🔪 Slicing brief into stories..."):
                        try:
                            st.session_state.orchestrator.sf_spec(spec_brief_input)
                            st.success("✅ Stories successfully generated in `docs/shipflow/stories/`!")
                        except Exception as e:
                            st.error(f"Error during spec generation: {str(e)}")

        with col4:
            st.markdown("#### Step D: Gate 2 Review")
            if st.button("Run /sf-check-plan", key="btn_check_plan"):
                with st.spinner("🔬 Tech Lead is reviewing the stories..."):
                    try:
                        st.session_state.orchestrator.sf_check_plan()
                        st.success("✅ Per-story review complete! Check the stories for Verdicts.")
                    except Exception as e:
                        st.error(f"Error during check-plan: {str(e)}")

    # 4. Build Phase
    with tab_build:
        st.subheader("Build & Verify")
        st.markdown("Implement the stories, run tests, and verify against the brief.")
        story_file_input = st.text_input("Story File Path to Build", placeholder="e.g., docs/shipflow/stories/STORY-0001.md")

        col5, col6 = st.columns(2)

        with col5:
            st.markdown("#### Step E: Build & Check (Gate 3)")
            if st.button("Run /sf-build", key="btn_build"):
                if not story_file_input.strip():
                    st.warning("Please enter a story file path.")
                else:
                    with st.spinner("💻 Building the story..."):
                        try:
                            st.session_state.orchestrator.sf_build(story_file_input)
                            st.success("✅ Build complete!")
                        except Exception as e:
                            st.error(f"Error during build: {str(e)}")

            if st.button("Run /sf-check-build", key="btn_check_build"):
                with st.spinner("🔎 Code Reviewer is checking the build..."):
                    try:
                        st.session_state.orchestrator.sf_check_build()
                        st.success("✅ Build review complete! Check verdicts.")
                    except Exception as e:
                        st.error(f"Error during check-build: {str(e)}")

        with col6:
            st.markdown("#### Step F: Verify Intent")
            if st.button("Run /sf-verify", key="btn_verify"):
                if not story_file_input.strip():
                    st.warning("Please enter a story file path.")
                else:
                    with st.spinner("🔍 QA Lead is verifying against parent brief..."):
                        try:
                            st.session_state.orchestrator.sf_verify(story_file_input)
                            st.success("✅ Verification report generated on story!")
                        except Exception as e:
                            st.error(f"Error during verify: {str(e)}")

    # 5. Ship Phase
    with tab_ship:
        st.subheader("Ship Release")
        st.markdown("Cut the final release, check for blockers, and archive the artifacts.")

        col7, col8 = st.columns(2)
        with col7:
            st.markdown("#### Step G: Ship Check (Gate 4)")
            if st.button("Run /sf-check-ship", key="btn_check_ship"):
                with st.spinner("🔬 Tech Lead doing final last-chance review..."):
                    try:
                        st.session_state.orchestrator.sf_check_ship()
                        st.success("✅ Ready to ship!")
                    except Exception as e:
                        st.error(f"Error during check-ship: {str(e)}")

        with col8:
            st.markdown("#### Step H: Ship It 🚀")
            if st.button("Run /sf-ship", key="btn_ship"):
                with st.spinner("📦 Release Manager is cutting the release..."):
                    try:
                        st.session_state.orchestrator.sf_ship()
                        st.success("✅ Release cut! Check `docs/shipflow/releases` and `docs/shipflow/index.md`.")
                    except Exception as e:
                        st.error(f"Error during shipping: {str(e)}")
