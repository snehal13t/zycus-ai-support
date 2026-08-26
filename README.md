# Zycus AI Support Assistant

Production-oriented AI tooling for Technical Support and Technical Account Management teams.

The project implements:

- Intelligent support ticket triage
- Knowledge-base retrieval (RAG)
- TAM account health summarisation
- Deterministic churn/escalation signal detection
- Offline evaluation and regression testing
- Structured output validation

The solution uses only the synthetic dataset provided for the assessment.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │   Support Ticket    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Ticket Triage     │
                    │  Gemini + RAG       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        Classification     KB Match       Response Draft
        Product/Area       + Evidence      + Team Routing


                    ┌─────────────────────┐
                    │     Account ID      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Account + 90d       │
                    │ Ticket Retrieval    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Deterministic Risk  │
                    │ Detection           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ TAM Brief Generator │
                    │ Gemini + Structured │
                    │ Output Validation   │
                    └─────────────────────┘Perfect. ✅ The entry point works.

We now need to make the README **submission-ready** and then do the final clean-install/security checks.

### Step 60 — Create the README

Open `README.md` and paste this:

````markdown
# Zycus AI Support Assistant

Production-oriented AI tooling for Technical Support and Technical Account Management teams.

The project implements:

- Intelligent support ticket triage
- Knowledge-base retrieval (RAG)
- TAM account health summarisation
- Deterministic churn/escalation signal detection
- Offline evaluation and regression testing
- Structured output validation

The solution uses only the synthetic dataset provided for the assessment.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │   Support Ticket    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Ticket Triage     │
                    │  Gemini + RAG       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        Classification     KB Match       Response Draft
        Product/Area       + Evidence      + Team Routing


                    ┌─────────────────────┐
                    │     Account ID      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Account + 90d       │
                    │ Ticket Retrieval    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Deterministic Risk  │
                    │ Detection           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ TAM Brief Generator │
                    │ Gemini + Structured │
                    │ Output Validation   │
                    └─────────────────────┘
````

---

## Project Structure

```text
.
├── data/
│   ├── tickets.json
│   └── accounts.json
├── knowledge-base/
│   ├── products/
│   ├── troubleshooting/
│   ├── billing/
│   └── onboarding/
├── prompts/
│   ├── triage_v1.txt
│   └── tam_v1.txt
├── src/
│   ├── retrieval/
│   ├── triage/
│   ├── tam/
│   └── evaluation/
├── evaluation/
│   └── fixtures/
├── tests/
├── DESIGN.md
├── eval_report.json
├── main.py
├── requirements.txt
└── .env.example
```

---

## Setup

Python 3.11+ is recommended.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the API key:

```bash
cp .env.example .env
```

Add the Gemini API key to `.env`:

```text
GEMINI_API_KEY=your_api_key_here
```


---

## Single Entry Point

Run:

```bash
python main.py
```

Available commands:

```bash
python main.py triage
python main.py tam
python main.py demo
```

`triage` runs Task 1.

`tam` runs Task 2.

`demo` runs both.

The `demo` command requires a configured Gemini API key.

---

# Task 1 — Intelligent Ticket Triage

The triage pipeline accepts a raw support ticket and produces:

* Product area
* Issue category
* Urgency tier (P1–P4)
* Classification reasoning
* Urgency reasoning
* Knowledge-base match
* Relevant KB reference
* Recommended responder team
* Draft first-response message

### Retrieval

The knowledge base is parsed into section-level chunks while preserving:

* Source document
* Section heading
* Document type

Semantic retrieval uses TF-IDF similarity to identify relevant knowledge-base content before generation.

### Example

```python
from src.triage.agent import TriageAgent

agent = TriageAgent()

result = agent.triage(
    subject="New users cannot authenticate via SSO",
    body="Existing users can log in but new joiners cannot."
)

print(result)
```

---

# Task 2 — TAM Account Health Summariser

The TAM pipeline accepts an account ID and combines:

* Account summary
* Last 90 days of ticket history
* Deterministic escalation/churn signals
* LLM synthesis

The output contains exactly three sections:

1. Executive summary
2. Open risks & flagged issues
3. Recommended talking points

Ticket-based risk flags include direct ticket evidence and quotes when applicable.

The system also handles:

* Missing account records
* Sparse ticket history
* Missing NPS
* Conflicting account/ticket metadata

The account ID is used as the authoritative join key.

---

# Task 3 — Evaluation Harness

The evaluation framework contains five test cases for each task.

### Task 1

Tests include:

* Feature request classification
* SSO known-issue retrieval
* Performance prioritisation
* Billing retrieval
* Ambiguous/adversarial ticket

### Task 2

Tests include:

* At-risk account escalation
* Sparse ticket history
* Healthy account
* New customer
* Incomplete-data adversarial case

Each test reports:

* Pass/fail
* Quality score from 0–1
* Checks passed
* Checks attempted

The evaluation uses versioned fixtures so regression tests can run without making live LLM API calls.

Run:

```bash
python -m tests.test_evaluation
```

Current evaluation result:

```text
TASK1: 5/5 passed | Average score: 1.0
TASK2: 5/5 passed | Average score: 1.0
```

The complete report is stored in:

```text
eval_report.json
```

---

# Determinism

Task 2 uses:

* Temperature `0`
* Deterministic risk detection before generation
* Structured JSON output
* Post-generation validation
* Versioned prompt templates
* Offline regression fixtures

This reduces variation and makes model/prompt regressions easier to detect.

---

# Prompt Versioning

Prompts are stored separately from application code:

```text
prompts/triage_v1.txt
prompts/tam_v1.txt
```

Version identifiers make future prompt changes traceable and allow regression comparisons between prompt versions.

---

# Data Handling

All data used by this project comes exclusively from the supplied synthetic dataset.

No live customer data, web scraping, or external knowledge sources are used.

API credentials are loaded through environment variables and `.env` is excluded from Git.

See [`DESIGN.md`](DESIGN.md) for the full discussion of failure modes, latency/quality trade-offs, data sensitivity, and scaling.

---

# Evaluation Report

The generated evaluation report is included at:

```text
eval_report.json
```

The evaluation fixtures used for offline regression testing are stored under:

```text
evaluation/fixtures/
```

---

# Limitations and Production Considerations

This assessment implementation uses local JSON files and an in-memory retrieval layer because the supplied dataset is small.

For production scale, the system could move ticket/account storage to a database, maintain a persistent vector/search index, cache embeddings and account summaries, introduce asynchronous processing, and add API observability, retries, rate limiting, and model fallback.

The design intentionally separates deterministic business logic from probabilistic LLM generation so high-risk decisions can be validated independently.

---

# Design Note

See:

```text
DESIGN.md
```

for the required production design analysis.

```
