# Maratha & OBC Reservation Q&A Chatbot

This is a Streamlit application powered by Google's Gemini model.  
It only answers questions related to **Maratha reservation** and **OBC-related issues in India**, following the Indian Reservation Acts.

---

## Features
- Restricted Q&A: Only about Maratha reservation & OBC reservation matters.
- Bilingual Support: English & Marathi (auto-detects based on user input).
- Policy-based responses: Grounded in Indian Constitution, GRs, NCBC guidelines, and court rulings.
- Styled interface inspired by Manoj Dada Jarange’s movement.

---

## Setup Instructions

### 1. Clone or extract project
Unzip the provided `maratha_obc_app` file.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
Create a `.env` file (already included) and put your Google Gemini API key:
```
GOOGLE_API_KEY=your_api_key_here
```

Or set it directly in terminal:
```bash
export GOOGLE_API_KEY="your_api_key_here"   # macOS/Linux
setx GOOGLE_API_KEY "your_api_key_here"     # Windows PowerShell
```

### 4. Run the application
```bash
streamlit run app.py
```

It will open automatically in your browser at `http://localhost:8501`.

---

## Notes

---

## Usage
- Enter your query in English or Marathi. The app auto-detects language and responds accordingly.
- Only queries related to Maratha or OBC reservation will be answered. Others will be refused politely.

## Troubleshooting
- **Regex error (TypeError: unhashable type: 'dict')**: This occurs if the app tries to compile a regex from a dictionary. Ensure you are using the latest code, which builds the regex from all phrases in `ALLOW_PATTERN.json`.
- **API Key issues**: Make sure your Gemini API key is set in `.env` or as an environment variable.
- **Dependency errors**: Run `pip install -r requirements.txt` to install all required packages.

## Testing
Unit tests are provided for the language detection function.

To run tests:
```bash
C:/Users/SA/Downloads/maratha_obc_app/venv/Scripts/python.exe -m pytest test_app.py
```
All tests should pass if the app is set up correctly.

## Customization
To add or change allowed topics, edit `ALLOW_PATTERN.json` and restart the app.

---
✍️ Inspired by Manoj Dada Jarange’s movement for justice.

---

✍️ Inspired by Manoj Dada Jarange’s movement for justice.
