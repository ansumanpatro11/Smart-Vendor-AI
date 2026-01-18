# Smart Vendor AI

> An AI-powered inventory and billing management system for vendors, featuring speech-to-text, semantic and keyword search, analytics, and a modern dashboard.

---

## 🚀 Features

- **Speech-to-Text Bill Entry**: Add bills by recording or uploading audio. Speech is transcribed and parsed into structured data using Sarvam AI and Gemini LLM.
- **Semantic Search vs Keyword Search**: Find products using natural language queries (semantic search with vector embeddings) or traditional keyword search.
- **Inventory Management**: View, add, and update product inventory. Stock is automatically updated when bills are processed.
- **AI Analytics**: Ask questions about your sales data using text or voice. Natural language queries are converted to SQL and results are displayed instantly.
- **Predefined Analytics Views**: Instantly access top-selling products, most profitable products, and monthly sales summaries.
- **User Authentication**: Secure login and registration with JWT-based authentication.
- **Modern Dashboard**: Streamlit-based dashboard for easy navigation and visualization.

---

## 🏗️ Project Structure

```
Smart-Vendor-AI/
├── backend/           # FastAPI backend (API, DB, services)
│   ├── main.py        # FastAPI app entrypoint
│   ├── routes/        # API endpoints (auth, inventory, bills, analytics)
│   ├── models/        # SQLAlchemy models & schemas
│   ├── db/            # DB session & setup
│   └── services/      # Speech, semantic, LLM, and business logic
├── dashboard/         # Streamlit dashboard app
│   ├── app.py         # Main dashboard launcher
│   └── pages/         # Inventory, Analytics pages
├── scripts/           # DB seeders, SQL views
├── requirements.txt   # Python dependencies
├── .env.example       # Example environment variables
└── README.md          # This file
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**

   ```sh
   git clone <repo-url>
   cd Smart-Vendor-AI
   ```

2. **Create and activate a virtual environment**

   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in required API keys and DB connection info.

5. **Set up the database**
   - Ensure your database is running (MySQL recommended).
   - Update `DATABASE_URL` in `.env`.
   - Run DB migrations and seed data:
     ```sh
     python scripts/seed.py
     ```
   - (Optional) Create analytics views:
     ```sh
     mysql -u <user> -p <db> < scripts/create_views.sql
     ```

6. **Start the backend API**

   ```sh
   uvicorn backend.main:app --reload
   ```

   - The API will be available at `http://localhost:8000`

7. **Start the dashboard**
   ```sh
   streamlit run dashboard/app.py
   ```

   - The dashboard will open in your browser (default: `http://localhost:8501`)

---

## 🧩 Key Components & Technologies

- **FastAPI**: High-performance Python API framework
- **Streamlit**: Interactive dashboard UI
- **SQLAlchemy**: ORM for database models
- **Sarvam AI**: Speech-to-text transcription
- **Google Gemini LLM**: Bill parsing & text-to-SQL
- **Pinecone + HuggingFace**: Semantic product search
- **JWT**: Secure authentication

---

## 📝 Usage Guide

### 1. **Login/Register**

    - Use the dashboard sidebar to register a new account or log in.

### 2. **Inventory Management**

    - View all products and stock levels.
    - Add or update inventory as needed.

### 3. **Add Bills (Speech-to-Text)**

    - Go to Inventory page > Add Bill by Voice.
    - Record or upload an audio file describing the bill.
    - The system transcribes, parses, and updates inventory automatically.

### 4. **Analytics**

    - Use predefined views for instant insights (top selling, most profitable, monthly summary).
    - Or, ask questions via text or speech (e.g., "What were my sales last month?").
    - The AI converts your question to SQL and shows results.

### 5. **Semantic vs Keyword Search**

    - Product search supports both traditional keyword and advanced semantic (vector-based) search for more accurate results.

---

## 🛠️ Environment Variables

Create a `.env` file with the following (see `.env.example`):

- `DATABASE_URL` - SQLAlchemy DB URL
- `GOOGLE_API_KEY` - Google Gemini API key
- `SARVAM_API_KEY` - Sarvam AI API key
- `PINECONE_API` - Pinecone vector DB API key
- `API_BASE` - (optional) API base URL for dashboard

---

## 📞 Support & Contributions

- For issues, open a GitHub issue.
- PRs welcome! Please document any new features.

---

## 📚 License

This project is licensed under the MIT License.
