# CIRAS – Cybercrime Investigation & Record Analysis System

## Overview

CIRAS (Cybercrime Investigation & Record Analysis System) is an intelligence and investigation platform designed to assist cybercrime investigators in analyzing telecom records, subscriber activity, call detail records (CDR), IPDR data, IMEI relationships, movement patterns, and communication networks.

The platform transforms raw telecom datasets into actionable intelligence through automated analytics, network visualization, risk scoring, and interactive dashboards.

---

## Key Features

### CDR Analysis

* Call frequency analysis
* Incoming and outgoing call statistics
* Communication pattern identification
* Suspicious activity detection

### Network Intelligence

* Relationship graph generation
* Identification of key suspects and associates
* Communication cluster analysis
* Centrality and influence scoring

### IMEI Investigation

* Device usage tracking
* Multiple SIM detection
* Shared device identification
* IMEI relationship mapping

### Tower Analysis

* Cell tower movement tracking
* Location pattern analysis
* Tower hotspot detection
* Movement timeline visualization

### Individual Investigation Dashboard

* Contact analysis
* Hourly activity profiling
* Timeline reconstruction
* Digital footprint assessment

### Risk Scoring Engine

* Automated suspect prioritization
* Risk categorization
* Pattern-based scoring
* Investigation lead generation

---

## Dashboard Modules

| Module                   | Purpose                    |
| ------------------------ | -------------------------- |
| CDR Analysis             | Call pattern investigation |
| Network Graph            | Relationship mapping       |
| IMEI Analysis            | Device intelligence        |
| Tower Analysis           | Location intelligence      |
| Individual Investigation | Suspect profiling          |
| Risk Scoring             | Threat prioritization      |

---

## Technology Stack

### Backend

* Python 3.13

### Data Analysis

* Pandas
* NumPy

### Visualization

* Plotly
* Folium
* PyVis

### Dashboard

* Streamlit

### Network Analytics

* NetworkX

### Machine Learning

* Scikit-Learn

---

## Project Structure

```text
CIRAS/
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
│   └── investigation datasets
│
├── screenshots/
│   ├── dashboard.png
│   ├── network_graph.png
│   ├── tower_map.png
│   └── investigation_panel.png
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

## Use Cases

* Cybercrime Investigation
* Telecom Fraud Detection
* Digital Forensics
* Organized Crime Analysis
* Call Network Intelligence
* Suspect Relationship Mapping
* Telecom Data Analytics

---

## Future Enhancements

* Real CDR/IPDR ingestion
* AI-assisted investigation summaries
* Geospatial crime heatmaps
* Multi-case intelligence correlation
* OSINT integration
* Automated lead generation
* Advanced anomaly detection

---

## Disclaimer

This project is developed for educational, research, and investigative workflow demonstration purposes. All datasets included are synthetic and generated for testing and learning.
