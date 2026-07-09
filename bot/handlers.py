import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# ============================
# COMMAND HANDLERS
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

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands."""
    await update.message.reply_text(
        "❌ Unknown command. Please use /start or /help to see available commands."
    )
