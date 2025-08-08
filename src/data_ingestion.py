import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- 1. تعریف مسیرها و متغیرهای اصلی ---

# مسیر پوشه‌ای که اسناد خام در آن قرار دارند
SOURCE_DIRECTORY = "data/raw"

# مسیر پوشه‌ای که پایگاه داده ভکتوری در آن ذخیره خواهد شد
VECTOR_DB_DIRECTORY = "vector_db"

# نام مدل Embedding برای پردازش زبان فارسی
# این مدل یکی از مدل‌های چندزبانه محبوب و کارآمد است.
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# --- 2. توابع پردازش ---

def load_documents(source_dir: str) -> list:
    """
    اسناد را از پوشه منبع بارگذاری می‌کند.
    در این پروژه فقط فایل‌های .docx را می‌خوانیم.
    """
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
    """
    اسناد بارگذاری‌شده را به قطعات (chunks) کوچک‌تر تقسیم می‌کند.
    استراتژی تقسیم بر اساس کاراکترهای خاص قوانین (مانند "ماده" و "تبصره") است
    تا یکپارچگی معنایی حفظ شود.
    """
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
    # مقدار 'device':'cpu' تضمین می‌کند که محاسبات روی CPU انجام شود.
    # اگر GPU در دسترس دارید، می‌توانید آن را حذف کنید.
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'} 
    )

    print(f"در حال ایجاد و ذخیره‌سازی بردارها در مسیر '{vector_db_path}'...")
    # ایجاد پایگاه داده از روی قطعات متنی و ذخیره در مسیر مشخص شده
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=vector_db_path
    )
    
    print("پایگاه داده ভکتوری با موفقیت ایجاد و ذخیره شد.")


def main():
    """
    تابع اصلی برای اجرای کامل فرآیند پردازش اسناد.
    """
    print("--- شروع فاز ۲: پردازش اسناد و ساخت پایگاه دانش ---")
    
    # مرحله 1: بارگذاری اسناد
    documents = load_documents(SOURCE_DIRECTORY)
    if not documents:
        print("هیچ سندی برای پردازش یافت نشد. لطفا فایل‌های .docx را در پوشه data/raw قرار دهید.")
        return

    # مرحله 2: خرد کردن متن
    document_chunks = chunk_data(documents)

    # مرحله 3: ایجاد و ذخیره‌سازی پایگاه داده ভکتوری
    create_and_store_embeddings(document_chunks, VECTOR_DB_DIRECTORY)

    print("--- فاز ۲ با موفقیت به پایان رسید. ---")


if __name__ == "__main__":
    main()