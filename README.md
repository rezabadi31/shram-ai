# ShramAI

## AI-Powered Labour Compliance & Inspection Intelligence

> **Transform labour documents into evidence-backed compliance insights, risk intelligence, and inspection priorities.**

ShramAI is an AI-powered labour compliance and inspection intelligence platform designed to help **employers identify potential compliance issues** and help **labour inspectors prioritize establishments using evidence-backed risk intelligence**.

The platform combines **Document AI, OCR, Agentic AI, Retrieval-Augmented Generation (RAG), compliance rules, cross-document anomaly detection, explainable machine learning, and human-in-the-loop review** into a single workflow.

### 🔗 Live Application

https://shramai.netlify.app/

The application provides separate role-based experiences for:

* 👨‍💼 **Employer**
* 👮 **Inspector**

The authenticated role determines which dashboard and functionality the user can access.


# 1. Problem

Labour compliance involves large volumes of documents and records, including:

* Wage registers
* Attendance records
* Employee registers
* Payroll documents
* Compliance returns
* Safety records
* Appointment and employment documents
* Scanned PDFs
* Images and other supporting records

Manually reviewing these documents against multiple labour requirements is time-consuming.

A second challenge is that important issues may not exist inside a single document.

For example:

| Source              | Employee Count |
| ------------------- | -------------: |
| Employee Register   |             62 |
| Attendance Register |             61 |
| Wage Register       |             57 |
| Payroll             |             59 |

A document-by-document system may treat each file independently.

ShramAI instead attempts to identify the **cross-document inconsistency** and surface it as a potential anomaly requiring verification.

---

# 2. Proposed Solution

ShramAI transforms employer records through an intelligence pipeline:

```text
Documents
    ↓
Document AI / OCR
    ↓
Structured Information
    ↓
Agentic AI
    ↓
Compliance Analysis
    ↓
Legal RAG
    ↓
Cross-Document Anomaly Detection
    ↓
Risk Intelligence
    ↓
Explainable Findings
    ↓
Inspector Prioritization
    ↓
Human Review
```

The objective is to move from:

> **Document-heavy and reactive inspection**

toward:

> **Proactive, evidence-backed and explainable compliance intelligence.**

---

# 3. Core Users

## 👨‍💼 Employer

The employer-facing experience focuses on:

* Compliance visibility
* Document management
* Potential issues
* Missing records
* Corrective actions
* Compliance self-assessment
* AI-assisted guidance

The goal is **prevention and voluntary compliance**.

---

## 👮 Inspector

The inspector-facing experience focuses on:

* Establishment risk ranking
* Inspection prioritization
* Compliance findings
* Cross-document anomalies
* Evidence
* Previous inspection information
* Risk explanations
* AI-generated inspection briefs
* Human verification

The goal is **evidence-backed inspection decision support**.

---

# 4. Role-Based Access

ShramAI separates employer and inspector workflows.

```text
                         LOGIN
                           │
                    Role Verification
                     ┌─────┴─────┐
                     ↓           ↓
                 EMPLOYER     INSPECTOR
                     ↓           ↓
              Employer UI    Inspector UI
```

### Employer

An employer can access:

* Own establishment information
* Uploaded documents
* Compliance findings
* Corrective actions
* Employer dashboard
* Compliance assistant

An employer cannot access inspector-only functionality or other establishments.

### Inspector

An inspector can access:

* Inspection queue
* Establishment risk ranking
* Compliance findings
* Cross-document anomalies
* Evidence
* Inspection intelligence
* Risk explanations

This separation is enforced at the application/backend authorization layer rather than relying only on hiding frontend elements.

---

# 5. Document Intelligence

ShramAI is designed to process different types of labour documentation.

### Supported document categories

| Category   | Examples                     |
| ---------- | ---------------------------- |
| Wage       | Wage registers               |
| Attendance | Attendance records           |
| Employee   | Employee registers           |
| Payroll    | Payroll records              |
| Safety     | Safety documentation         |
| Employment | Appointment/contract records |
| Returns    | Labour/compliance returns    |
| General    | Supporting documents         |

### Processing workflow

```text
Upload
  ↓
File Validation
  ↓
Text Extraction
  ↓
OCR / Vision Processing
  ↓
Document Classification
  ↓
Table & Field Extraction
  ↓
Structured Data
  ↓
Validation
```

The structured information becomes the foundation for subsequent compliance and anomaly analysis.

---

# 6. Agentic AI Architecture

Instead of using a single general-purpose AI workflow, ShramAI is designed around specialized agents coordinated through an orchestrator.

```text
                    ORCHESTRATOR
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
   Document Agent   Compliance Agent   Anomaly Agent
                         │
                         ↓
                    Risk Agent
                         │
                         ↓
                    Report Agent
```

## Document Agent

Responsible for:

* Document understanding
* Information extraction
* Field validation
* Document classification

## Compliance Agent

Responsible for:

* Identifying applicable requirements
* Retrieving relevant legal information
* Generating compliance findings
* Connecting findings with evidence

## Anomaly Agent

Responsible for:

* Comparing documents
* Detecting inconsistencies
* Finding missing records
* Identifying duplicate or conflicting information

## Risk Agent

Responsible for:

* Combining risk indicators
* Generating establishment-level risk predictions
* Supporting inspection prioritization

## Report Agent

Responsible for:

* Summarizing findings
* Producing evidence-backed explanations
* Preparing inspection/compliance briefs

---

# 7. Legal Intelligence with RAG

A major component of ShramAI is its legal intelligence layer.

A general-purpose LLM should not be expected to independently determine labour compliance requirements.

ShramAI therefore uses **Retrieval-Augmented Generation** to ground AI responses in an authoritative knowledge base.

### Potential knowledge sources

* Labour Codes
* Central Rules
* Government notifications
* Ministry FAQs
* Compliance handbooks
* Official guidelines

### RAG pipeline

```text
Authoritative Sources
        ↓
Document Processing
        ↓
Chunking
        ↓
Embedding Generation
        ↓
Vector Database
        ↓
Semantic Retrieval
        ↓
Relevant Legal Evidence
        ↓
AI Compliance Analysis
```

### Example

```text
Detected Evidence
       ↓
Missing wage information
       ↓
Legal retrieval
       ↓
Relevant requirement
       ↓
Compliance finding
       ↓
Evidence + source + recommendation
```

This improves traceability and reduces dependence on unsupported model-generated answers.

---

# 8. Cross-Document Intelligence

One of ShramAI's major differentiating capabilities is **cross-document reasoning**.

Instead of evaluating each document independently, the system can compare related records.

### Example

```text
Employee Register → 62
Attendance        → 61
Wage Register     → 57
Payroll           → 59
```

Possible output:

> 🔴 Potential cross-document inconsistency detected.

### Potential anomaly categories

* Employee-count mismatch
* Missing employees
* Duplicate employees
* Missing fields
* Incorrect values
* Calculation inconsistencies
* Conflicting employee information
* Expired documents
* Missing records

The system should treat these findings as **potential issues requiring verification**, rather than automatically declaring a legal violation.

---

# 9. Risk Intelligence

ShramAI incorporates a risk-based inspection philosophy inspired by approaches such as **MIRA Albania**, while adapting the concept to the Indian labour-compliance context.

The risk model can consider:

* Compliance findings
* Severity
* Missing documents
* Cross-document anomalies
* Previous inspection findings
* Unresolved findings
* Establishment characteristics
* Historical outcomes

```text
Compliance Findings
        +
Missing Documents
        +
Anomalies
        +
Historical Information
        +
Establishment Features
        ↓
   ML Risk Model
        ↓
   Risk Score
```

Example:

```text
        87 / 100
        HIGH RISK
```

### Inspection prioritization

| Risk      | Suggested Action       |
| --------- | ---------------------- |
| 🔴 High   | Priority inspection    |
| 🟠 Medium | Review / clarification |
| 🟢 Low    | Routine monitoring     |

The risk score should be produced by the ML model rather than being arbitrarily selected by an LLM.

---

# 10. Explainable Risk

ShramAI is designed to make risk predictions understandable.

SHAP or similar explainability methods can identify important contributing features.

Example:

```text
Risk Score: 87

Risk Contributors

Missing wage records          +18
Cross-document mismatch       +14
Unresolved finding            +12
Missing safety document        +9
```

This allows an inspector to understand:

> **Why was this establishment prioritized?**

rather than receiving an unexplained black-box prediction.

---

# 11. Generative AI Explanation Layer

Generative AI acts primarily as an **explanation and interaction layer**.

An inspector could ask:

> "Why is this establishment high risk?"

The system can produce a structured explanation based on available evidence.

Example:

```text
Risk Score: 87/100 — High

Key contributors:
• Multiple high-severity findings
• Cross-document inconsistencies
• Missing records
• Previous unresolved findings

Recommended action:
Prioritize the establishment for inspection and
verify the flagged records.
```

Important principle:

> **ML predicts the risk; GenAI explains the risk.**

---

# 12. Employer Dashboard

The employer dashboard is designed around voluntary compliance.

### Dashboard capabilities

* Compliance score
* Document status
* Missing documents
* Potential issues
* Risk areas
* Corrective actions
* AI compliance assistant
* Uploaded records

### Employer workflow

```text
Employer Login
      ↓
Authentication
      ↓
Employer Dashboard
      ↓
Upload Documents
      ↓
Compliance Analysis
      ↓
Review Findings
      ↓
Corrective Action
```

---

# 13. Inspector Dashboard

The inspector dashboard focuses on inspection intelligence.

### Dashboard capabilities

* Establishment ranking
* Risk score
* High-risk establishments
* Inspection queue
* Compliance findings
* Cross-document anomalies
* Evidence
* Previous inspection history
* Explainability
* AI inspection brief

### Inspector workflow

```text
Inspector Login
       ↓
Authentication
       ↓
Inspector Dashboard
       ↓
Risk Ranking
       ↓
Evidence Review
       ↓
Inspection Prioritization
       ↓
Human Inspector Decision
```

---

# 14. Human-in-the-Loop

ShramAI is designed as a decision-support system, not an autonomous enforcement system.

```text
AI Analysis
     ↓
Risk Prediction
     ↓
Evidence
     ↓
Inspector Review
     ↓
Actual Inspection
     ↓
Actual Findings
     ↓
Feedback
```

Human inspectors remain responsible for final inspection and enforcement decisions.

---

# 15. Closed-Loop Learning

Inspection outcomes can eventually be used to evaluate and improve the risk model.

```text
AI Risk Prediction
        ↓
Inspector Inspection
        ↓
Actual Findings
        ↓
Feedback Database
        ↓
Model Evaluation
        ↓
Retraining / Improvement
        ↓
Future Predictions
```

A portion of inspections can also be retained for random or unbiased selection to reduce over-reliance on automated prioritization.

---

# 16. System Architecture

```text
                         SHRAMAI
                            │
                            ▼
                    React Frontend
                   TypeScript / Vite
                            │
                            ▼
                       FastAPI API
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
       Authentication   Document AI    Agentic AI
             │              │              │
             ↓              ↓              ↓
           RBAC            OCR             RAG
                                            │
                                            ↓
                                  Compliance Intelligence
                                            │
                              ┌─────────────┼─────────────┐
                              ↓             ↓             ↓
                         Rule Engine    Anomaly       Risk Model
                                        Detection          │
                                                           ↓
                                                         SHAP
                                                           │
                                                           ↓
                                                Risk Intelligence
                                                           │
                                      ┌────────────────────┴──────────────┐
                                      ↓                                   ↓
                               Employer Portal                    Inspector Portal
```

---

# 17. Technology Stack

## Frontend

* React
* TypeScript
* Vite
* Responsive UI

## Backend

* Python
* FastAPI

## Database

* PostgreSQL
* pgvector

## AI / ML

* OCR / Vision AI
* Large Language Models
* Agentic AI
* Retrieval-Augmented Generation
* Embeddings
* Machine Learning
* XGBoost
* SHAP

## Authentication

* JWT
* Role-Based Access Control

## Deployment

* Netlify — Frontend
* Render — Backend deployment option
* PostgreSQL — Database

---

# 18. Deployment

The current ShramAI web application is deployed on **Netlify**.

### Current frontend

```text
Internet
   ↓
Netlify
   ↓
React / Vite Application
```

For a production-style full-stack deployment, the architecture can be extended to:

```text
                  NETLIFY
               React Frontend
                     │
                   HTTPS
                     │
                     ▼
                  RENDER
              FastAPI Backend
                     │
                     ▼
              PostgreSQL
               + pgvector
                     │
                     ▼
                 AI / RAG
```

The frontend should communicate with the backend through an environment-configured API base URL.

Sensitive credentials and API keys must remain server-side.

---

# 19. Security & Privacy

ShramAI follows security-by-design principles.

### Authentication

JWT-based authentication can be used for secure sessions.

### Authorization

Role-based access ensures:

```text
EMPLOYER ≠ INSPECTOR
```

### Data isolation

Employers should only access their authorized establishment data.

### Secrets

Sensitive credentials should be stored using environment variables rather than committed to GitHub.

### API Security

* HTTPS
* CORS configuration
* Backend authorization
* Input validation
* Authentication middleware

### Privacy

Real worker information should not be used in the prototype without appropriate authorization and governance.

Synthetic or privacy-safe data should be used for demonstration and testing.

---

# 20. Accessibility & Inclusion

ShramAI can support inclusive access through:

* Multilingual interfaces
* Hindi
* English
* Regional Indian languages
* Responsive layouts
* Accessible typography
* High-contrast interfaces
* Keyboard navigation
* Screen-reader-compatible controls
* Voice interaction

Future low-tech interfaces can include:

* IVR
* SMS
* Voice-based compliance assistance

---

# 21. Data Strategy

A practical prototype does not require a massive proprietary dataset.

ShramAI can use three complementary data sources.

## Legal Knowledge Dataset

Authoritative legal sources:

* Labour Codes
* Rules
* Notifications
* FAQs
* Guidelines

## Synthetic Document Dataset

Privacy-safe examples of:

* Wage registers
* Attendance
* Payroll
* Employee records
* Safety records
* Returns

Both compliant and non-compliant examples can be generated.

## Risk Dataset

Synthetic establishment profiles containing:

* Compliance indicators
* Inspection history
* Anomalies
* Establishment characteristics
* Historical outcomes

---

# 22. Evaluation

ShramAI should be evaluated independently at multiple levels.

### Document Intelligence

* OCR accuracy
* Field extraction accuracy
* Table extraction accuracy

### RAG

* Retrieval precision
* Retrieval recall
* Citation correctness
* Grounded response rate

### Anomaly Detection

* Precision
* Recall
* F1-score

### Risk Prediction

* ROC-AUC
* Precision
* Recall
* F1-score
* Calibration
* False-positive rate

### User Experience

* Task completion time
* Usability
* Dashboard comprehension
* User satisfaction

---

# 23. Innovation

ShramAI's innovation comes from combining multiple intelligence layers.

```text
             SHRAMAI
                │
    ┌───────────┼───────────┐
    ↓           ↓           ↓
Document AI   Legal RAG   Agentic AI
    │           │           │
    └───────────┼───────────┘
                ↓
       Cross-Document AI
                ↓
       ML Risk Prediction
                ↓
        SHAP Explainability
                ↓
        Human-in-the-Loop
```

### Key differentiators

**1. Document-to-Risk Pipeline**

Documents are transformed into establishment-level intelligence.

**2. Legal Grounding**

Compliance reasoning can be grounded in retrieved legal sources.

**3. Cross-Document Reasoning**

The system looks for inconsistencies across records.

**4. Predictive Inspection**

Risk intelligence can support inspection prioritization.

**5. Explainable AI**

Risk predictions can be accompanied by contributing factors.

**6. Human Governance**

AI assists authorized personnel rather than replacing them.

---

# 24. Existing Work & Extensibility

ShramAI is designed using established technologies and open-source components where appropriate.

Potential building blocks include:

* OCR frameworks
* Vector databases
* Agent orchestration frameworks
* PostgreSQL
* FastAPI
* React
* XGBoost
* SHAP

The project-specific contribution is the combination of these components into a labour-compliance workflow consisting of:

```text
Document
   ↓
Evidence
   ↓
Compliance
   ↓
Anomaly
   ↓
Risk
   ↓
Inspection Intelligence
```

Open-source components should always be used according to their respective licenses.

---

# 25. Project Structure

A modular implementation can follow:

```text
ShramAI/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── models/
│   │   ├── services/
│   │   ├── agents/
│   │   ├── rag/
│   │   ├── compliance/
│   │   ├── anomaly/
│   │   └── risk/
│   └── requirements.txt
│
├── data/
├── ml/
├── docs/
├── tests/
│
├── .gitignore
└── README.md
```

---

# 26. Roadmap

```text
CURRENT
Working Prototype
      ↓
Expanded Synthetic Dataset
      ↓
RAG & Model Evaluation
      ↓
Pilot Testing
      ↓
Potential Shram Suvidha Integration
      ↓
State-Level Intelligence
      ↓
National-Scale Labour Intelligence
```

### Future capabilities

* Multilingual AI assistant
* Voice/IVR
* SMS notifications
* Mobile application
* GIS-based inspection intelligence
* Real-time regulatory updates
* Advanced predictive models
* Government API integrations
* Sector-specific compliance models
* Privacy-preserving machine learning

---

# 27. Limitations

ShramAI is currently a prototype and has several areas requiring further validation.

### Synthetic Data

Real-world deployment requires appropriately authorized datasets.

### OCR Errors

Poor-quality scans may reduce extraction accuracy.

### Legal Interpretation

AI-generated findings should not replace authorized legal or inspection decisions.

### Model Bias

Risk models require continuous evaluation for false positives, false negatives and potential bias.

### LLM Reliability

Generative AI can produce incorrect information if not properly grounded.

### Mitigation

```text
RAG
 +
Rules
 +
Evidence
 +
Confidence
 +
Human Review
```

---

# 28. Positioning

ShramAI is:

* Inspired by risk-based inspection approaches such as MIRA Albania.
* Designed for potential integration with Indian labour digital ecosystems.
* An AI-assisted decision-support platform.
* Focused on explainability and evidence.

ShramAI is **not**:

* An official replacement for government labour systems.
* An autonomous enforcement authority.
* A substitute for authorized labour inspectors.
* A claim of official integration with Shram Suvidha.

Final enforcement decisions remain with authorized human authorities.

---

# 29. Impact

### Employer Impact

* Faster compliance review
* Better visibility into potential issues
* Corrective-action guidance
* Improved voluntary compliance

### Inspector Impact

* Risk-based prioritization
* Faster document analysis
* Cross-document anomaly visibility
* Evidence-backed inspection preparation
* Explainable risk intelligence

### System-Level Impact

Potential future applications include:

* Sector-level compliance trends
* Geographic risk patterns
* Policy intelligence
* Emerging violation detection
* Data-driven inspection planning

# 30. Disclaimer

ShramAI is a prototype and research-oriented implementation intended to demonstrate the feasibility of AI-assisted labour compliance and inspection intelligence.

The system does not constitute legal advice, does not automatically establish legal violations, and should not replace decisions made by authorized government officials or labour inspectors.

