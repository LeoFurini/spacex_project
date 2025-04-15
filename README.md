# 🚀 SpaceX Data Engineering Pipeline

This project is a fully containerized Data Engineering pipeline designed to extract, load, transform, and visualize data from the [SpaceX API](https://github.com/r-spacex/SpaceX-API). The pipeline leverages modern cloud-native tools and orchestration to automate the entire workflow daily, from raw API ingestion to business-ready dashboards.

Inspired by [vzucher/spacex](https://github.com/vzucher/spacex) with improvements and personal learning goals as a Data Engineer.

---

## 📌 Project Overview

**Architecture Summary:**

1. **Data Source:** [SpaceX API](https://github.com/r-spacex/SpaceX-API)
2. **Ingestion:** Python scripts extract API data and load to Google Cloud Storage (GCS)
3. **Storage:** Raw and staged data stored in GCS, then moved to BigQuery
4. **Transformation:** dbt (Data Build Tool) performs SQL-based transformations in BigQuery
5. **Orchestration:** Apache Airflow DAG manages all ETL tasks
6. **Containerization:** Docker + Docker Compose for development; built for `linux/amd64`
7. **Deployment:** Cloud Run Job triggered daily by Cloud Scheduler
8. **Secrets Management:** GCP Secret Manager handles credentials securely
9. **Visualization:** Power BI dashboards connected directly to BigQuery datasets

---

## 🧱 Tech Stack

| Layer            | Tool/Service                         |
|------------------|--------------------------------------|
| Orchestration    | Apache Airflow                       |
| Ingestion        | Python (Requests, Pandas)            |
| Storage          | Google Cloud Storage, BigQuery       |
| Transformation   | dbt (Core)                           |
| Scheduling       | Cloud Scheduler                      |
| Deployment       | Cloud Run (Job)                      |
| Secrets          | Google Secret Manager                |
| Containerization | Docker, Docker Compose               |
| Visualization    | Power BI (via BigQuery connector)    |

---

## 🛣️ Roadmap / Learning Goals
### 📦 Phase 1: Extract

- [ ] Create virtual environment and install dependencies (`Python`, `requests`, etc.)
- [ ] Connect to SpaceX API using Python
- [ ] Extract and parse API response into structured format (e.g., pandas DataFrame)
- [ ] Save raw JSON or CSV locally for testing
- [ ] Create Airflow DAG to schedule data extraction
- [ ] Containerize Python + Airflow using Docker and Docker Compose

---

### 🛢️ Phase 2: Load

- [ ] Configure AWS S3 bucket for raw data storage
- [ ] Upload raw extracted data to S3
- [ ] Set up PostgreSQL for staging data
- [ ] Load data from S3 into PostgreSQL (using Python or Airflow tasks)

---

### 🔄 Phase 3: Transformation

- [ ] Set up dbt Core project
- [ ] Create dbt models to transform staging data
- [ ] Configure and run dbt tests (unique, not null, accepted values, etc.)
- [ ] Generate dbt documentation site (`dbt docs generate`)
- [ ] Connect dbt to BigQuery as the final warehouse

---

### 📊 Phase 4: Visualization

- [ ] Connect Power BI to BigQuery
- [ ] Build dashboards and visualizations using transformed data
- [ ] Publish or export reports

---

### 🛠️ Final Steps

- [ ] Create `.env` file or secret manager setup for credentials
- [ ] Set up logging in Python and Airflow tasks
- [ ] Write a clear `README.md` for the GitHub project
- [ ] Add architecture diagram to `README.md`
- [ ] Create a Makefile or helper scripts for common commands
- [ ] Test full pipeline end-to-end
- [ ] Push code and documentation to GitHub

---

### ✅ Stretch Goals (Optional but Awesome)

- [ ] Add CI/CD with GitHub Actions (linting, tests, dbt docs)
- [ ] Add Great Expectations for extra data validation
- [ ] Set up alerting in Airflow (email/Slack on failure)
- [ ] Include sample queries and dashboard screenshots in the repo