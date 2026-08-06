# EduTrack Analytics Hub 🎓

> Centres for Academic Excellence 2026 | Challenge 3: Multi-Currency & Multi-Language Higher Education Portal

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Completed](https://img.shields.io/badge/Status-Completed-success.svg)]()

A single, safe web app for many students.  
It is made for keeping records, grading school work automatically, showing data in simple charts, and helping with local use in higher education.  
The app is built with security in mind, with routing, and support for different languages used in South Africa.  

---

## 🌍 Workflow & Features

### 1. Header, Clock & Language Selector
* Shows a live clock, date, theme switch, and a language selector for all 11 official South African languages plus SASL.

![Header Topbar](Screenshots/edutrack-header-topbar.png)
![Language Dropdown](Screenshots/edutrack-language-dropdown.jpg)

### 2. Academic Dashboard
* Brings together student tabs, showing marks, performance data, and module records in real time.

![Full Dashboard](Screenshots/edutrack-full-dashboard.png)

### 3. Transcript Export
* Makes official PDF transcripts with local headers and secure check codes.

![PDF Transcript](Screenshots/edutrack-pdf-transcript.jpg)

---

## 📋 System Setup

### Multi-Language Dictionary
The app maps school terms across South African languages:
* **Nguni:** isiZulu, isiXhosa, isiNdebele, siSwati  
* **Sotho-Tswana:** Sepedi, Sesotho, Setswana  
* **Tswa-Ronga & Venda:** Xitsonga, Tshivenda  
* **Other:** Afrikaans, English, SASL  

### Academic Rules
* **Average & Percent:** Works out marks and averages.  
* **Pass Rules:** Checks if marks meet pass levels.  
* **Secure Hashing:** Adds codes to transcripts to stop fake copies.  

---

## 🚀 Features

* Manage many student profiles, search by ID, and switch accounts.  
* Automatic grade calculations to avoid mistakes.  
* Make and download transcripts and reports.  
* Works well on low internet and small servers.  

---

## 🔒 Security

Built with security in mind:
* **Input Checks:** Stops unsafe data.  
* **Data Safety:** Keeps sessions and routes secure.  
* **Clear Control:** Splits app logic, templates, and storage.  

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)  
* **Frontend:** HTML5, CSS3  
* **Version Control:** Git & GitHub  

---

## 🏁 Getting Started

### Needs
* Python 3.10+  
* Git  

### Setup
```bash
git clone https://github.com/Tshepo-Letsoalo/edutrack-analytics-hub
cd edutrack-analytics-hub

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux

pip install flask
python app.py
