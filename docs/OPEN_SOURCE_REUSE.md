# Open Source Reuse Strategy & Architectural Inspirations

ShramAI adopts a disciplined, modular reuse strategy. Rather than wholesale cloning or monolithic adoption, ShramAI extracts vetted architectural design patterns from top-tier open-source projects:

---

### 1. Indian Labour Law RAG Architecture
- **Reference**: `algsoch/indianlabour`
- **Reused Patterns**:
  - Legal knowledge ingestion pipelines for Indian statutory texts.
  - Granular chunking strategies optimized for legislative acts, rules, and schedules.
  - Source citation mechanics attributing findings to specific sections and gazette notifications.
- **Original Contribution in ShramAI**:
  - Replaced generic chat queries with establishment-focused document evidence cross-examination.
  - Structured evidence-to-provision linking rather than free-form conversational legal summaries.

---

### 2. Agentic RAG Architecture
- **Reference**: `dkleptsov/agentic-rag-assistant`
- **Reused Patterns**:
  - LangGraph state machine patterns for conditional routing between specialized agents.
  - Streaming agent telemetry and observable intermediate steps.
  - Structured Pydantic contracts passed across agent transitions.
- **Original Contribution in ShramAI**:
  - Purpose-built multi-agent team: Document Agent, Compliance Agent, Anomaly Agent, Risk Agent, and Report Agent.
  - Strict guardrails preventing LLMs from deciding statutory violations or inventing risk scores.

---

### 3. Document Intelligence & OCR Pipeline
- **Reference**: `PaddleOCR` & `FastAPI OCR Service` (`gabriele-mastrapasqua/fastapi-ocr`)
- **Reused Patterns**:
  - Direct digital PDF text extraction first with confidence verification before invoking OCR.
  - Fallback layout analysis and tabular extraction for scanned registers.
- **Original Contribution in ShramAI**:
  - Document classifier tailored to Indian statutory labour formats (Form B Wage Register, Form A Employee Register, Attendance Muster Rolls).
  - Canonical data normalization preserving page and bounding provenance.

---

### 4. Deterministic Rule Engine
- **Reference**: `santalvarez/python-rule-engine`
- **Reused Patterns**:
  - Separation of legal rules from application code using structured JSON configurations.
  - Deterministic evaluation of condition trees yielding boolean outcomes (PASS, FAIL, INSUFFICIENT EVIDENCE).
- **Original Contribution in ShramAI**:
  - Rule definitions mapped directly to statutory mandates under the Code on Wages 2019 and OSH&WC Code 2020.
