import os
import json

def create_project_structure_in_current_dir():
    """
    Creates the project directory and file structure within the current directory.
    Assumes the script is run from the project's root folder.
    """
    # ریشه پروژه، پوشه جاری در نظر گرفته می‌شود
    root_dir = "." 
    current_path = os.getcwd()
    
    print(f"Initializing project structure in the current directory: {current_path}")

    # لیست تمام پوشه‌هایی که باید ایجاد شوند
    DIRECTORIES = [
        "data/raw",
        "data/processed",
        "docs",
        "logs",
        "src/core",
        "tests",
        "vector_db"
    ]

    # لیست تمام فایل‌هایی که باید ایجاد شوند
    FILES = {
        ".gitignore": "# Virtual Environments\nvenv/\n.venv/\n\n# System files\n.DS_Store\n\n# IDE files\n.idea/\n.vscode/\n\n# Byte-compiled files\n__pycache__/\n*.pyc",
        "Dockerfile": "# Base image\nFROM python:3.9-slim\n\n# Set working directory\nWORKDIR /app\n\n# Copy and install requirements\nCOPY requirements.txt .\nPip install --no-cache-dir -r requirements.txt\n\n# Copy project files\nCOPY . .\n\n# Command to run the app\nCMD [\"streamlit\", \"run\", \"app.py\"]",
        "README.md": "# Just-Gem-Legal-AI\n\nدستیار هوشمند تحلیل اسناد حقوقی پژوهش و فناوری ایران.",
        "app.py": "import streamlit as st\n\nst.title('دستیار هوشمند حقوقی پژوهش و فناوری ایران')\n\nquestion = st.text_input('سوال خود را اینجا بپرسید:')\n\nif st.button('ارسال'):\n    st.write(f'پرسش شما: {question}')\n    # TODO: Connect to the legal assistant core\n    st.info('پاسخ در اینجا نمایش داده خواهد شد.')\n",
        "requirements.txt": "fastapi\nuvicorn\nstreamlit\nlangchain\ntransformers\ntorch\nsentence-transformers\nchromadb-client\npython-docx\n",
        "config.py": "# Configuration settings\n# Example: API_KEY = 'YOUR_API_KEY_HERE'",
        "data/raw/.gitkeep": "",
        "data/processed/.gitkeep": "",
        "docs/architecture.md": "",
        "docs/developer_guide.md": "",
        "docs/user_guide.md": "",
        "logs/conversation_log.db": "", # Placeholder for the database
        "src/__init__.py": "",
        "src/data_ingestion.py": "# Code for reading, processing, and chunking documents.",
        "src/core/__init__.py": "",
        "src/core/generator.py": "# Code for generating answers using LLM.",
        "src/core/retriever.py": "# Code for retrieving relevant documents from vector_db.",
        "src/legal_assistant.py": "# Main assistant logic orchestrating retriever and generator.",
        "tests/__init__.py": "",
        "tests/run_evaluation.py": "# Script to run evaluations using the dataset.",
        "vector_db/.gitkeep": ""
    }

    # فایل JSON برای ارزیابی
    EVAL_JSON_FILE = "tests/evaluation_dataset.json"
    EVAL_JSON_CONTENT = [
        {
            "question": "سوال نمونه اول؟",
            "expected_answer_snippet": "بخشی از پاسخ مورد انتظار",
            "expected_citation": "ماده X قانون Y"
        }
    ]

    # ایجاد تمام پوشه‌ها
    for dir_path in DIRECTORIES:
        full_path = os.path.join(root_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"  Ensured directory exists: {os.path.join(current_path, dir_path)}")

    # ایجاد تمام فایل‌ها
    for file_path, content in FILES.items():
        full_path = os.path.join(root_dir, file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Created/updated file:      {os.path.join(current_path, file_path)}")

    # ایجاد فایل JSON ارزیابی
    eval_full_path = os.path.join(root_dir, EVAL_JSON_FILE)
    with open(eval_full_path, 'w', encoding='utf-8') as f:
        json.dump(EVAL_JSON_CONTENT, f, ensure_ascii=False, indent=4)
    print(f"  Created/updated file:      {os.path.join(current_path, EVAL_JSON_FILE)}")

    print("\nProject structure initialized successfully in the current directory.")


if __name__ == "__main__":
    create_project_structure_in_current_dir()