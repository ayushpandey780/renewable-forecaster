<div align="center">

# ☀️ Endsley Solar Forecaster

![Python](https://img.shields.io/badge/Python-3.14+-blue?logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange?logo=xgboost)
![Accuracy](https://img.shields.io/badge/Accuracy_(R²)-99.8%25-brightgreen)
![Pipeline](https://img.shields.io/badge/Data-No--API_Scraping-blueviolet)

> **An end-to-end Machine Learning pipeline predicting solar farm power output via real-time, autonomously scraped meteorological telemetry.**

</div>

---

## 📖 Project Overview

Grid operators need precise generation forecasts to balance the power grid. However, relying on commercial weather APIs introduces latency, strict rate limits, and high operational costs. 

The **Endsley Solar Forecaster** solves this by establishing a **"No-API" data pipeline**. It autonomously scrapes unstructured meteorological data from the web, processes it into structured time-series features, and feeds it into a highly accurate XGBoost regression model to predict real-time solar megawatt capacity.

---

## ✨ Core Features

*   **🕵️‍♂️ Autonomous Data Ingestion:** Fault-tolerant web scrapers utilizing `trafilatura` and Regular Expressions to extract live environmental data (humidity, wind speed, pressure) directly from public meteorological bulletins.
*   **🧬 Physics-Based Data Synthesis:** Engineered an 8,700+ row historical dataset utilizing orbital mechanics, cloud attenuation formulas, and temperature coefficients to simulate realistic solar array outputs.
*   **🧠 Extreme Gradient Boosting (AI):** A tuned XGBoost Regressor capable of mapping complex, non-linear weather patterns to energy output with a **99.8% R² Accuracy**.
*   **🛡️ Resilient Architecture:** Built-in `try/except` guardrails for missing data, ensuring the pipeline never crashes during anomalous weather events or missing sensor telemetry.

---

## 🏗️ System Architecture

```mermaid
graph TD;
    A[Public Web / Meteorological Data] -->|No-API Scraper| B(trafilatura Text Extraction);
    B -->|RegEx Parsing| C{Data Engineering Pipeline};
    C -->|Store| D[(Raw Data Lake / CSV)];
    C -->|Clean & Format| E[Feature Engineering];
    D --> E;
    E --> F((XGBoost Predictive Engine));
    F -->|Real-Time Inference| G[Predicted MW Output];
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#bfb,stroke:#333,stroke-width:2px
'''


📂 Repository Structure
'''

endsley-solar-forecaster/
├── data/
│   ├── raw/                  # Scraped live telemetry (CSV)
│   └── processed/            # Synthesized historical physics data
├── models/
│   └── solar_forecaster.json # Compiled XGBoost model weights
├── notebooks/
│   ├── 01_weather_ingestion_test.ipynb
│   ├── 02_dataset_generation.ipynb
│   └── 03_model_training.ipynb
├── scrapers/
│   └── weather_scraper.py    # Production ingestion script
├── predict.py                # Core execution & inference engine
├── requirements.txt          # Python dependencies
└── README.md

🚀 Quick Start / Installation
1. Clone the repository and navigate to the directory:

git clone [https://github.com/YOUR-USERNAME/renewable-forecaster.git](https://github.com/YOUR-USERNAME/renewable-forecaster.git)
cd renewable-forecaster

2. Create a virtual environment and install dependencies:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Run the live prediction engine:
python predict.py

☕ Enterprise Integration (Future Scope)

While the core machine learning model and data pipelines are built in Python to leverage the rich data science ecosystem, the system is designed for massive scale.
The compiled .json model weights can easily be served via a lightweight REST API (FastAPI) and consumed by a Java Spring Boot enterprise backend. This architecture allows legacy grid control systems and Java-based microservices to seamlessly query the AI engine for real-time grid balancing and dispatch decisions.
