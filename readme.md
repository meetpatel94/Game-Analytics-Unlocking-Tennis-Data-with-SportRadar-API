# 🎾 Game Analytics: Unlocking Tennis Data with SportRadar API

## 📌 Project Overview

Game Analytics is a Streamlit-based data analytics application that explores and visualizes professional tennis data collected from the SportRadar API.

The application provides interactive dashboards for analyzing:

* Competitions
* Categories
* Complexes
* Venues
* Competitors
* Doubles Rankings

The project transforms raw API data into structured datasets and presents meaningful insights through modern visualizations and filters.

---

## 🚀 Features

### 🏆 Competition Analysis

* Explore tennis competitions and categories
* Analyze competition types and structures
* View parent and sub-competitions

### 🏟️ Complexes & Venues Explorer

* Browse sports complexes and venues
* Analyze venue distribution by country
* View timezone and location information

### 👥 Competitor Analytics

* Search competitors by name
* Country-wise competitor analysis
* Ranking and points insights

### 📈 Rankings Dashboard

* Top-ranked competitors
* Highest scoring competitors
* Rank movement analysis
* Competition participation statistics

### 🎨 Interactive Dashboard

* Dynamic filters
* KPI cards
* Charts and visualizations
* Responsive user interface

---

## 🛠️ Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### Data Processing

* Pandas
* NumPy

### Visualization

* Plotly
* Altair

### API Integration

* SportRadar Tennis API

### Database

* MySQL (Optional)

---

## 📂 Project Structure

```text
Game-Analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── category_details.json
│   ├── competition_details.json
│   ├── complexes_details.json
│   ├── venues_details.json
│   ├── competitors_details.json
│   └── competitor_rankings_details.json
│
├── components/
│
├── assets/
│
└── sql_queries.sql
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/Game-Analytics.git
cd Game-Analytics
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## 📊 Data Sources

The project uses data extracted from the SportRadar Tennis API.

Data Collections:

* Competitions
* Categories
* Complexes
* Venues
* Competitors
* Doubles Competitor Rankings

---

## 📸 Dashboard Highlights

* Competition Distribution Analysis
* Venue Analytics
* Country-wise Competitor Insights
* Rankings Explorer
* Interactive Filtering System
* KPI Overview Cards

---

## 📈 Business Use Cases

* Event Exploration
* Tournament Analysis
* Performance Insights
* Competition Tracking
* Sports Data Visualization
* Decision Support for Event Organizers

---

## 👨‍💻 Author

**Meet Patel**

M.E. Artificial Intelligence & Data Science
Gujarat Technological University (GTU)

GitHub: https://github.com/meetpatel94

---

## 📜 License

This project is developed for educational and analytical purposes.
