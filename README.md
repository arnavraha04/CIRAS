# CIRAS – Cybercrime Investigation & Record Analysis System

## Overview

CIRAS (Cybercrime Investigation & Record Analysis System) is an intelligence-driven telecom investigation platform designed to assist cybercrime investigators in analysing:

* Call Detail Records (CDR)
* Internet Protocol Detail Records (IPDR)
* IMEI Relationships
* Communication Networks
* Tower Movement Patterns
* Digital Behavioural Indicators

The platform converts raw telecom datasets into actionable intelligence through automated analytics, visualization, risk scoring and investigation dashboards.

---

## Core Capabilities

### CDR Analysis

* Call frequency analysis
* Associate identification
* Communication pattern detection
* Incoming / outgoing call statistics
* Timeline reconstruction

### IPDR Analysis

* Website activity analysis
* Application usage profiling
* VPN usage detection
* Internet session tracking
* Digital behaviour assessment

### Network Intelligence

* Communication graph generation
* Cluster identification
* Relationship mapping
* Influence analysis
* Central node detection

### IMEI Investigation

* Shared device detection
* Multiple SIM analysis
* Device movement tracking
* IMEI relationship mapping

### Tower Analysis

* Tower movement reconstruction
* Location intelligence
* Movement timelines
* Hotspot identification

### Risk Scoring

* Automated suspect prioritization
* Pattern-based risk assessment
* Lead generation
* Investigation ranking

---

## Dashboard Modules

| Module                   | Purpose                         |
| ------------------------ | ------------------------------- |
| CDR Analysis             | Telecom communication analysis  |
| IPDR Analysis            | Internet activity investigation |
| Network Graph            | Associate mapping               |
| IMEI Analysis            | Device intelligence             |
| Tower Analysis           | Movement intelligence           |
| Individual Investigation | Suspect profiling               |
| Risk Scoring             | Threat prioritization           |

---

## Technology Stack

### Backend

* Python 3.13

### Dashboard

* Streamlit

### Analytics

* Pandas
* NumPy

### Network Analysis

* NetworkX

### Visualisation

* Plotly
* Folium
* PyVis

### Machine Learning

* Scikit-Learn

---

## Project Structure

```text
CIRAS/
│
├── analysis/
│   ├── cdr_analysis.py
│   ├── network_graph.py
│   ├── imei_analysis.py
│   ├── tower_analysis.py
│   ├── risk_scorer.py
│   └── individual_investigation.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── mock_cdr.csv
│   ├── mock_ipdr.csv
│   ├── mock_complaints.csv
│   └── sample_data/
│
├── docs/
│
├── lib/
│
└── README.md
```

---

## Installation

```bash
git clone https://github.com/arnavraha04/CIRAS.git

cd CIRAS

pip install -r requirements.txt

streamlit run dashboard/app.py
```

---

## Sample Validation Dataset

CIRAS includes a dedicated validation dataset.

Location:

```text
data/sample_data/
```

Files:

```text
sample_cdr.csv
sample_ipdr.csv
expected_findings.md
```

Purpose:

* Validate associate detection
* Validate communication clustering
* Validate IMEI analysis
* Validate tower movement analysis
* Validate IPDR/CDR correlation
* Validate VPN detection

---

## Expected Validation Results

Running CIRAS against the sample dataset should identify:

### Primary Associate

9811122233

### Communication Cluster

4 interconnected numbers

### IMEI Correlation

351796540645876

### Tower Movement Pattern

TWR_DEL_001
→ TWR_DEL_002
→ TWR_MUM_001
→ TWR_MUM_002

### Timeline Correlation

IPDR activity immediately preceding voice communication events.

### VPN Usage

9988776655

Detailed findings are documented in:

```text
data/sample_data/expected_findings.md
```

---

## Use Cases

* Cybercrime Investigation
* Telecom Fraud Detection
* Digital Forensics
* Organised Crime Analysis
* Telecom Intelligence
* Suspect Profiling
* Relationship Mapping
* Behavioural Analysis

---

## Future Enhancements

* Real-time CDR ingestion
* Real-time IPDR ingestion
* AI-assisted investigation summaries
* Geospatial crime heatmaps
* OSINT integration
* Cross-case intelligence correlation
* Advanced anomaly detection

---

## Disclaimer

All datasets included in this repository are synthetic and generated solely for educational, research and demonstration purposes.

No real subscriber information, telecom records or personal data are included.
