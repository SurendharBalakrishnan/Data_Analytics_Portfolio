# Credit Card Payment History - Phase 1: Email Fetcher
## Complete Implementation Guide

This notebook walks you through the complete Phase 1 implementation for fetching PDF attachments from your email (HDFC and IDFC credit card statements).

### 📋 Prerequisites

Before running this notebook, ensure you have:

1. **Python libraries installed** (see requirements.txt)
2. **Email access configured** (IMAP enabled, App Password created)
3. **Project structure created** (folders for data, config, etc.)

### 🔧 Setup Instructions

#### 1. Gmail Setup (if using Gmail):
- Enable 2-Factor Authentication
- Generate App Password: Google Account → Security → 2-Step Verification → App Passwords
- Enable IMAP: Gmail Settings → Forwarding and POP/IMAP → Enable IMAP

#### 2. Other Email Providers:
- **Outlook**: Use `outlook.office365.com` as IMAP server
- **Yahoo**: Use `imap.mail.yahoo.com` as IMAP server
- Enable IMAP in your email settings

### 📁 Project Structure
```
Credit_Card_Payment_History_Project/
├── config/
│   └── email_config.json
├── data/
│   └── raw_emails/
├── src/
│   └── email_fetcher/
├── notebooks/
│   └── phase1_email_fetcher.ipynb
└── requirements.txt
```

---

## Cell 1: Import Required Libraries

```python
# Import all required libraries
import imaplib
import email
import os
import json
import logging
from datetime import datetime, timedelta
from email.header import decode_header
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append('../src')

print("✅ All libraries imported successfully!")
print(f"📅 Current date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```

---

## Cell 2: Configuration Setup

```python
# Configuration for email fetcher
CONFIG = {
    "email_address": "",  # Enter your email address
    "password": "",       # Enter your app password
    "imap_server": "imap.gmail.com",  # Change based on your provider
    "imap_port": 993,
    "download_folder": "../data/raw_emails",
    "search_criteria": {
        "hdfc_sender": "creditcards@hdfcbank.net",
        "idfc_sender": "statements@idfcfirstbank.com",
        "subject_keywords": ["statement", "credit card", "bill", "HDFC", "IDFC"]
    }
}

# Create necessary directories
os.makedirs(CONFIG['download_folder'], exist_ok=True)
os.makedirs('../config', exist_ok=True)

print("📁 Directory structure created!")
print("⚠️  IMPORTANT: Please update CONFIG with your email credentials above!")
```

---

## Cell 3: Logging Setup

```python
# Setup comprehensive logging
def setup_logging():
    """Setup logging for email fetcher"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Create logs directory
    os.makedirs('../logs', exist_ok=True)
    
    # Setup file and console logging
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('../logs/email_fetcher.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()
logger.info("🚀 Email Fetcher Phase 1 Started")
```

---

## Cell 4: Email Connection Functions

```python
def connect_to_email(config):
    """Connect to email server using IMAP"""
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
        
        # Login with credentials
        mail.login(config['email_address'], config['password'])
        
        logger.info("✅ Successfully connected to email server")
        return mail
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to email: {str(e)}")
        return None

def test_connection():
    """Test email connection with current config"""
    if not CONFIG['email_address'] or not CONFIG['password']:
        print("❌ Please update CONFIG with your email credentials first!")
        return False
    
    mail = connect_to_email(CONFIG)
    if mail:
        try:
            mail.close()
            mail.logout()
            print("✅ Email connection test successful!")
            return True
        except:
            pass
    
    print("❌ Email connection test failed!")
    return False

# Test the connection
test_connection()
```

---

## Cell 5: Email Search Functions

```python
def search_credit_card_emails(mail, config, days_back=365):
    """Search for credit card statement emails"""
    try:
        # Select inbox
        mail.select('inbox')
        
        # Calculate date range (going backwards from today)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        start_date_str = start_date.strftime("%d-%b-%Y")
        
        logger.info(f"🔍 Searching emails from {start_date_str} to today")
        
        # Multiple search criteria for better coverage
        search_criteria = [
            f'(FROM "{config["search_criteria"]["hdfc_sender"]}" SINCE "{start_date_str}")',
            f'(FROM "{config["search_criteria"]["idfc_sender"]}" SINCE "{start_date_str}")',
            '(SUBJECT "HDFC Credit Card Statement" SINCE "{}")'.format(start_date_str),
            '(SUBJECT "IDFC Credit Card Statement" SINCE "{}")'.format(start_date_str),
            '(SUBJECT "statement" SINCE "{}") (FROM "hdfc")'.format(start_date_str),
            '(SUBJECT "statement" SINCE "{}") (FROM "idfc")'.format(start_date_str),
        ]
        
        all_email_ids = set()  # Use set to avoid duplicates
        
        for criteria in search_criteria:
            try:
                typ, messages = mail.search(None, criteria)
                if messages[0]:
                    email_ids = messages[0].split()
                    all_email_ids.update(email_ids)
                    logger.info(f"Found {len(email_ids)} emails with criteria: {criteria}")
            except Exception as e:
                logger.warning(f"Search failed for criteria {criteria}: {str(e)}")
        
        unique_email_ids = list(all_email_ids)
        logger.info(f"📧 Total unique emails found: {len(unique_email_ids)}")
        
        return unique_email_ids
        
    except Exception as e:
        logger.error(f"❌ Search failed: {str(e)}")
        return []

# Test search function (will run in next cell with actual connection)
print("✅ Search functions defined successfully!")
```

---

## Cell 6: PDF Processing Functions

```python
def decode_header_value(header_value):
    """Decode email header value"""
    if header_value:
        try:
            decoded = decode_header(header_value)[0]
            if isinstance(decoded[0], bytes):
                return decoded[0].decode(decoded[1] or 'utf-8')
            return decoded[0]
        except:
            return str(header_value)
    return ""

def identify_bank(sender):
    """Identify bank from sender email"""
    sender_lower = sender.lower()
    if 'hdfc' in sender_lower:
        return 'HDFC'
    elif 'idfc' in sender_lower:
        return 'IDFC'
    elif 'axis' in sender_lower:
        return 'AXIS'
    elif 'sbi' in sender_lower:
        return 'SBI'
    elif 'icici' in sender_lower:
        return 'ICICI'
    else:
        return 'UNKNOWN'

def make_safe_filename(filename):
    """Make filename safe for filesystem"""
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename

def is_pdf_attachment(part):
    """Check if email part is a PDF attachment"""
    content_disposition = part.get("Content-Disposition", "")
    content_type = part.get_content_type()
    filename = part.get_filename()
    
    is_attachment = "attachment" in content_disposition
    is_pdf = (content_type == "application/pdf" or 
              (filename and filename.lower().endswith('.pdf')))
    
    return is_attachment and is_pdf

print("✅ PDF processing functions defined successfully!")
```

---

## Cell 7: Main PDF Download Function

```python
def extract_pdf_attachments(mail, email_ids, config):
    """Extract PDF attachments from emails"""
    pdf_files = []
    total_emails = len(email_ids)
    
    logger.info(f"📥 Processing {total_emails} emails for PDF attachments...")
    
    for idx, email_id in enumerate(email_ids, 1):
        try:
            logger.info(f"Processing email {idx}/{total_emails} (ID: {email_id.decode()})")
            
            # Fetch email
            typ, msg_data = mail.fetch(email_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parse email message
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Get email details
                    subject = decode_header_value(msg["Subject"])
                    sender = decode_header_value(msg.get("From"))
                    date = msg.get("Date")
                    
                    logger.info(f"📨 Processing: {subject[:50]}... from {sender}")
                    
                    # Process attachments
                    if msg.is_multipart():
                        for part in msg.walk():
                            if is_pdf_attachment(part):
                                pdf_info = save_pdf_attachment(
                                    part, subject, sender, date, config
                                )
                                if pdf_info:
                                    pdf_files.append(pdf_info)
                                    logger.info(f"💾 Downloaded: {pdf_info['filename']}")
                                    
        except Exception as e:
            logger.error(f"❌ Error processing email {email_id}: {str(e)}")
            continue
    
    return pdf_files

def save_pdf_attachment(part, subject, sender, date, config):
    """Save PDF attachment to disk"""
    try:
        filename = part.get_filename()
        if not filename:
            return None
            
        # Clean filename
        safe_filename = make_safe_filename(filename)
        
        # Create timestamp for unique naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine bank type from sender
        bank_type = identify_bank(sender)
        
        # Create final filename
        final_filename = f"{bank_type}_{timestamp}_{safe_filename}"
        
        # Ensure download directory exists
        download_path = config['download_folder']
        os.makedirs(download_path, exist_ok=True)
        
        # Full file path
        file_path = os.path.join(download_path, final_filename)
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(part.get_payload(decode=True))
        
        file_size = os.path.getsize(file_path)
        logger.info(f"💾 Saved PDF: {final_filename} ({file_size} bytes)")
        
        return {
            'filename': final_filename,
            'file_path': file_path,
            'bank': bank_type,
            'subject': subject,
            'sender': sender,
            'date': date,
            'size': file_size,
            'download_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error saving PDF: {str(e)}")
        return None

print("✅ PDF download functions defined successfully!")
```

---

## Cell 8: Main Execution Function

```python
def run_complete_email_fetch(config, days_back=365):
    """Main function to run the complete email fetching process"""
    logger.info("🚀 Starting Credit Card Email Fetch Process")
    
    # Validate configuration
    if not config['email_address'] or not config['password']:
        logger.error("❌ Email credentials not provided in config!")
        return []
    
    # Connect to email
    mail = connect_to_email(config)
    if not mail:
        return []
    
    try:
        # Search for emails
        email_ids = search_credit_card_emails(mail, config, days_back)
        
        if not email_ids:
            logger.info("📭 No credit card emails found")
            return []
        
        # Extract PDFs
        pdf_files = extract_pdf_attachments(mail, email_ids, config)
        
        # Save summary
        summary = {
            'total_emails_found': len(email_ids),
            'total_pdfs_downloaded': len(pdf_files),
            'download_timestamp': datetime.now().isoformat(),
            'days_searched': days_back,
            'pdf_files': pdf_files
        }
        
        # Save summary to JSON
        summary_path = os.path.join(config['download_folder'], 'download_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"✅ Process complete!")
        logger.info(f"📊 Summary: {len(email_ids)} emails found, {len(pdf_files)} PDFs downloaded")
        
        return pdf_files
        
    finally:
        # Always close connection
        try:
            mail.close()
            mail.logout()
            logger.info("🔐 Email connection closed")
        except:
            pass

print("✅ Main execution function defined successfully!")
print("🎯 Ready to run the complete email fetch process!")
```

---

## Cell 9: Execute Phase 1 - Email Fetching

```python
# IMPORTANT: Update your credentials in CONFIG before running this cell!

# Check if credentials are provided
if not CONFIG['email_address'] or not CONFIG['password']:
    print("⚠️  STOP! Please update CONFIG with your email credentials first!")
    print("📝 Edit Cell 2 and add your email address and app password")
else:
    print("🚀 Starting Phase 1: Email Fetching Process...")
    print(f"📧 Email: {CONFIG['email_address']}")
    print(f"🏦 Looking for: HDFC and IDFC credit card statements")
    print(f"📅 Time range: Last 365 days")
    print("\n" + "="*50)
    
    # Run the complete process
    downloaded_files = run_complete_email_fetch(CONFIG, days_back=365)
    
    print("="*50)
    print(f"✅ Phase 1 Complete!")
    print(f"📁 Files saved to: {CONFIG['download_folder']}")
    print(f"📊 Total PDFs downloaded: {len(downloaded_files)}")
    
    # Display summary
    if downloaded_files:
        print("\n📋 Downloaded Files Summary:")
        for i, file_info in enumerate(downloaded_files, 1):
            print(f"{i}. {file_info['bank']} - {file_info['filename']}")
            print(f"   Size: {file_info['size']} bytes")
            print(f"   Subject: {file_info['subject'][:60]}...")
            print()
```

---

## Cell 10: Verify Downloads and Next Steps

```python
# Verify the downloads
download_folder = CONFIG['download_folder']

if os.path.exists(download_folder):
    files = [f for f in os.listdir(download_folder) if f.endswith('.pdf')]
    
    print(f"📁 Download folder: {download_folder}")
    print(f"📄 Total PDF files found: {len(files)}")
    
    if files:
        print("\n📋 Files by Bank:")
        hdfc_files = [f for f in files if f.startswith('HDFC')]
        idfc_files = [f for f in files if f.startswith('IDFC')]
        unknown_files = [f for f in files if f.startswith('UNKNOWN')]
        
        print(f"🏦 HDFC: {len(hdfc_files)} files")
        print(f"🏦 IDFC: {len(idfc_files)} files")
        print(f"❓ Unknown: {len(unknown_files)} files")
        
        # Show file sizes
        total_size = sum(os.path.getsize(os.path.join(download_folder, f)) 
                        for f in files)
        print(f"💾 Total size: {total_size / 1024 / 1024:.2f} MB")
        
    print("\n🎯 Next Steps:")
    print("✅ Phase 1 Complete - Email fetching done!")
    print("📋 Phase 2 - PDF Processing and password handling")
    print("📊 Phase 3 - Data extraction and ETL pipeline")
    print("📈 Phase 4 - Dashboard creation")
    
else:
    print("❌ Download folder not found!")

# Load and display summary if available
summary_path = os.path.join(download_folder, 'download_summary.json')
if os.path.exists(summary_path):
    with open(summary_path, 'r') as f:
        summary = json.load(f)
    
    print(f"\n📊 Process Summary:")
    print(f"   📧 Emails searched: {summary['total_emails_found']}")
    print(f"   📄 PDFs downloaded: {summary['total_pdfs_downloaded']}")
    print(f"   📅 Search period: {summary['days_searched']} days")
    print(f"   ⏰ Completed at: {summary['download_timestamp']}")
```

---

## 🎯 Next Steps After Phase 1

Once you've successfully completed Phase 1, we'll move to:

### Phase 2: PDF Processing
- Handle password-protected PDFs
- Extract data from HDFC and IDFC statements
- Parse transaction details, amounts, dates

### Phase 3: ETL Pipeline
- Clean and standardize the data
- Create database schema
- Load data into SQLite/PostgreSQL

### Phase 4: Dashboard Creation
- Build Power BI or Streamlit dashboard
- Answer all your analytical questions
- Set up automated reporting

### 🔧 Configuration Tips

1. **Gmail Users**: Use App Password, not regular password
2. **Corporate Email**: Check with IT for IMAP server details
3. **Multiple Accounts**: You can modify config to handle multiple email accounts
4. **Scheduling**: Later we'll add scheduling to run this automatically

### 🚨 Important Notes

- Keep your credentials secure
- Test with a small date range first (e.g., 30 days)
- Monitor the logs for any issues
- Backup your downloaded files

---

## 📝 Save Configuration (Optional)

```python
# Save configuration for future use (without sensitive data)
safe_config = CONFIG.copy()
safe_config['password'] = "****"  # Hide password

config_path = '../config/email_config_template.json'
with open(config_path, 'w') as f:
    json.dump(safe_config, f, indent=2)

print(f"✅ Configuration template saved to: {config_path}")
print("📝 Remember to update with your actual credentials when needed!")
```