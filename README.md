# 🚀 Open Source Onboarding Agent

> An AI-powered multi-agent assistant that helps developers understand unfamiliar GitHub repositories and make their first open-source contribution faster.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

Contributing to an open-source project can be difficult for first-time contributors. Developers often spend hours understanding the repository structure, finding a suitable issue, identifying the relevant files, and planning an implementation.

**Open Source Onboarding Agent** automates this onboarding process using a multi-agent AI workflow built with LangGraph.

Given a GitHub repository, the system:

* Analyzes the repository
* Finds beginner-friendly issues
* Explains selected issues
* Identifies relevant source files
* Generates an implementation plan
* Drafts a professional Pull Request description

---

## ✨ Features

* Repository analysis
* README understanding
* Repository structure analysis
* Beginner-friendly issue discovery
* AI-powered issue explanation
* Relevant file mapping
* Implementation planning
* Professional PR draft generation
* Multi-agent workflow using LangGraph
* Interactive Streamlit interface

---

## 🏗 Architecture

```text
                     User
                       │
                       ▼
                Streamlit Frontend
                       │
                       ▼
             Repository Analysis Graph
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
     GitHub Repository      README Analysis
             │
             ▼
      Beginner Issue Discovery
             │
             ▼
      User Selects an Issue
             │
             ▼
          Contribution Graph
             │
      ┌──────┼──────────────┐
      ▼      ▼              ▼
 Issue Agent File Mapper Planner Agent
             │
             ▼
       PR Generator Agent
             │
             ▼
      Contribution Guide
```

---

## 🤖 Multi-Agent Workflow

### Repository Agent

Responsible for:

* Fetching repository metadata
* Reading the README
* Understanding repository structure
* Finding beginner-friendly issues

---

### Issue Analysis Agent

Responsible for:

* Understanding the selected issue
* Explaining the problem
* Identifying required skills
* Suggesting an approach

---

### File Mapper Agent

Responsible for:

* Inspecting repository structure
* Reading candidate source files
* Identifying relevant files

---

### Implementation Planner Agent

Responsible for:

* Creating a step-by-step implementation plan
* Suggesting required code changes
* Identifying testing requirements

---

### PR Generator Agent

Responsible for generating:

* Branch Name
* Commit Message
* Pull Request Title
* Professional Pull Request Description

---

## 🛠 Tech Stack

### AI & Agent Framework

* Python
* LangGraph
* LangChain
* LangChain Core

### Large Language Model

* Hugging Face Inference Endpoints
* Qwen2.5-72B-Instruct

### Frontend

* Streamlit

### Backend

* Python

### APIs

* GitHub REST API
* Hugging Face API

### State Management

* LangGraph StateGraph
* Streamlit Session State

### Database

* SQLite (Checkpointing)

---

## 📂 Project Structure

```text
open_source_onboarding_agent/

├── agent/
│   ├── nodes/
│   ├── repository_graph.py
│   └── contribution_graph.py
│
├── config/
│
├── models/
│
├── prompts/
│
├── tools/
│
├── database/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/open-source-onboarding-agent.git

cd open-source-onboarding-agent
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
HF_TOKEN=YOUR_HUGGINGFACE_TOKEN

GITHUB_TOKEN=YOUR_GITHUB_TOKEN
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---
