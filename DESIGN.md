# Design Note — AI Support & TAM Assistant

## 1. Production Failure Modes

### 1. Incorrect LLM classification or hallucinated recommendations

An LLM may incorrectly classify an ambiguous ticket, assign an inappropriate urgency, or invent a knowledge-base recommendation. This is especially risky for P1/P2 tickets because incorrect routing can delay incident response.

The system mitigates this through structured output, constrained prompts, knowledge-base retrieval, and deterministic validation. Task 1 also separates retrieved evidence from the LLM's reasoning rather than allowing the model to invent documentation references. The evaluation harness tests ambiguous and known-issue scenarios as regression cases.

### 2. Incomplete or inconsistent customer data

Real support data can contain missing account records, sparse ticket history, conflicting fields, or inconsistent company/product information. The supplied dataset already demonstrates these cases: some ticket account IDs have no matching account and some joined records contain inconsistent metadata.

The system uses `account_id` as the join key, handles missing accounts explicitly, and avoids silently modifying source data. Risk detection also distinguishes account-level evidence from ticket-level evidence. Missing information is surfaced to the TAM rather than being replaced with assumptions.

### 3. External API failures or model availability issues

LLM APIs can experience rate limits, outages, latency spikes, or model/version changes. The development process exposed this directly when the free-tier API quota was exhausted during evaluation.

The evaluation harness was therefore designed so regression tests can run against versioned output fixtures without making live API calls. In production, I would additionally use retries with exponential backoff, request timeouts, model fallback, monitoring, and clear degraded-mode responses.

---

## 2. Latency vs Quality

The main quality decision was to use retrieval before generation rather than sending the entire knowledge base to the LLM. Knowledge-base documents are chunked into sections and retrieved using semantic similarity, reducing the amount of context sent to the model while keeping relevant troubleshooting information available.

For Task 2, the pipeline first performs deterministic account/ticket retrieval and risk detection, then uses the LLM only for synthesis. This adds an intermediate processing step but improves grounding and consistency.

If latency became the hard constraint, I would reduce the number of retrieved chunks, cache frequently accessed embeddings and account summaries, use a smaller/faster model for straightforward classifications, and reserve the larger model only for ambiguous cases.

---

## 3. Data Sensitivity

Support tickets and account summaries may contain personally identifiable or commercially sensitive information. The system therefore uses only the supplied dataset and does not perform external web searches or introduce third-party customer data.

API credentials are loaded through environment variables rather than source code, with `.env.example` containing only placeholder variable names. In a production deployment, sensitive fields should be redacted before external LLM calls where possible, API access should be restricted through a secure secret manager, and logging should avoid storing raw ticket bodies or customer information.

A production implementation should also apply data retention policies, access controls, encryption in transit and at rest, and provider-level controls appropriate for customer data.

---

## 4. Scaling to 10× Volume

The current mock dataset contains 500 tickets and 50 accounts. At 10× volume, the first pressure point would be retrieval and repeated LLM inference rather than the basic Python data structures.

The current in-memory loading approach is appropriate for the assignment but would not be the ideal production architecture. I would move ticket and account data into a database or search index, maintain a persistent vector index for the knowledge base, and process ticket ingestion asynchronously.

For higher throughput, embeddings should be generated once and cached, frequently requested account summaries should be cached, and independent requests should be processed concurrently with rate limiting. LLM calls should also have bounded retries and observability around latency, token usage, failures, and classification quality.

The evaluation harness should run continuously against a versioned regression suite so model or prompt changes can be detected before deployment.