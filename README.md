# 🎓 AI-Powered Student Support Chatbot

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql)
![Dialogflow](https://img.shields.io/badge/Dialogflow-NLP-green?style=for-the-badge&logo=google-cloud)

> **An intelligent conversational agent designed to automate student inquiries, course registrations, and schedule management using Natural Language Processing (NLP).**

---

## 🚀 Project Overview
This project solves the problem of manual student handling by providing a **24/7 Virtual Assistant**. The chatbot understands natural human language and performs real-time database operations to assist students.

**Key Features:**
* 🤖 **NLP Understanding:** Uses Google Dialogflow to understand user intents (Greetings, Inquiries, etc.).
* 📂 **Smart Course Info:** Fetches course fees, duration, and details dynamically from the database.
* 📝 **Auto-Registration:** Students can register for courses directly through chat (Data is saved to MySQL).
* 📅 **Schedule Tracking:** Provides class timings and days instantly.
* 🧠 **Smart Small Talk:** Hybrid approach using Dialogflow & Regex for human-like small talk.
* 🛡️ **Error Handling:** Intelligent retry logic if a user inputs incorrect data.

---

## 📸 Screenshots
*(Upload screenshots of your chatbot here)*

| Chat Interface | Registration Flow | Database View |
|:---:|:---:|:---:|
| ![Chat](https://via.placeholder.com/200x400?text=Chat+Interface) | ![Register](https://via.placeholder.com/200x400?text=Registration) | ![DB](https://via.placeholder.com/300x200?text=Database) |

---

## 🛠️ Tech Stack
* **Frontend:** Dialogflow ES (Natural Language Processing)
* **Backend:** Python (Flask Framework)
* **Database:** MySQL (XAMPP Server)
* **Tunneling:** Ngrok (For exposing localhost to the web)
* **Tools:** VS Code, Postman, PHPMyAdmin

---

## ⚙️ How to Run Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/ArslanAkhtar/NLP-Chatbot.git](https://github.com/ArslanAkhtar/NLP-Chatbot.git)
cd NLP-Chatbot
