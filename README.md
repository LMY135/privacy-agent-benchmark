# Privacy-Agent-Benchmark

## Overview

Privacy-Agent-Benchmark is a training-free framework for simulating realistic users in multi-turn conversations with AI assistants.

The project aims to generate natural user–AI conversations in which users have consistent identities, behavioral characteristics, and private personal information. Instead of explicitly scripting when personal information should be disclosed, the simulated user maintains a private memory bank and decides naturally what information becomes relevant as the conversation develops.

The generated conversations can be used to study realistic user behavior and personal-information disclosure in multi-turn AI interactions.

## User Simulation

Our simulated users are constructed from three main components:

```text
Persona
  │
  ├── Identity Profile
  └── Behavior Profile
  │
  ▼
Private Memory Bank
  │
  ▼
Task Scenario
  │
  ▼
Simulated User Agent
  │
  │ Multi-turn Interaction
  ▼
Assistant Agent
```

### Persona

Each user is initialized from a structured persona describing identity and behavioral characteristics, including demographic background, language, professional domain, personality traits, and interaction tendencies.

### Private Memory

Each persona is associated with synthetic private memories covering five categories:

- Personal Identity
- Financial
- Health & Medical
- Beliefs & Politics
- Relationships & Work

These memories represent information known by the simulated user. They are not directly inserted into the dialogue. Instead, the user agent can disclose relevant memories naturally when they become useful during the conversation.

### Scenario

Each conversation begins with a task-oriented scenario containing a context and a broad user goal.

We currently consider five task families:

- Advice Seeking
- Decision Support
- Information Seeking
- Communication Assistance
- Planning & Problem Solving

The scenario specifies the user's initial situation rather than defining a complete conversation trajectory, allowing the interaction to evolve dynamically.

### Multi-Turn Conversation

For each scenario, a persona-conditioned user agent interacts with a general-purpose assistant.

The user agent receives:

```text
Identity Profile
+ Behavior Profile
+ Private Memories
+ Current Scenario
+ Conversation History
```

The user may ask questions, provide additional context, disagree with suggestions, clarify previous statements, reveal relevant personal information, or terminate the conversation when its goal has been sufficiently resolved.

The framework is fully **training-free** and does not require fine-tuning the underlying language model.

---

## Environment Setup

This project uses `uv` for Python dependency management.

### 1. Install uv

```bash
pip install uv
```

### 2. Install dependencies

From the project root:

```bash
uv sync
```

### 3. Configure the LLM

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then configure your LLM endpoint in `.env`:

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your_model_name
```

### 4. Run the Pipeline

Generate private memories:

```bash
uv run python scripts/generate_memories.py --all-personas --count 7
```

Generate scenarios:

```bash
uv run python scripts/generate_scenarios.py --all-personas
```

Generate conversations:

```bash
uv run python scripts/generate_conversations.py --persona 0001 --num-conversations 1 --max-turns 10
```

---

## Environment File

The repository contains:

```text
.env.example
```

with placeholder configuration:

```env
LLM_API_KEY=
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=
```

Create your own `.env` locally and **do not commit API keys or other credentials**.