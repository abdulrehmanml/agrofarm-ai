<div align="center">
  
# 🌱 AgroFarm AI
**Your Smart, Agentic Decision Support System for Precision Agriculture**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/LLM-Gemini_2.5_Flash-8E75B2.svg)](https://deepmind.google/technologies/gemini/)

[**🚀 View Live Demo**](https://agrofarm-ai.streamlit.app/)

*Empowering farmers and agronomists with zero-hallucination, data-driven crop intelligence.*

</div>

## 💡 The Vision

Agriculture relies on precision. **AgroFarm AI** bridges the gap between static agronomy research and real-time field conditions. By fusing live weather telemetry with localized crop science via **Retrieval-Augmented Generation (RAG)**, this platform delivers highly accurate, contextual farming interventions while strictly preventing AI hallucinations.

## ✨ Core Capabilities

* **💬 Context-Aware Chatbot (RAG):** Ask complex agronomy questions in natural language. The AI fetches answers strictly from a curated, localized vector database.
* **🌦️ Agentic Field Advisor:** Automatically merges live Open-Meteo weather forecasts and current soil telemetry (NPK, moisture, pH) to recommend actionable, priority-based next steps.
* **🛡️ Zero-Hallucination Guardrails:** Programmed with strict reasoning logic. If crucial data thresholds are missing, the AI safely declines to guess, ensuring enterprise-grade reliability.
* **✅ Human-in-the-Loop (HITL):** Users retain final authority. Approve or reject AI recommendations to build a historical audit trail (`decision_log.csv`).

## 🛠️ Tech Stack & Architecture

| Component | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Generative AI** | Google Gemini 2.5 Flash | High-speed, cost-effective reasoning and NLP. |
| **Vector Engine** | ChromaDB | Local persistent storage for TF-IDF semantic embeddings. |
| **Live Telemetry** | Open-Meteo API & Pandas | Real-time weather and simulated sensor data integration. |
| **Frontend UI** | Streamlit | Responsive, high-contrast, mobile-friendly interface tailored for field use. |

## 📂 Repository Structure

```text
agrofarm-ai/
├── app.py                  # Main Streamlit UI frontend
├── src/                    # Modular OOP Backend
│   ├── llm_engine.py       # Gemini API integration & prompt orchestration
│   ├── rag_engine.py       # ChromaDB retrieval logic
│   ├── weather_engine.py   # Live telemetry mapping
│   └── config.py           # Environment variables management
├── data/                   # Data Directory
│   ├── raw/                # Raw agronomy PDFs and text files
│   ├── processed/          # Processed datasets (e.g., field telemetry CSV)
│   └── vectorstore/        # ChromaDB persistent storage & TF-IDF vectorizer
└── requirements.txt        # Exact dependency versions
```
(Note: The local vectorstore/ directory is ignored via .gitignore to keep the repository lightweight.)

## 🚀 Quick Start Guide

1. Clone the repository:
```Bash
git clone https://github.com/abdulrehmanml/agrofarm-ai.git
```
```Bash
cd agrofarm-ai
```
2. Install dependencies:
```Bash
pip install -r requirements.txt
```

3. Configure your environment:
Add your Gemini API Key to src/config.py or set it securely in your deployment environment secrets.

4. Launch the platform:
```Bash
streamlit run app.py
```
