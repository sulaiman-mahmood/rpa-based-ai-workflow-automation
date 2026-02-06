# RPA-Based AI Workflow Automation (Streamlit + Power Automate Desktop)

## Overview
This repository contains an **AI-assisted workflow automation prototype** designed to reduce manual effort and improve decision-making in routine approval processes. The system combines **machine learning**, a **Streamlit-based user interface**, and **Power Automate Desktop (RPA)** to automatically triage straightforward cases while escalating ambiguous or high-risk cases for human review.

The project was built as a **production-minded prototype** using synthetic but realistic data, with full audit logging and measurable performance indicators.

---

## Problem Statement
Across functions such as **Buying, Merchandising, and Finance**, routine approvals often involve:
- high manual effort,
- slow triage cycles,
- limited transparency and auditability.

Many cases are straightforward and could be automated, but teams still need:
- confidence thresholds,
- human-in-the-loop controls,
- and reliable audit logs.

**Objective:**  
Automate simple cases, surface “interesting” or uncertain cases for humans, and log every decision for audit and analysis.

---

## End-to-End Architecture
The system follows a clear, modular flow:

1. **Model layer** – ML classifier predicts approve / reject / manual review  
2. **UI layer** – Streamlit app mimicking an internal business portal  
3. **Automation layer** – Power Automate Desktop orchestrates browser actions  
4. **Logging layer** – append-only Excel logs for traceability and KPI reporting  


---

## Methodology & Delivery
A **lightweight agile / iterative approach** was used:

- stakeholder requirements → prototype → feedback → refinement
- clear definition of done:
  - automated end-to-end run
  - exported audit file
  - demonstrable KPIs

Although built with synthetic data, the system is designed to be directly extensible to real operational datasets.

---

## Data & Modelling
### Data
- Synthetic but realistic records (no production data)
- Labels: `Approve`, `Reject`, `Manual Review`
- Designed to be replaceable with historical approval data

### Model
- **Random Forest Classifier**
- ~2,000 rows
- Features include:
  - transaction amount
  - customer / vendor score
  - urgency indicators

**Why Random Forest**
- handles non-linear relationships
- robust with mixed feature scales
- explainable via feature importance (important for trust)

### Risk Handling
- confidence-based gating:
  - low confidence (e.g. 40–60%) → **Manual Review**
- avoids over-automation in uncertain cases

---

## Streamlit Application
The Streamlit UI provides:
- a **dashboard** view for running the model in bulk
- a **decision mode** showing individual cases
- clear visual separation between automated vs manual outcomes

The UI is designed to mimic an internal business portal and prioritises stability and clarity over visual complexity.

---

## Power Automate Desktop (RPA)
Power Automate Desktop is used for:
- browser-based orchestration
- looping through decisions
- interacting with UI elements
- exporting structured audit logs

Key design considerations:
- stable selectors
- explicit waits and fallback logic
- rerun-safe execution
- append-only logging

---

## Logging, KPIs & Auditability
All decisions are logged to **Excel** to keep the prototype:
- portable
- transparent
- Power BI–ready

Example metrics:
- % automated vs manual
- average processing time
- confidence distribution
- error / retry counts

---

## My Role & Responsibilities
I designed and implemented the **entire prototype end to end**, including:
- synthetic data generation
- ML pipeline (training, evaluation, confidence thresholds)
- Streamlit multi-page UI
- Power Automate Desktop flows
- acceptance criteria and success metrics
- runbooks, documentation, and presentation assets

The system was built with **production thinking**, despite being a prototype.

---

## Challenges & How They Were Solved
- **UI instability** → fixed element IDs and controlled rerenders  
- **Lack of real data** → realistic synthetic generation + clear replacement plan  
- **RPA timing issues** → explicit waits and fallback interaction logic  
- **Model uncertainty** → confidence-based manual review gating  
- **Mixed technical audiences** → diagrams for operations, metrics for data teams  

---

## Tools & Technology
- Python: `pandas`, `scikit-learn`, `joblib`
- ML: Random Forest classifier
- UI: Streamlit (multi-page)
- Automation: Power Automate Desktop
- Logging: Excel (append-only, Power BI–ready)
- Optional / future: Azure hosting, CI/CD, Power BI dashboards

---

## Demo Flow
1. Run model from dashboard and export results  
2. Open decision mode for individual cases  
3. Trigger Power Automate Desktop  
4. Observe counters and logs updating  
5. Review final Excel audit output and summary metrics  

---

## Roadmap / Next Steps
- Replace synthetic data with real approval sources
- Expand feature set (vendor risk, fraud signals, PO matching, seasonality)
- Deploy model as a service
- Add CI/CD
- Power BI dashboards for ops
- Drift monitoring for data teams

---

## Positioning
This project demonstrates:
- applied AI decision systems
- RPA orchestration in operational workflows
- human-in-the-loop safety design
- end-to-end system ownership

It is presented as a **portfolio and research-style artifact**, suitable for Global Talent endorsement and further academic or industrial development.

