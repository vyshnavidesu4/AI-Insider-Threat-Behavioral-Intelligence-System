# Insider Threat Behavioral Intelligence System

A Security Operations Center (SOC) Behavioral Intelligence & Insider Threat Detection System specifically scoped for a mid-size regional banking institution.

---

## Regional Bank Domain Architecture

The system is configured around 6 critical regional banking departments with tailored access heuristics:

1. **Treasury Operations** (Critical Risk Tier): Monitors high-value SWIFT/Fedwire transmissions, dual-control bypass attempts, and off-hour settlement queues.
2. **Wealth Management** (High Risk Tier): Monitors client portfolio scraping, High-Net-Worth (HNW) KYC dossier exports, and advisor pre-resignation data staging.
3. **IT Operations** (High Risk Tier): Monitors core banking DBA privilege escalation, off-schedule service principal creation, and credential access.
4. **Loan Origination** (Medium Risk Tier): Monitors commercial underwriter bulk credit file / SSN access and loan approval velocity.
5. **Retail Banking** (Low Risk Tier): Monitors branch head teller overrides and customer account lookups.
6. **Compliance & Risk** (Low Risk Tier): Monitors audit log access and regulatory reporting queries.

---

## 5-Factor Risk Weighting Model

The `risk_scores` table explicitly persists the 5 core behavioral threat pillars matching the 35/25/20/10/10 weighting specification:

| Factor | Weight | Description |
|---|:---:|---|
| **`behavioral_anomalies_score`** | **35%** | Statistical volume deviations, USB transfers, outbound data spikes vs. peer baseline |
| **`privilege_misuse_score`** | **25%** | Unauthorized permission elevation, administrative tooling misuse, DBA access |
| **`data_access_violations_score`** | **20%** | Non-departmental asset probing, wire approval share access, bulk PII queries |
| **`access_pattern_deviations_score`** | **10%** | After-hours access, abnormal IP/VPN geo-origin, concurrent device hopping |
| **`historical_security_events_score`** | **10%** | Prior confirmed alerts, DLP trigger history, security policy violations |
| **`composite_score`** | **100%** | Final weighted composite score (0–100 scale) |

`risk_factors` (`jsonb`) stores the structured human-readable explanation and top risk drivers for SOC analyst triage.

---

## Factual `event_type` Model

In compliance with forensic audit standards, raw telemetry `event_type` categories remain neutral and factual:
- `LOGON`
- `LOGOFF`
- `FILE_ACCESS`
- `USB_TRANSFER`
- `EMAIL_SENT`
- `DB_QUERY`
- `WIRE_TRANSFER_INITIATED`
- `PRIVILEGE_CHANGE`

*Note: Temporal indicators (e.g. after-hours) are derived dynamically from event timestamps; exfiltration/anomaly judgments belong exclusively in `is_anomalous` and dedicated anomaly detection tables.*

---

## Tech Stack & Project Structure

```
├── docker-compose.yml              # Multi-container orchestration (postgres, backend, frontend)
├── .env.example                    # Environment variable template
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/0001_initial_schema.py
│   └── app/
│       ├── main.py                 # FastAPI application initialization & CORS
│       ├── core/
│       │   ├── config.py           # Pydantic Settings & environment variables
│       │   ├── database.py         # SQLAlchemy engine, session maker, Base model
│       │   ├── security.py         # Password hashing (bcrypt) & JWT token encoding
│       │   └── dependencies.py     # DB injection, get_current_user, require_role
│       ├── models/                 # SQLAlchemy ORM models
│       │   ├── user.py             # SOC Users (analyst, manager, admin)
│       │   ├── department.py       # 6 Bank Departments
│       │   ├── employee.py         # Bank Staff entities & clearance tiers
│       │   ├── activity_event.py   # Raw factual audit events
│       │   ├── behavior_baseline.py# Historical statistical metrics
│       │   ├── risk_score.py       # 5 explicit components + composite score
│       │   ├── alert.py            # Triage alert lifecycle
│       │   └── investigation.py    # Case management dossier
│       ├── schemas/                # Pydantic validation & response models
│       ├── services/               # AuthService & UserService business logic
│       └── routers/                # API route endpoints (/auth, /users, /health)
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.ts          # Custom SOC dark theme (deep slate, tabular mono, zero neon)
    └── src/
        ├── index.css               # SOC styling tokens & monospace font rules
        ├── api/                    # Axios client with JWT auto-refresh interceptor
        ├── hooks/                  # useAuth hook powered by React Query
        ├── types/                  # TypeScript interfaces matching backend models
        ├── components/
        │   ├── common/             # DenseTable, Badge, RiskScoreBadge
        │   └── layout/             # Header, Sidebar, AppLayout
        └── pages/                  # SOC Overview Dashboard, Alerts, Employees, Cases, Login
```

---

## Running the System

### 1. With Docker Compose (Recommended)

```bash
docker-compose up --build
```
- **Frontend SOC Console**: `http://localhost:5173`
- **Backend API & Swagger Docs**: `http://localhost:8000/docs`
- **PostgreSQL**: `localhost:5432`

### 2. Running Locally for Development

**Backend**:
```bash
cd backend
python -m venv .venv
# On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

---

## Authentication & Role-Based Access Control (RBAC)

- **JWT Tokens**: Emits access tokens (60 min) and refresh tokens (7 days).
- **FastAPI Dependencies**:
  - `get_current_user`: Validates token signature and fetches active user.
  - `require_role([UserRole.ADMIN])`: Restricts administrative mutation endpoints.
  - `require_manager`: Authorizes case assignment and user listing.
  - `require_analyst`: Authorizes alert triage and telemetry analysis.
