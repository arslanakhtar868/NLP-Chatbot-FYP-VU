# 🤖 AI Based Chatbot for Educational Institutes  
### Final Year Project (FYP)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-red?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql)
![Dialogflow](https://img.shields.io/badge/Dialogflow-NLP-green?logo=googlecloud)
![Status](https://img.shields.io/badge/Project-FYP-success)

---

## 📌 Introduction

This repository contains the source code and documentation for the **AI Based Chatbot for Schools and Training Institutes**, developed as a **Final Year Project (FYP)**.

The system is designed to automate **front-desk and inquiry handling operations** of educational institutes by responding to student queries related to **admissions, courses, fees, and schedules** using **Artificial Intelligence (AI)** and **Natural Language Processing (NLP)**.

---

## 🧠 Project Overview

Educational institutes often receive a large number of repetitive inquiries from students and parents. Handling these inquiries manually increases workload on administrative staff and results in delayed responses.

This project proposes an **AI-powered chatbot** that acts as an **automated receptionist**, capable of answering queries instantly and operating **24/7 without human intervention**.

The chatbot is implemented using:
- **Google Dialogflow** for NLP and intent detection  
- **Python Flask** for backend processing  
- **MySQL** for data storage and management  

---

## 🎯 Objectives

- Automate student inquiry handling  
- Reduce workload on administrative staff  
- Provide 24/7 assistance to students  
- Securely store admission-related data  
- Implement NLP-based intelligent responses  

---

## ✨ Key Features

- 🤖 Automated responses to student queries  
- 📝 Admission data collection (Name, Phone, Email)  
- 💰 Course, fee, and duration information  
- 📅 Class schedule and timing updates  
- 🧠 NLP-based intent detection using Dialogflow  
- 🔗 Backend integration using Flask  
- 🗄️ MySQL database for persistent storage  

---

## 🛠️ Technology Stack

| Layer | Technology |
|-----|-----------|
| NLP Engine | Google Dialogflow ES |
| Backend | Python (Flask Framework) |
| Database | MySQL (XAMPP) |
| Webhook Testing | Ngrok |
| Version Control | Git & GitHub |

---

## 🏗️ System Architecture

![System Architecture](https://via.placeholder.com/900x400?text=System+Architecture+Diagram)

### Architecture Flow

1. User interacts with the chatbot interface  
2. Dialogflow processes the message using NLP  
3. Intent is detected and sent to Flask backend via webhook  
4. Backend performs logic and database operations  
5. Response is returned to Dialogflow  
6. User receives the final response  

---

## 📸 Project Screenshots

### Chatbot Interface
![Chatbot Interface](Screenshots/IF-1.png)


### Admission Data Storage
![Database](https://via.placeholder.com/600x300?text=MySQL+Database+View)

*(Replace placeholder images with actual project screenshots)*

---

## ⚙️ How to Run the Project Locally

### Step 1: Clone Repository

git clone https://github.com/arslanakhtar868/NLP-Chatbot-FYP-VU.git
cd NLP-Chatbot-FYP-VU

---

### Step 2: Install Dependencies
pip install flask mysql-connector-python

---

### Step 3: Database Setup
1. Open XAMPP Control Panel
2. Start Apache and MySQL
3. Open http://localhost/phpmyadmin
4. Create database: fyp_chatbot_db
5. Import fyp_chatbot_db.sql

---

### Step 4: Run Backend Server
python app.py

Server will run at:

http://localhost:5000

---

### Step 5: Dialogflow Webhook Configuration

ngrok http 5000

1. Copy HTTPS URL
2. Paste into Dialogflow Fulfillment Webhook
3. Enable webhook for required intents

---

### 🎓 Project Details

Project Type: Final Year Project (FYP)

Level: BSSE

University: Virtual University of Pakistan

---

### 👨‍💻 Author

Muhammad Arslan Akhtar
Final Year Student
arslanakhtar868@gmail.com

---

### 👨‍🏫 Supervisor

Abdullah Qammar (https://github.com/aqdesk)

---

### 🔮 Future Enhancements

Multi-language support (Urdu / English)

Voice-based chatbot interaction

Mobile application integration

Online admission and fee payment

---

### 📄 License & Usage

This project is intended for academic evaluation and learning purposes only.

