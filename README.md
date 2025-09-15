# Streamlit SQL Library App  

<p align="center">  
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python"/>  
  <img src="https://img.shields.io/badge/SQL-MySQL-orange?logo=mysql" alt="MySQL"/>  
  <img src="https://img.shields.io/badge/SQLite-lightgrey?logo=sqlite" alt="SQLite"/>  
  <img src="https://img.shields.io/badge/Framework-Streamlit-red?logo=streamlit" alt="Streamlit"/>  
  <img src="https://img.shields.io/badge/ORM-SQLAlchemy-green?logo=python" alt="SQLAlchemy"/>  
  <img src="https://img.shields.io/badge/Deployment-Streamlit%20Cloud-brightgreen?logo=streamlit" alt="Deployment"/>  
</p>  

---

## 🚀 Overview  
A **full-stack data application** for managing borrowed books.  
This project demonstrates my ability to:  
- design relational databases,  
- integrate SQL with Python,  
- and build interactive apps with Streamlit.  

👉 [Live Demo (SQLite version)](https://lianes-library-demo.streamlit.app/)  

---

## 📸 Preview  

<p align="center">  
  <img src="https://github.com/victoria-vasilieva/streamlit-library-app/blob/main/screenshot/Bildschirmfoto%202025-09-07%20um%2023.13.46.png" alt="App Screenshot" width="600"/>  
</p>  

---

## 🔑 Key Features  
- **CRUD Operations** – add, view, edit, and delete book records.  
- **Database Design** – ERDs, normalization, relationships, constraints.  
- **SQL + Python Integration** – via SQLAlchemy.  
- **Streamlit UI** – intuitive interface for non-technical users.  
- **Deployment Ready** – MySQL locally, SQLite for demo hosting.  

---

## 🛠️ Tech Stack  
- **Backend:** MySQL (local), SQLite (demo), SQLAlchemy  
- **Frontend:** Streamlit  
- **Language:** Python 3  
- **Deployment:** Streamlit Community Cloud  

---

## 👩‍💻 Contributors  
- **Carlos Montefusco (@camontefusco)**  
- **Olaf Bulas (@Cebulva)**  
- **Azumi Muhammed (@azumimuhammed)**  

---

# 📘 Technical Documentation  

## 1. Introduction  
This project was inspired by a real-world use case: helping a friend track borrowed books.  
We designed a relational database, connected it with Python, and built a Streamlit UI to manage it.  

---

## 2. Features (Detailed)  
- CRUD support with MySQL backend  
- Database design with normalization & ERDs  
- SQLAlchemy integration  
- Streamlit front-end  
- SQLite-powered demo for quick deployment  

---



## 3. Getting Started

### 3.1 Prerequisites
- A web browser
- Local MySQL instance
- Python 3.x
- Required libraries:
```bash
streamlit
sqlalchemy
mysql-connector-python
```

### 3.2 Installation
```bash
# Clone repository
git clone https://github.com/your-username/streamlit-library-app.git

# Navigate into project directory
cd streamlit-library-app

# Install dependencies
pip install -r requirements.txt
```



## 4. Project Workflow
### 4.1 Database Design & Implementation

Entities: books, borrowers.

Normalization and constraints applied.

Database created with `Lianes_Library.sql`.

### 4.2 SQL–Python Integration

- The file [`library_connection.py`](library_connection.py) establishes a secure connection to the database using SQLAlchemy.

### 4.3 Streamlit Application & Deployment

- **Local version:** connects to MySQL  
- **Cloud demo version:** uses SQLite for portability



## 5. Project Components

- [`Lianes_Library.sql`](Lianes_Library.sql) – SQL script to create and populate the database
- [`Login.py`](Login.py) – Main Streamlit application code
- [Live demo on Streamlit Cloud](https://lianes-library-demo.streamlit.app/) – Browser-accessible version of the app



## 6. Usage

### Database Setup
1. Start your local MySQL instance.
2. Run the SQL script [`Lianes_Library.sql`](Lianes_Library.sql) in MySQL Workbench or a terminal.
3. Create and populate the database schema `lianes_library`.

### Run the App
```bash
streamlit run Login.py
```

Browser will prompt for MySQL password to connect.

