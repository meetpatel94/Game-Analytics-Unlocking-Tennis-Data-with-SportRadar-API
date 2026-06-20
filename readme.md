# 🎾 Game Analytics: Unlocking Tennis Data with Sportradar API

## 📌 Project Overview

Game Analytics is a comprehensive Tennis Analytics Dashboard built using Python, Neon PostgreSQL, and Streamlit. The application extracts tennis competition, venue, complex, competitor, and ranking data from the Sportradar Tennis API, stores structured data in Neon PostgreSQL, and provides interactive visualizations, analytics, and insights through a modern web interface.

The project enables users to explore competition structures, analyze player rankings, investigate venues and complexes, and gain meaningful insights from tennis tournament data.

---

## 🚀 Features

### 📊 Interactive Dashboard

* Total Competitions
* Total Categories
* Total Venues
* Total Complexes
* Total Competitors
* Ranking Statistics
* Country-wise Analysis
* Competition Distribution Analysis

### 🏆 Competition Analytics

* Competition Overview
* Competition Type Analysis
* Gender-wise Distribution
* Parent-Child Competition Hierarchy
* Category-based Filtering

### 🎾 Competitor Rankings

* Top Ranked Players
* Ranking Movement Analysis
* Points Distribution
* Country-wise Competitor Analysis
* Search Competitors

### 🏟️ Venues & Complexes

* Venue Information Explorer
* Complex Details Viewer
* Country-wise Venue Distribution
* Timezone Analysis
* Complex-Venue Relationships

### 🔍 Advanced Filtering

* Filter by Category
* Filter by Competition Type
* Filter by Country
* Search Competitors
* Ranking Range Selection

### 📈 Data Visualization

* Interactive Charts
* KPI Cards
* Trend Analysis
* Distribution Graphs
* Comparative Analytics

---

## 🛠️ Technology Stack

### Frontend

* Streamlit
* HTML
* CSS
* Plotly
* Altair

### Backend

* Python

### Database

* Neon PostgreSQL

### Data Processing

* Pandas
* NumPy

### API Integration

* Sportradar Tennis API

---

## 📂 Project Structure

```text
Game-Analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── assets/
│   ├── images/
│
├── data/
│   ├── competitions.json
│   ├── complexes.json
│   └── double_competitors_rankings.json
│
├── database/
│   ├── db.py
│   └── test_connection.py
│
├── api_scripts/
│   ├── fetch_competitions.py
│   ├── fetch_complexes.py
│   ├── fetch_rankings.py
│   └── load_json_to_neon.py
│
├── streamlit_app/
│   ├── dashboard.py
│   ├── competitions.py
│   ├── venues.py
│   ├── rankings.py
│   └── compititions.py
│
├── components/
├── queries/
└── test_query.py
```

---

## 🗄️ Database Schema

### Categories Table

| Column        | Type         |
| ------------- | ------------ |
| category_id   | VARCHAR(50)  |
| category_name | VARCHAR(100) |

### Competitions Table

| Column           | Type         |
| ---------------- | ------------ |
| competition_id   | VARCHAR(50)  |
| competition_name | VARCHAR(100) |
| parent_id        | VARCHAR(50)  |
| type             | VARCHAR(20)  |
| gender           | VARCHAR(10)  |
| category_id      | VARCHAR(50)  |

### Complexes Table

| Column       | Type         |
| ------------ | ------------ |
| complex_id   | VARCHAR(50)  |
| complex_name | VARCHAR(100) |

### Venues Table

| Column       | Type         |
| ------------ | ------------ |
| venue_id     | VARCHAR(50)  |
| venue_name   | VARCHAR(100) |
| city_name    | VARCHAR(100) |
| country_name | VARCHAR(100) |
| country_code | CHAR(3)      |
| timezone     | VARCHAR(100) |
| complex_id   | VARCHAR(50)  |

### Competitors Table

| Column        | Type         |
| ------------- | ------------ |
| competitor_id | VARCHAR(50)  |
| name          | VARCHAR(100) |
| country       | VARCHAR(100) |
| country_code  | CHAR(3)      |
| abbreviation  | VARCHAR(10)  |

### Competitor Rankings Table

| Column              | Type        |
| ------------------- | ----------- |
| rank_id             | INT         |
| rank                | INT         |
| movement            | INT         |
| points              | INT         |
| competitions_played | INT         |
| competitor_id       | VARCHAR(50) |

---

## 🔗 API Endpoints Used

### Competitions API

```bash
https://api.sportradar.com/tennis/trial/v3/en/competitions.json
```

### Complexes API

```bash
https://api.sportradar.com/tennis/trial/v3/en/complexes.json
```

### Doubles Competitor Rankings API

```bash
https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/meetpatel94/Game-Analytics-Unlocking-Tennis-Data-with-Sportradar-API.git

cd Game-Analytics-Unlocking-Tennis-Data-with-Sportradar-API
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application URL

```text
http://localhost:8501
```

---

## 📈 Sample Insights

* Competition Distribution by Category
* Country-wise Venue Analysis
* Ranking Points Distribution
* Top Ranked Competitors
* Parent Competition Structure
* Venue Timezone Analytics
* Competition Type Analysis

---

## 🎯 Business Use Cases

* Event Exploration
* Competition Hierarchy Analysis
* Player Ranking Monitoring
* Sports Data Visualization
* Venue & Infrastructure Analysis
* Decision Support for Organizers
* Tennis Data Research

---

## 🔒 Error Handling

* API Rate Limit Handling
* Missing Data Validation
* Database Exception Handling
* User Input Validation
* Streamlit Session State Management

---

## 📚 Skills Demonstrated

* API Integration
* JSON Processing
* Database Design
* SQL Query Optimization
* Data Analytics
* Data Visualization
* Streamlit Development
* Dashboard Design
* Python Programming

---

## 👨‍💻 Author

### Meet Patel

B.E. Information Technology
M.E. Artificial Intelligence & Data Science

GitHub:
https://github.com/meetpatel94

Portfolio:
https://meetpatelportfolio.vercel.app

Email:
[meetpatel96645@gmail.com](mailto:meetpatel96645@gmail.com)

---

## ⭐ Acknowledgements

* Sportradar Tennis API
* Streamlit
* Neon PostgreSQL
* SQLAlchemy
* Pandas
* Plotly
* Python Community
