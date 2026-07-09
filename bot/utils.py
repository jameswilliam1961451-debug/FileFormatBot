import os
import logging
from PIL import Image
import PyPDF2
import docx
import pandas as pd
from pydub import AudioSegment

logger = logging.getLogger(__name__)

# ============================
# IMAGE CONVERSION
# ============================

def convert_image(input_path, output_format):
    """Convert image to specified format."""
    try:
        with Image.open(input_path) as img:
            output_path = f"{os.path.splitext(input_path)[0]}.{output_format.lower()}"
            img.save(output_path, format=output_format.upper())
        return output_path
    except Exception as e:
        logger.error(f"Image conversion error: {e}")
        return None

# ============================
# DOCUMENT CONVERSION
# ============================

def pdf_to_text(input_path):
    """Extract text from PDF."""
    try:
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"PDF to text error: {e}")
        return None

def docx_to_text(input_path):
    """Extract text from DOCX."""
    try:
        doc = docx.Document(input_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        logger.error(f"DOCX to text error: {e}")
        return None

# ============================
# AUDIO CONVERSION
# ============================

def convert_audio(input_path, output_format):
    """Convert audio to specified format."""
    try:
        audio = AudioSegment.from_file(input_path)
        output_path = f"{os.path.splitext(input_path)[0]}.{output_format.lower()}"
        audio.export(output_path, format=output_format.lower())
        return output_path
    except Exception as e:
        logger.error(f"Audio conversion error: {e}")
        return None

# ============================
# SPREADSHEET CONVERSION
# ============================

def excel_to_csv(input_path):
    """Convert Excel to CSV."""
    try:
        df = pd.read_excel(input_path)
        output_path = f"{os.path.splitext(input_path)[0]}.csv"
        df.to_csv(output_path, index=False)
        return output_path
    except Exception as e:
        logger.error(f"Excel to CSV error: {e}")
        return None

# ============================
# FILE UTILITIES
# ============================

def get_file_extension(filename):
    """Get file extension."""
    return os.path.splitext(filename)[1].lower()

def is_image(filename):
    """Check if file is an image."""
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    return get_file_extension(filename) in extensions

def is_document(filename):
    """Check if file is a document."""
    extensions = ['.pdf', '.docx', '.txt', '.html', '.odt', '.rtf', '.md']
    return get_file_extension(filename) in extensions

def is_audio(filename):
    """Check if file is audio."""
    extensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac']
    return get_file_extension(filename) in extensions

def is_video(filename):
    """Check if file is video."""
    extensions = ['.mp4', '.mkv', '.avi', '.webm', '.mov', '.flv']
    return get_file_extension(filename) in extensions

def is_archive(filename):
    """Check if file is an archive."""
    extensions = ['.zip', '.rar', '.7z', '.tar', '.gz']
    return get_file_extension(filename) in extensions
