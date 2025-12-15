# FinSight AI  
### Intelligent Personal Finance Tracker powered by LLMs

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LLM](https://img.shields.io/badge/AI-Gemini_2.5_Flash-green)
![License](https://img.shields.io/badge/License-MIT-black)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

FinSight AI is an intelligent financial tracking system that automatically categorizes transactions, analyzes spending patterns, and provides smart insights — all powered by **Gemini 2.5 Flash**, **Pandas**, and **Streamlit**.

This project is built with a focus on **clean architecture**, **automation**, and **real-world usability**, making it ideal for personal use, demos, and portfolio showcasing.

## 🚀 Features

### 🔵 Core
- Add income & expense entries through a **clear-on-submit form**  
- Auto-predicted **category and entry type** using AI, editable by the user  
- Automatic CSV handling (creates one if missing)  
- One-click CSV download from the UI

### 🤖 AI Intelligence
- **LLM-powered auto-categorization** (Gemini 2.5 Flash)  
- Predicts:
  - **Category** (Food, Transport, Bills, Shopping, etc.)  
  - **Entry Type** (Income/Expense)  
- Dynamic prediction is **cached per note** to avoid repeated API calls  
- Monthly AI insights analyzing spending patterns, top expenses, and actionable suggestions  

### 📊 Analytics
- Monthly breakdown with **Month names instead of numbers**  
- Category-based spend distribution  
- Visualizations update automatically after each entry  

### 📁 Data Storage
- CSV-based data persistence (`expense_data_1.csv`)  
- Auto-updates whenever a new entry is added  
- One-click CSV download from UI

## 🧱 Tech Stack

| Component        | Technology |
|-----------------|-------------|
| Frontend         | Streamlit |
| AI Model         | Gemini 2.5 Flash |
| Data Layer       | CSV (migrating to DB soon) |
| Visualization    | Matplotlib |
| Processing       | Pandas |


## 🗂 Project Structure

├── app.py  
├── data_handler.py  
├── visualize.py  
├── llm_service.py  
├── requirements.txt  
├── README.md  
└── expense_data_1.csv (auto-generated)

## ⚙ Installation

### 1. Clone the repo
```bash
git clone https://github.com/PypCoder/finsight-ai.git
cd finsight-ai
```
### 2a. Set up your API Key
Create a `.env` file in the project root and add your Gemini API key:
```env
GENAI_API_KEY=your_api_key_here
```
The app will automatically load this key using `python-dotenv`.
### 2b. Install dependencies
```python
pip install -r requirements.txt
```

### 3. Run the App
```python
streamlit run app.py
```

## 📥 CSV Export

The app automatically stores all transactions in expense_data_1.csv.

Download from the UI using the ``download_button`` provided the UI.


## 🧠 AI Logic

FinSight AI uses a hybrid workflow:

### 1. User enters:
- Description
- Amount

### 2. LLM predicts:
- Category
- Entry type

### 3. User can override the results

### 4. Entry is logged and appended to persistent CSV

### 5. Visualizations and Monthly AI Insights update automatically

All AI logic is abstracted in ``llm_service.py.``

## 🚧 Roadmap

### ✅ Implemented
- Monthly AI Insights
- Category recommendation engine

### 🔜 Upcoming
- OCR-based receipt scanning
- Anomaly detection (fraud or unusual spending detection)
- Advanced analytics dashboard
- Database migration (SQLite / Supabase)

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

## 📜 License

MIT License.

## ⭐ Support

If you like this project, please consider giving it a star on GitHub ⭐


---

<p align="center">
  <a href="https://github.com/PypCoder" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-PypCoder-181717?style=for-the-badge&logo=github&logoColor=white" alt="PypCoder GitHub"/>
  </a>
</p>