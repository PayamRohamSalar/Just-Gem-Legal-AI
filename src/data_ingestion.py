import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- 1. تعریف مسیرها و متغیرهای اصلی ---
SOURCE_DIRECTORY = "data/raw"
VECTOR_DB_DIRECTORY = "vector_db"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# --- 2. توابع پردازش ---

def load_documents(source_dir: str) -> list:
    print("در حال بارگذاری اسناد...")
    all_docs = []
    for filename in os.listdir(source_dir):
        if filename.endswith(".docx"):
            file_path = os.path.join(source_dir, filename)
            try:
                loader = Docx2txtLoader(file_path)
                docs = loader.load()
                all_docs.extend(docs)
                print(f"فایل '{filename}' با موفقیت بارگذاری شد.")
            except Exception as e:
                print(f"خطا در بارگذاری فایل '{filename}': {e}")
    return all_docs

def chunk_data(documents: list, chunk_size: int = 1000, chunk_overlap: int = 100) -> list:
    print("در حال تقسیم‌بندی اسناد به قطعات (Chunking)...")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\nماده", "\nتبصره", "\n\n", "\n", " "],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"تعداد کل قطعات ایجاد شده: {len(chunks)}")
    return chunks

def create_and_store_embeddings(chunks: list, vector_db_path: str):
    """
    برای هر قطعه، بردار (embedding) ایجاد کرده و آن را در پایگاه داده ভکتوری ذخیره می‌کند.
    """
    print("در حال ایجاد مدل Embedding...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'}
    )

    print(f"در حال ایجاد و ذخیره‌سازی بردارها در مسیر '{vector_db_path}'...")
    # استفاده از روش ساده و استاندارد که با این نسخه از Chroma کار می‌کند
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=vector_db_path
    )
    
    print("پایگاه داده ভکتوری با موفقیت ایجاد و ذخیره شد.")

def main():
    print("--- شروع فاز ۲: پردازش اسناد و ساخت پایگاه دانش ---")
    documents = load_documents(SOURCE_DIRECTORY)
    if not documents:
        print("هیچ سندی برای پردازش یافت نشد. لطفا فایل‌های .docx را در پوشه data/raw قرار دهید.")
        return
    document_chunks = chunk_data(documents)
    create_and_store_embeddings(document_chunks, VECTOR_DB_DIRECTORY)
    print("--- فاز ۲ با موفقیت به پایان رسید. ---")

if __name__ == "__main__":
    main()