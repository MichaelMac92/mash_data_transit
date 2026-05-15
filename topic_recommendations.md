# 🚇 TransitGuard AI — Multi-Agent Transit Disruption Optimizer

> **The Pitch:** CredPath AI, but for transit. A multi-agent AI system that responds to service disruptions in real-time — predicting passenger impact, optimizing rerouting, and coaching transit operators through recovery.

---

## The CredPath → TransitGuard Parallel

What made CredPath special wasn't just the ML model — it was the **5-agent orchestrated architecture** where each agent had a distinct role, and the Streamlit UI walked users through a guided, multi-step experience. That same pattern translates *perfectly* to transit:

### Agent-by-Agent Mapping

| CredPath AI (Loan) | TransitGuard AI (Transit) | Role |
|---|---|---|
| 🤖 **Risk Agent** — XGBoost predicts default probability | 🤖 **Impact Agent** — ML predicts passenger displacement & delay severity | Core prediction engine |
| 📋 **Compliance Agent** — checks FICO floor, DTI limits | 📋 **Constraint Agent** — checks fleet capacity, driver availability, road accessibility | Feasibility validation |
| 💡 **Explanation Agent** — SHAP feature importance | 💡 **Explanation Agent** — explains *why* certain routes are affected most (network centrality, transfer dependency) | Interpretability |
| 🔄 **Negotiation Agent** — what-if scenarios (lower loan, improve FICO) | 🔄 **Scenario Agent** — what-if scenarios (partial closure vs. full, shuttle bridge vs. reroute) | Interactive exploration |
| 🎓 **Coach Agent** — actionable improvement advice | 🎓 **Recovery Agent** — recommends optimal restoration sequence & communicates ETAs to passengers | Actionable output |
| 🎯 **Orchestrator** — coordinates all agents | 🎯 **Orchestrator** — coordinates all agents per disruption event | Pipeline controller |

> [!TIP]
> Same architecture, same wow factor, but applied to a **completely different domain**. The judges will see a sophisticated, production-style AI system — not just a dashboard with a chart.

---

## How It Works — The User Flow

Just like CredPath had a 3-page guided flow (Tier Selection → Application Form → Decision Dashboard), TransitGuard has:

### Page 1 — 🗺️ Network Map & Disruption Selector
- Interactive map of a real Canadian city's transit network (TTC Toronto)
- User clicks a station/line segment to simulate a disruption
- Choose disruption type: full closure, partial service, delay, weather event
- Choose severity: minor (30 min), moderate (2 hrs), major (full day)

*→ Like CredPath's Tier Selection page, this is where the user sets up the scenario*

### Page 2 — 🤖 Agent Analysis Pipeline (The Magic)
- System shows agents working in sequence (with progress indicators):
  1. **Impact Agent** analyzes affected routes, estimates displaced passengers
  2. **Constraint Agent** checks available buses, depot proximity, road network
  3. **Scenario Agent** generates 3 response options ranked by cost-effectiveness
  4. **Recovery Agent** builds a phased restoration timeline
  5. **Explanation Agent** generates plain-English summary of reasoning

*→ Like CredPath's loading screen where all 5 agents processed the loan application*

### Page 3 — 📊 Response Dashboard (Multi-Tab, Just Like CredPath)

| Tab | Content | CredPath Equivalent |
|---|---|---|
| **Overview** | Decision summary: recommended response, estimated delay reduction, cost | Overview tab (Approved/Denied + probability) |
| **Impact Analysis** | Heatmap of affected stations, displaced passenger count by route | Risk breakdown |
| **Response Options** | 3 optimized response plans side-by-side (shuttle bridge, reroute, frequency boost) | What-If Simulator |
| **Explanation** | Why this response was chosen — network centrality analysis, SHAP-style feature importance | SHAP Explanation tab |
| **Timeline** | Phased restoration sequence with ETAs | Coaching tab |
| **Equity Check** | Does the response disproportionately affect underserved communities? | Compliance tab |

---

## Technical Architecture

```
┌─────────────────────────────────────────────────┐
│                  Streamlit UI                     │
│   Page 1: Map  →  Page 2: Agents  →  Page 3: Dashboard  │
└─────────────┬───────────────────────┬───────────┘
              │                       │
              ▼                       ▼
┌─────────────────────┐   ┌───────────────────────┐
│    Orchestrator      │   │   GTFS Data Layer      │
│  (coordinates all)   │   │  (routes, stops,       │
│                      │   │   schedules, shapes)   │
└──┬──┬──┬──┬──┬───────┘   └───────────────────────┘
   │  │  │  │  │
   ▼  ▼  ▼  ▼  ▼
┌────┐┌────┐┌────┐┌────┐┌────┐
│Imp.││Cons││Scen││Recv││Expl│
│Agnt││Agnt││Agnt││Agnt││Agnt│
└────┘└────┘└────┘└────┘└────┘
   │           │
   ▼           ▼
┌────────┐ ┌──────────┐
│ ML     │ │ Gurobi   │
│ Model  │ │ Optimizer│
│(XGBoost│ │ (MILP    │
│/ LSTM) │ │ routing) │
└────────┘ └──────────┘
```

### Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| **Frontend** | Streamlit + Folium/Plotly | Same stack as CredPath — you know this cold |
| **Agent Framework** | Python classes with Orchestrator pattern | Same pattern as CredPath's `agent_*.py` files |
| **ML Model** | XGBoost or Random Forest | Predict disruption impact severity |
| **Optimizer** | Gurobi (MILP) | Vehicle rerouting / shuttle bridge optimization — directly from OMIS 6000 |
| **Geospatial** | GeoPandas + Folium + Shapely | Transit network graph analysis |
| **Data** | GTFS + Synthetic ridership | 100% privacy compliant |

---

## Data Sources (All Open & Compliant)

| Dataset | Source | License |
|---|---|---|
| TTC GTFS feed | [City of Toronto Open Data](https://open.toronto.ca/) | Open Government Licence |
| OpenStreetMap road network | OSM | ODbL |
| Census demographics | Statistics Canada | Open Government Licence |
| Synthetic ridership | Team-generated from GTFS | N/A — explicitly allowed by rules |

---

## Why This Wins

### Scoring Breakdown

| Criterion (Weight) | TransitGuard Score | Why |
|---|---|---|
| **Innovation & Originality (20%)** | ⭐⭐⭐⭐⭐ | Multi-agent AI architecture for transit is novel and memorable |
| **Technical Merit (25%)** | ⭐⭐⭐⭐⭐ | ML + MILP optimization + agent orchestration = maximum technical depth |
| **Relevance to Transit (20%)** | ⭐⭐⭐⭐⭐ | Service disruption is the #1 operational pain point for transit agencies |
| **Interactive Tool Quality (20%)** | ⭐⭐⭐⭐⭐ | Map-based UI + multi-tab dashboard + live agent pipeline visualization |
| **Presentation & Communication (10%)** | ⭐⭐⭐⭐⭐ | Live demo: "Let's break Line 1 at Bloor-Yonge and watch the AI respond" |
| **Privacy & Ethics (5%)** | ⭐⭐⭐⭐⭐ | Synthetic data + public GTFS = zero PII risk |

### The Demo Moment 🎤
During the 10-minute live presentation, you literally **click on Bloor-Yonge station on the map**, simulate a closure, and the audience watches the 5 agents activate in sequence and produce a full response plan. That's a *mic-drop* demo — same energy as CredPath's loan application flow but with a map lighting up in real-time.

---

## What Each Team Member Could Own

| Role | Responsibility | Key Skills |
|---|---|---|
| **You (Michael)** | Orchestrator + Agent architecture + Gurobi optimizer | Your MILP/optimization expertise + CredPath experience |
| **Friend #1** | ML pipeline (Impact Agent) + synthetic data generation | Data science / ML modeling |
| **Friend #2** | Frontend (Streamlit + Folium map) + Explanation/Equity agents | UI/UX + data visualization |

---

## Timeline to May 30 Deadline

| Week | Milestone |
|---|---|
| **Apr 14–20** | Finalize topic, register, download TTC GTFS, build network graph |
| **Apr 21–27** | Agent skeleton (all 5 agents + orchestrator), synthetic data generation |
| **Apr 28 – May 4** | ML model training, Gurobi optimizer for shuttle routing |
| **May 5–11** | Streamlit UI: map page, agent pipeline visualization, dashboard tabs |
| **May 12–18** | Integration testing, equity analysis, polish |
| **May 19–25** | Technical report writing, video recording, bug fixes |
| **May 26–30** | Final submission, deploy to cloud (Render/Railway) |

> [!IMPORTANT]
> You have **~6.5 weeks** until the May 30 deadline. This is tight but very doable given you've already built CredPath's full agent architecture once. The transit version reuses the same structural patterns.
