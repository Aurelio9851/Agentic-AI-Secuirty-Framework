# Agentic Code Analysis System

> A lightweight multi-agent AI framework built **from scratch** in Python, featuring planning, orchestration, shared memory, semantic code retrieval (RAG), and autonomous tool usage.

---

## Overview

This project implements a complete **multi-agent architecture** without relying on frameworks such as LangGraph, CrewAI or AutoGen.

The goal is to understand how modern AI agent systems work internally by implementing every component manually:

- Agent orchestration
- Planning
- Re-planning
- Shared memory
- Tool calling (ReAct)
- Retrieval-Augmented Generation (RAG)
- Semantic code search
- Multi-agent collaboration

Instead of hiding the logic behind a framework, every decision is explicit and customizable.

---

# Features

- Multi-Agent Architecture
- Planner Agent
- Supervisor / Orchestrator
- ReAct Agents
- Shared Memory
- Semantic RAG over codebases
- Tool Calling
- Autonomous Re-planning
- Repository Exploration
- Security Analysis
- Code Review
- Automatic Report Generation

---

# Architecture

```text
                             USER
                               │
                               ▼
                     +------------------+
                     |    Supervisor    |
                     +------------------+
                               │
                               ▼
                     +------------------+
                     | Planner + Replan |
                     +------------------+
                               │
      ----------------------------------------------------------
      │                      │                │                 │
      ▼                      ▼                ▼                 ▼
 SearchAgent            CodeAgent      SecurityAgent      ReporterAgent
      │                      │                │                 │
      └──────────────────────┴────────────────┴─────────────────┘
                             │
                             ▼
                     Shared Memory
                             │
                             ▼
                          Tool Layer
```

---

# Tool Layer

```text
                        +--------------------+
                        |       Tools        |
                        +--------------------+
                        | list_files()       |
                        | grep_file()        |
                        | read_file()        |
                        | security_scan()    |
                        | run_terminal()     |
                        | search_codebase()  |
                        +----------+---------+
                                   │
                  ┌────────────────┴──────────────┐
                  ▼                               ▼
            File System                    Semantic RAG
```

# Agents

## Planner Agent

Responsible for:

- understanding the user request
- creating an execution plan
- selecting the best agent
- triggering re-planning whenever necessary

---

## Supervisor Agent

Coordinates the execution.

Responsibilities:

- executes the current plan
- dispatches tasks
- collects outputs
- triggers Planner for re-planning
- stops execution when the task is complete

---

## Search Agent

Repository explorer.

Tools:

- list_files()
- grep_file()

Responsibilities:

- discover project structure
- locate relevant files
- collect repository information

---

## Code Agent

Software engineering specialist.

Tools:

- read_file()
- search_codebase()

Responsibilities:

- explain code
- identify logic bugs
- understand architectures
- suggest improvements

---

## Security Agent

Security specialist.

Tools:

- security_scan()
- read_file()
- search_codebase()

Responsibilities:

- OWASP analysis
- authentication review
- secret detection
- insecure configuration analysis
- code security review

---

## Reporter Agent

Produces the final report.

Responsibilities:

- aggregate agent outputs
- summarize findings
- generate recommendations

---

# Shared Memory

Agents communicate through a shared memory.

```text
                 Shared Memory

        observations
        search_results
        files_found
        reports
        planner_notes
```

Every agent can:

- read previous observations
- write new findings
- reuse existing knowledge

This prevents duplicated work and enables collaborative reasoning.

---

# Planning Workflow

```text
User Request

↓

Planner

↓

Execution Plan

↓

Supervisor

↓

Agents

↓

Shared Memory Updated

↓

Need More Work?

├── Yes → Re-plan
└── No  → Finish
```

---

# Project Structure

```text
project/

│

├── agents/

│   ├── base_agent.py

│   ├── planner_agent.py

│   ├── supervisor_agent.py

│   ├── search_agent.py

│   ├── code_agent.py

│   ├── security_agent.py

│   └── reporter_agent.py

│

├── tools/

│   ├── file_tools.py

│   ├── code_tools.py

│   ├── security_tools.py

│   └── rag_tools.py

│

├── rag/

│   ├── rag.py

│   ├── gemini_embedding.py

│   └── vector_store.py

│

├── memory/

│   └── shared_memory.py

│

└── main.py
```

---

# Current Capabilities

- Multi-agent collaboration
- Autonomous planning
- Dynamic re-planning
- Shared memory
- ReAct reasoning
- Tool calling
- Semantic repository search
- Code explanation
- Security analysis
- Report generation

---
