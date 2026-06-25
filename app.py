import uuid

import streamlit as st
from langchain_core.messages import HumanMessage

from agent.repository_graph import repository_graph
from agent.contribution_graph import contribution_graph


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Open Source Onboarding Agent",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Open Source Onboarding Agent")
st.caption(
    "Analyze GitHub repositories, discover beginner-friendly issues, "
    "and generate a complete contribution guide."
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "repo_state" not in st.session_state:
    st.session_state.repo_state = None

if "repository_analysis" not in st.session_state:
    st.session_state.repository_analysis = None

if "beginner_issues" not in st.session_state:
    st.session_state.beginner_issues = []

if "contribution_result" not in st.session_state:
    st.session_state.contribution_result = None


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Project Information")

    st.markdown(
        """
        **Workflow**

        1. Analyze Repository
        2. Discover Beginner Issues
        3. Select Issue
        4. Generate Contribution Guide
        5. Draft Pull Request
        """
    )

    st.divider()

    st.write("Thread ID")
    st.code(st.session_state.thread_id)


# --------------------------------------------------
# Repository Input
# --------------------------------------------------

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/github/codeql"
)


# --------------------------------------------------
# Repository Analysis
# --------------------------------------------------

if st.button(
    "Analyze Repository",
    use_container_width=True
):

    if not repo_url:

        st.error(
            "Please enter a repository URL."
        )

    else:

        with st.spinner(
            "Analyzing repository..."
        ):

            initial_state = {
                "messages": [
                    HumanMessage(
                        content=f"Analyze repository: {repo_url}"
                    )
                ],
                "repo_url": repo_url,
                "selected_issue": None,
                "repo_metadata": None,
                "repo_tree": None,
                "beginner_issues": None,
                "issue_details": None,
                "repository_analysis": None,
                "issue_analysis": None,
                "file_mapping_analysis": None,
                "relevant_files": None,
                "issues_dropdown": None,
                "implementation_plan": None,
                "pr_draft": None,
            }

            result = repository_graph.invoke(
                initial_state,
                config={
                    "configurable": {
                        "thread_id":
                        st.session_state.thread_id
                    }
                }
            )

            st.session_state.repo_state = result

            st.session_state.repository_analysis = (
                result.get(
                    "repository_analysis",
                    ""
                )
            )

            st.session_state.beginner_issues = (
                result.get(
                    "beginner_issues",
                    []
                )
            )

        st.success(
            "Repository analysis completed."
        )


# --------------------------------------------------
# Repository Results
# --------------------------------------------------

if st.session_state.repository_analysis:

    st.divider()

    st.subheader(
        "📊 Repository Analysis"
    )

    st.markdown(
        st.session_state.repository_analysis
    )

    repo_state = st.session_state.repo_state

    repo_metadata = repo_state.get(
        "repo_metadata",
        {}
    )

    if repo_metadata:

        st.subheader(
            "Repository Metrics"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Language",
                repo_metadata.get(
                    "language",
                    "N/A"
                )
            )

        with col2:
            st.metric(
                "Stars",
                repo_metadata.get(
                    "stars",
                    0
                )
            )

        with col3:
            st.metric(
                "Forks",
                repo_metadata.get(
                    "forks",
                    0
                )
            )

        with col4:
            st.metric(
                "Open Issues",
                repo_metadata.get(
                    "open_issues",
                    0
                )
            )


# --------------------------------------------------
# Issue Selection
# --------------------------------------------------

issues = st.session_state.beginner_issues

if issues:

    st.divider()

    st.subheader(
        "🐣 Beginner-Friendly Issues"
    )

    issue_map = {}

    for issue in issues:

        label = (
            f"#{issue['number']} - "
            f"{issue['title']}"
        )

        issue_map[label] = (
            issue["number"]
        )

    selected_issue_label = st.selectbox(
        "Select an Issue",
        options=list(issue_map.keys())
    )

    if st.button(
        "Generate Contribution Guide",
        use_container_width=True
    ):

        issue_number = issue_map[
            selected_issue_label
        ]

        with st.spinner(
            "Generating contribution guide..."
        ):

            repo_state = (
                st.session_state.repo_state
            )

            contribution_input = {
                **repo_state,
                "selected_issue":
                issue_number
            }

            result = (
                contribution_graph.invoke(
                    contribution_input,
                    config={
                        "configurable": {
                            "thread_id":
                            st.session_state.thread_id
                        }
                    }
                )
            )

            st.session_state.contribution_result = (
                result
            )

        st.success(
            "Contribution guide generated."
        )


# --------------------------------------------------
# Contribution Guide
# --------------------------------------------------

result = st.session_state.contribution_result

if result:

    st.divider()

    st.header(
        "🛠 Contribution Guide"
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Issue Analysis",
            "File Mapping",
            "Implementation Plan",
            "PR Draft"
        ]
    )

    with tab1:

        st.markdown(
            result.get(
                "issue_analysis",
                "No analysis available."
            )
        )

    with tab2:

        with st.expander(
            "Relevant Files",
            expanded=True
        ):

            relevant_files = (
                result.get(
                    "relevant_files",
                    []
                )
            )

            if relevant_files:

                for file in relevant_files:

                    st.code(file)

        with st.expander(
            "File Mapping Reasoning",
            expanded=True
        ):

            st.markdown(
                result.get(
                    "file_mapping_analysis",
                    "No mapping analysis."
                )
            )

    with tab3:

        st.markdown(
            result.get(
                "implementation_plan",
                "No implementation plan."
            )
        )

    with tab4:

        pr_draft = result.get(
            "pr_draft",
            "No PR draft."
        )

        st.markdown(
            pr_draft
        )

        st.download_button(
            label="Download PR Draft",
            data=pr_draft,
            file_name="pr_draft.md",
            mime="text/markdown"
        )