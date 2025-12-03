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
- Add income & expense entries  
- Editable fields (amount, description, category, type)  
- Automatic CSV handling (creates one if missing)

### 🤖 AI Intelligence
- **LLM-powered auto-categorization** (Gemini 2.5 Flash)  
- Predicts:
  - **Category** (e.g., Food, Transport, Bills, Shopping)
  - **Entry Type** (Income/Expense)
- No prompt required — the model infers everything from your description  
- User can override categories manually

### 📊 Analytics
(Currently two charts — more coming soon)
- Monthly breakdown  
- Category-based spend distribution  

### 📁 Data Storage
- CSV-based data persistence  
- Auto-updates whenever an entry is added  
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
git clone https://github.com/yourusername/finsight-ai.git
cd finsight-ai
```
### 2. Install dependencies
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

### 5. Visualizations update automatically

All AI is abstracted in ``llm_service.py.``

## 🚧 Roadmap (Upcoming Features)

- AutoML integration for spend prediction
- OCR-based receipt scanning
- Anomaly detection (fraud or unusual spending detection)
- Advanced analytics dashboard
- Category recommendation engine
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