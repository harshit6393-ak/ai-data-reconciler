# AI Data Reconciliation Engine 🚀

A full-stack, multimodal AI application designed to automate data reconciliation. This tool leverages Large Language Models (LLMs) and Vision APIs to semantically compare structured digital records (JSON/Databases) against physical documents (receipts, invoices), eliminating the need for strict regex or rigid heuristic rules.

## 🌟 Features

* **Multimodal Vision Processing:** Upload physical receipts or invoices. The AI extracts the unstructured text, amounts, and dates directly from the image pixels.
* **Semantic Data Matching:** Replaces traditional exact-string matching. The engine understands that "Microsoft Corp" and "MSFT" are the same entity.
* **Structured JSON Output:** The LLM is strictly prompted to return programmatic JSON (Confidence Score, Boolean Match, and Explanation), making it ready for enterprise database integration.
* **Full-Stack Architecture:** Built with a decoupled architecture featuring a blazing-fast Python REST API and a modern React frontend.

## 🛠️ Tech Stack

* **Frontend:** React, Vite, JavaScript, CSS
* **Backend:** Python, FastAPI, Uvicorn, Pydantic
* **AI/ML:** Google Gemini 1.5 Flash (Vision & Text capabilities), Prompt Engineering
* **Data Handling:** Multipart Form Data, JSON parsing

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Node.js & npm
* A free [Google Gemini API Key](https://aistudio.google.com/)

### 1. Backend Setup (FastAPI)
Clone the repository and navigate to the root directory.
```bash
git clone [https://github.com/your-username/ai-data-reconciler.git](https://github.com/your-username/ai-data-reconciler.git)
cd ai-data-reconciler