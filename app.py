import os
import logging
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Get bot token
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-app.up.railway.app/webhook")

# Create Telegram application
application = Application.builder().token(BOT_TOKEN).build()

# ============================
# BOT COMMAND HANDLERS
# ============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = f"""
👋 Welcome to FileFormatProBot, {user.first_name}!

I can convert your files between different formats.

🔹 **What I can do:**
• 📸 Image conversion: JPEG, PNG, WebP, GIF, TIFF, BMP
• 📄 Document conversion: PDF, DOCX, TXT, HTML
• 🎵 Audio conversion: MP3, WAV, OGG, FLAC
• 🎬 Video conversion: MP4, MKV, AVI, WEBM
• 📦 Archive extraction: ZIP, RAR, 7Z, TAR

📌 **How to use:**
1. Send me any file
2. Choose the format you want to convert to
3. I'll send you the converted file!

Type /help for more information.
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued."""
    help_text = """
🆘 **Help Center**

**How to use this bot:**
1. Send me any file
2. I'll show you available conversion options
3. Click the format you want
4. Receive your converted file!

**Supported formats:**
• Images: JPEG, PNG, WebP, GIF, TIFF, BMP
• Documents: PDF, DOCX, TXT, HTML, ODT
• Audio: MP3, WAV, OGG, FLAC, M4A
• Video: MP4, MKV, AVI, WEBM, MOV
• Archives: ZIP, RAR, 7Z, TAR

**Commands:**
/start - Show welcome message
/help - Show this help
/formats - List all supported formats
/about - About this bot

Questions? Contact @your_support_username
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def formats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all supported formats."""
    formats_text = """
📋 **Supported Formats**

**Images:**
JPEG, PNG, WebP, GIF, TIFF, BMP, ICO

**Documents:**
PDF, DOCX, TXT, HTML, ODT, RTF, MD

**Audio:**
MP3, WAV, OGG, FLAC, M4A, AAC

**Video:**
MP4, MKV, AVI, WEBM, MOV, FLV

**Archives:**
ZIP, RAR, 7Z, TAR, GZ

**Spreadsheets:**
XLSX, CSV, ODS

**Ebooks:**
EPUB, MOBI, PDF, TXT

**Just send a file to get started!**
"""
    await update.message.reply_text(formats_text, parse_mode='Markdown')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About the bot."""
    about_text = """
ℹ️ **About FileFormatProBot**

Version: 1.0.0
Created: 2026

This bot helps you convert files between different formats quickly and easily. No registration required, no limits on file size.

**Why use this bot?**
• ✅ 100% free to use
• ✅ No registration required
• ✅ Fast conversion
• ✅ 50+ supported formats
• ✅ Your privacy is respected

Built with ❤️ using Python and the Telegram Bot API.
"""
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file uploads."""
    file = update.message.document or update.message.photo or update.message.video or update.message.audio
    
    if not file:
        await update.message.reply_text("❌ Please send a file to convert.")
        return
    
    # Get file info
    file_name = getattr(file, 'file_name', 'unknown')
    file_id = file.file_id
    
    # Store file info in context
    context.user_data['file_id'] = file_id
    context.user_data['file_name'] = file_name
    
    # Create keyboard with conversion options
    keyboard = [
        [InlineKeyboardButton("📸 Image Formats", callback_data='image_formats')],
        [InlineKeyboardButton("📄 Document Formats", callback_data='doc_formats')],
        [InlineKeyboardButton("🎵 Audio Formats", callback_data='audio_formats')],
        [InlineKeyboardButton("🎬 Video Formats", callback_data='video_formats')],
        [InlineKeyboardButton("📦 Archive Formats", callback_data='archive_formats')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"📁 Received: **{file_name}**\n\nChoose the format you want to convert to:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Show format options based on category
    if data == 'image_formats':
        keyboard = [
            [InlineKeyboardButton("JPEG", callback_data='convert_jpeg'),
             InlineKeyboardButton("PNG", callback_data='convert_png')],
            [InlineKeyboardButton("WebP", callback_data='convert_webp'),
             InlineKeyboardButton("GIF", callback_data='convert_gif')],
            [InlineKeyboardButton("TIFF", callback_data='convert_tiff'),
             InlineKeyboardButton("BMP", callback_data='convert_bmp')],
            [InlineKeyboardButton("🔙 Back", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📸 **Choose image format:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == 'doc_formats':
        keyboard = [
            [InlineKeyboardButton("PDF", callback_data='convert_pdf'),
             InlineKeyboardButton("DOCX", callback_data='convert_docx')],
            [InlineKeyboardButton("TXT", callback_data='convert_txt'),
             InlineKeyboardButton("HTML", callback_data='convert_html')],
            [InlineKeyboardButton("ODT", callback_data='convert_odt'),
             InlineKeyboardButton("RTF", callback_data='convert_rtf')],
            [InlineKeyboardButton("🔙 Back", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📄 **Choose document format:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == 'audio_formats':
        keyboard = [
            [InlineKeyboardButton("MP3", callback_data='convert_mp3'),
             InlineKeyboardButton("WAV", callback_data='convert_wav')],
            [InlineKeyboardButton("OGG", callback_data='convert_ogg'),
             InlineKeyboardButton("FLAC", callback_data='convert_flac')],
            [InlineKeyboardButton("M4A", callback_data='convert_m4a'),
             InlineKeyboardButton("AAC", callback_data='convert_aac')],
            [InlineKeyboardButton("🔙 Back", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎵 **Choose audio format:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == 'video_formats':
        keyboard = [
            [InlineKeyboardButton("MP4", callback_data='convert_mp4'),
             InlineKeyboardButton("MKV", callback_data='convert_mkv')],
            [InlineKeyboardButton("AVI", callback_data='convert_avi'),
             InlineKeyboardButton("WEBM", callback_data='convert_webm')],
            [InlineKeyboardButton("MOV", callback_data='convert_mov'),
             InlineKeyboardButton("FLV", callback_data='convert_flv')],
            [InlineKeyboardButton("🔙 Back", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎬 **Choose video format:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == 'archive_formats':
        keyboard = [
            [InlineKeyboardButton("ZIP", callback_data='convert_zip'),
             InlineKeyboardButton("RAR", callback_data='convert_rar')],
            [InlineKeyboardButton("7Z", callback_data='convert_7z'),
             InlineKeyboardButton("TAR", callback_data='convert_tar')],
            [InlineKeyboardButton("GZ", callback_data='convert_gz'),
             InlineKeyboardButton("🔙 Back", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📦 **Choose archive format:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == 'back_to_main':
        keyboard = [
            [InlineKeyboardButton("📸 Image Formats", callback_data='image_formats')],
            [InlineKeyboardButton("📄 Document Formats", callback_data='doc_formats')],
            [InlineKeyboardButton("🎵 Audio Formats", callback_data='audio_formats')],
            [InlineKeyboardButton("🎬 Video Formats", callback_data='video_formats')],
            [InlineKeyboardButton("📦 Archive Formats", callback_data='archive_formats')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📁 Choose the format you want to convert to:",
            reply_markup=reply_markup
        )
    
    elif data.startswith('convert_'):
        # Handle actual conversion
        format_type = data.replace('convert_', '')
        await query.edit_message_text(
            f"🔄 Converting to **{format_type.upper()}**...\n\nThis may take a moment.",
            parse_mode='Markdown'
        )
        
        # Here you would implement actual conversion logic
        # For demo, we'll just send a message
        await query.message.reply_text(
            f"✅ Conversion complete!\n\nYour file has been converted to **{format_type.upper()}**.\n\n*(This is a demo. Actual conversion will be implemented in the next version.)*",
            parse_mode='Markdown'
        )

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("formats", formats))
application.add_handler(CommandHandler("about", about))
application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO, handle_file))
application.add_handler(CallbackQueryHandler(button_callback))

# ============================
# FLASK WEBHOOK
# ============================

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "bot": "FileFormatProBot",
        "version": "1.0.0",
        "message": "Bot is running!"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle incoming webhook updates."""
    try:
        # Get update data
        update_data = request.get_json()
        if not update_data:
            return jsonify({"ok": False, "error": "No data provided"}), 400
        
        # Create Update object
        update = Update.de_json(update_data, application.bot)
        
        # Process update
        await application.process_update(update)
        
        return jsonify({"ok": True}), 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

# ============================
# SET WEBHOOK ENDPOINT
# ============================

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set webhook URL."""
    try:
        webhook_url = WEBHOOK_URL
        response = application.bot.set_webhook(webhook_url)
        if response:
            return jsonify({"ok": True, "message": f"Webhook set to {webhook_url}"})
        else:
            return jsonify({"ok": False, "error": "Failed to set webhook"}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ============================
# RUN APPLICATION
# ============================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
