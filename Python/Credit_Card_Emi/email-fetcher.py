#!/usr/bin/env python3
"""
Credit Card Payment History - Phase 1: Email Fetcher Script
Complete production-ready implementation for automated email fetching
Author: Senior Data Analyst Team
Date: 2025-08-09
"""

import imaplib
import email
import os
import json
import logging
import argparse
import sys
from datetime import datetime, timedelta
from email.header import decode_header
from pathlib import Path
from typing import List, Dict, Optional, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; fall back to environment variables already set

class CreditCardEmailFetcher:
    """
    Production-ready email fetcher for credit card statements
    Supports HDFC, IDFC and other Indian banks
    """
    
    def __init__(self, config_path: str = 'config/email_config.json'):
        """Initialize email fetcher with configuration"""
        self.config = self.load_config(config_path)
        self.logger = self.setup_logging()
        self.downloaded_files = []
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration. Credentials are read from environment variables (.env).
        Non-sensitive settings fall back to the JSON config file if present."""
        config = self._get_default_config()

        # Load non-sensitive settings from JSON if it exists
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                # Merge only non-credential keys from the file
                for key in ('download_folder', 'search_criteria', 'file_naming', 'filters'):
                    if key in file_config:
                        config[key] = file_config[key]
        except Exception as e:
            print(f"⚠️  Could not read config file ({e}). Using defaults.")

        # Always load credentials from environment variables
        env_email = os.environ.get('EMAIL_ADDRESS', '')
        env_password = os.environ.get('EMAIL_PASSWORD', '')
        env_imap = os.environ.get('IMAP_SERVER', 'imap.gmail.com')
        env_port = os.environ.get('IMAP_PORT', '993')

        if not env_email or not env_password:
            print("⚠️  EMAIL_ADDRESS or EMAIL_PASSWORD not set in environment.")
            print("    Copy .env.example → .env and fill in your credentials.")

        config['email_address'] = env_email
        config['password'] = env_password
        config['imap_server'] = env_imap
        config['imap_port'] = int(env_port)

        return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "email_address": "",
            "password": "",
            "imap_server": "imap.gmail.com",
            "imap_port": 993,
            "download_folder": "data/raw_emails",
            "search_criteria": {
                "hdfc_senders": [
                    "creditcards@hdfcbank.net",
                    "creditcard@hdfcbank.net",
                    "statements@hdfcbank.com"
                ],
                "idfc_senders": [
                    "statements@idfcfirstbank.com",
                    "creditcard@idfcfirstbank.com",
                    "noreply@idfcfirstbank.com"
                ],
                "subject_keywords": [
                    "statement", "credit card", "bill", "HDFC", "IDFC",
                    "Credit Card Statement", "Monthly Statement"
                ]
            },
            "file_naming": {
                "include_timestamp": True,
                "include_bank_name": True,
                "include_statement_date": True
            },
            "filters": {
                "min_file_size": 1024,  # Minimum 1KB
                "max_file_size": 10485760,  # Maximum 10MB
                "allowed_extensions": [".pdf"]
            }
        }
    
    def setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Setup formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup file handler
        file_handler = logging.FileHandler(
            f'logs/email_fetcher_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Setup logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def validate_config(self) -> bool:
        """Validate configuration before processing"""
        if not self.config.get('email_address'):
            self.logger.error("❌ Email address not configured")
            return False
        
        if not self.config.get('password'):
            self.logger.error("❌ Email password/app password not configured")
            return False
        
        if not self.config.get('imap_server'):
            self.logger.error("❌ IMAP server not configured")
            return False
        
        return True
    
    def connect_to_email(self) -> Optional[imaplib.IMAP4_SSL]:
        """Connect to email server using IMAP with error handling"""
        try:
            self.logger.info(f"🔌 Connecting to {self.config['imap_server']}...")
            
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(
                self.config['imap_server'], 
                self.config['imap_port']
            )
            
            # Login with credentials
            mail.login(
                self.config['email_address'], 
                self.config['password']
            )
            
            self.logger.info("✅ Successfully connected to email server")
            return mail
            
        except imaplib.IMAP4.error as e:
            self.logger.error(f"❌ IMAP error: {str(e)}")
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to email: {str(e)}")
        
        return None
    
    def search_credit_card_emails(self, mail: imaplib.IMAP4_SSL, 
                                 days_back: int = 365) -> List[bytes]:
        """Search for credit card statement emails with comprehensive criteria"""
        try:
            # Select inbox
            mail.select('inbox')
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            start_date_str = start_date.strftime("%d-%b-%Y")
            
            self.logger.info(f"🔍 Searching emails from {start_date_str} to today")
            
            # Build comprehensive search criteria
            all_senders = (self.config['search_criteria']['hdfc_senders'] + 
                          self.config['search_criteria']['idfc_senders'])
            
            search_criteria = []
            
            # Search by sender emails
            for sender in all_senders:
                search_criteria.append(
                    f'(FROM "{sender}" SINCE "{start_date_str}")'
                )
            
            # Search by subject keywords combined with date
            for keyword in self.config['search_criteria']['subject_keywords']:
                search_criteria.append(
                    f'(SUBJECT "{keyword}" SINCE "{start_date_str}")'
                )
            
            # Additional combined searches for better coverage
            search_criteria.extend([
                f'(BODY "HDFC Credit Card" SINCE "{start_date_str}")',
                f'(BODY "IDFC FIRST Bank" SINCE "{start_date_str}")',
                f'(SUBJECT "statement" BODY "credit card" SINCE "{start_date_str}")',
            ])
            
            all_email_ids = set()
            
            for criteria in search_criteria:
                try:
                    typ, messages = mail.search(None, criteria)
                    if messages[0]:
                        email_ids = messages[0].split()
                        all_email_ids.update(email_ids)
                        self.logger.debug(
                            f"Found {len(email_ids)} emails with criteria: {criteria}"
                        )
                except Exception as e:
                    self.logger.warning(
                        f"Search failed for criteria {criteria}: {str(e)}"
                    )
            
            unique_email_ids = list(all_email_ids)
            self.logger.info(f"📧 Total unique emails found: {len(unique_email_ids)}")
            
            return unique_email_ids
            
        except Exception as e:
            self.logger.error(f"❌ Search failed: {str(e)}")
            return []
    
    def decode_header_value(self, header_value: str) -> str:
        """Decode email header value safely"""
        if not header_value:
            return ""
        
        try:
            decoded = decode_header(header_value)[0]
            if isinstance(decoded[0], bytes):
                encoding = decoded[1] or 'utf-8'
                return decoded[0].decode(encoding, errors='ignore')
            return str(decoded[0])
        except Exception as e:
            self.logger.warning(f"Header decode failed: {e}")
            return str(header_value)
    
    def identify_bank(self, sender: str, subject: str = "") -> str:
        """Identify bank from sender email and subject"""
        combined_text = f"{sender.lower()} {subject.lower()}"
        
        bank_patterns = {
            'HDFC': ['hdfc', 'hdfcbank'],
            'IDFC': ['idfc', 'idfcfirst'],
            'AXIS': ['axis', 'axisbank'],
            'ICICI': ['icici', 'icicibank'],
            'SBI': ['sbi', 'onlinesbi'],
            'KOTAK': ['kotak', 'kotakbank'],
            'CITI': ['citi', 'citibank'],
            'AMEX': ['americanexpress', 'amex'],
            'YES': ['yesbank', 'yes bank'],
            'INDUSIND': ['indusind', 'induslnd']
        }
        
        for bank, patterns in bank_patterns.items():
            if any(pattern in combined_text for pattern in patterns):
                return bank
        
        return 'UNKNOWN'
    
    def make_safe_filename(self, filename: str) -> str:
        """Make filename safe for filesystem"""
        # Remove unsafe characters
        unsafe_chars = '<>:"/\\|?*'
        safe_name = filename
        for char in unsafe_chars:
            safe_name = safe_name.replace(char, '_')
        
        # Remove multiple underscores and trim
        safe_name = '_'.join(safe_name.split())
        return safe_name[:100]  # Limit length
    
    def is_pdf_attachment(self, part: email.message.EmailMessage) -> bool:
        """Check if email part is a PDF attachment"""
        content_disposition = part.get("Content-Disposition", "")
        content_type = part.get_content_type()
        filename = part.get_filename()
        
        is_attachment = "attachment" in content_disposition
        is_pdf = (content_type == "application/pdf" or 
                 (filename and filename.lower().endswith('.pdf')))
        
        return is_attachment and is_pdf
    
    def extract_statement_date(self, subject: str, filename: str) -> str:
        """Extract statement date from subject or filename"""
        import re
        
        # Common date patterns in credit card statements
        date_patterns = [
            r'(\d{2})[-/](\d{2})[-/](\d{4})',  # DD-MM-YYYY or DD/MM/YYYY
            r'(\d{4})[-/](\d{2})[-/](\d{2})',  # YYYY-MM-DD or YYYY/MM/DD
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s\-_]*(\d{4})',  # Mon YYYY
            r'(\d{2})[\s\-_]*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s\-_]*(\d{4})',  # DD Mon YYYY
        ]
        
        combined_text = f"{subject} {filename}"
        
        for pattern in date_patterns:
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                return match.group(0).replace(' ', '_')
        
        return datetime.now().strftime("%Y%m")
    
    def save_pdf_attachment(self, part: email.message.EmailMessage, 
                          subject: str, sender: str, date: str) -> Optional[Dict[str, Any]]:
        """Save PDF attachment with intelligent naming"""
        try:
            filename = part.get_filename()
            if not filename:
                return None
            
            # Get payload and validate
            payload = part.get_payload(decode=True)
            if not payload:
                return None
            
            # Check file size constraints
            file_size = len(payload)
            min_size = self.config['filters']['min_file_size']
            max_size = self.config['filters']['max_file_size']
            
            if file_size < min_size:
                self.logger.warning(f"File too small ({file_size} bytes): {filename}")
                return None
            
            if file_size > max_size:
                self.logger.warning(f"File too large ({file_size} bytes): {filename}")
                return None
            
            # Create intelligent filename
            safe_filename = self.make_safe_filename(filename)
            bank_type = self.identify_bank(sender, subject)
            statement_date = self.extract_statement_date(subject, filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Build final filename with all components
            name_parts = []
            
            if self.config['file_naming']['include_bank_name']:
                name_parts.append(bank_type)
            
            if self.config['file_naming']['include_statement_date']:
                name_parts.append(statement_date)
            
            if self.config['file_naming']['include_timestamp']:
                name_parts.append(timestamp)
            
            name_parts.append(safe_filename)
            
            final_filename = '_'.join(name_parts)
            
            # Ensure download directory exists
            download_path = self.config['download_folder']
            os.makedirs(download_path, exist_ok=True)
            
            # Full file path
            file_path = os.path.join(download_path, final_filename)
            
            # Avoid duplicate files
            counter = 1
            original_path = file_path
            while os.path.exists(file_path):
                name, ext = os.path.splitext(original_path)
                file_path = f"{name}_({counter}){ext}"
                counter += 1
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(payload)
            
            file_info = {
                'filename': os.path.basename(file_path),
                'file_path': file_path,
                'bank': bank_type,
                'subject': subject,
                'sender': sender,
                'date': date,
                'size': file_size,
                'statement_date': statement_date,
                'download_timestamp': datetime.now().isoformat(),
                'original_filename': filename
            }
            
            self.logger.info(f"💾 Saved: {bank_type} - {os.path.basename(file_path)} ({file_size} bytes)")
            return file_info
            
        except Exception as e:
            self.logger.error(f"❌ Error saving PDF: {str(e)}")
            return None
    
    def extract_pdf_attachments(self, mail: imaplib.IMAP4_SSL, 
                               email_ids: List[bytes]) -> List[Dict[str, Any]]:
        """Extract PDF attachments from emails with progress tracking"""
        pdf_files = []
        total_emails = len(email_ids)
        
        self.logger.info(f"📥 Processing {total_emails} emails for PDF attachments...")
        
        for idx, email_id in enumerate(email_ids, 1):
            try:
                if idx % 10 == 0:  # Progress update every 10 emails
                    self.logger.info(f"Progress: {idx}/{total_emails} emails processed")
                
                # Fetch email
                typ, msg_data = mail.fetch(email_id, '(RFC822)')
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        # Parse email message
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Get email details
                        subject = self.decode_header_value(msg["Subject"])
                        sender = self.decode_header_value(msg.get("From", ""))
                        date = msg.get("Date", "")
                        
                        # Process attachments
                        if msg.is_multipart():
                            for part in msg.walk():
                                if self.is_pdf_attachment(part):
                                    pdf_info = self.save_pdf_attachment(
                                        part, subject, sender, date
                                    )
                                    if pdf_info:
                                        pdf_files.append(pdf_info)
                                        
            except Exception as e:
                self.logger.error(f"❌ Error processing email {email_id}: {str(e)}")
                continue
        
        return pdf_files
    
    def save_summary_report(self, pdf_files: List[Dict[str, Any]], 
                           email_count: int, days_back: int) -> None:
        """Save comprehensive summary report"""
        summary = {
            'process_info': {
                'total_emails_found': email_count,
                'total_pdfs_downloaded': len(pdf_files),
                'download_timestamp': datetime.now().isoformat(),
                'days_searched': days_back,
                'config_used': {
                    'email_address': self.config['email_address'],
                    'imap_server': self.config['imap_server'],
                    'download_folder': self.config['download_folder']
                }
            },
            'bank_breakdown': {},
            'file_details': pdf_files
        }
        
        # Calculate bank-wise breakdown
        for pdf in pdf_files:
            bank = pdf['bank']
            if bank not in summary['bank_breakdown']:
                summary['bank_breakdown'][bank] = {
                    'count': 0,
                    'total_size': 0,
                    'files': []
                }
            summary['bank_breakdown'][bank]['count'] += 1
            summary['bank_breakdown'][bank]['total_size'] += pdf['size']
            summary['bank_breakdown'][bank]['files'].append(pdf['filename'])
        
        # Save summary to multiple formats
        summary_dir = os.path.join(self.config['download_folder'], 'summaries')
        os.makedirs(summary_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON summary
        json_path = os.path.join(summary_dir, f'download_summary_{timestamp}.json')
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # CSV summary for easy analysis
        import csv
        csv_path = os.path.join(summary_dir, f'files_summary_{timestamp}.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            if pdf_files:
                writer = csv.DictWriter(f, fieldnames=pdf_files[0].keys())
                writer.writeheader()
                writer.writerows(pdf_files)
        
        self.logger.info(f"📊 Summary saved: {json_path}")
        self.logger.info(f"📊 CSV report saved: {csv_path}")
    
    def run_complete_fetch(self, days_back: int = 365) -> List[Dict[str, Any]]:
        """Main method to run the complete email fetching process"""
        start_time = datetime.now()
        self.logger.info("🚀 Starting Credit Card Email Fetch Process")
        
        # Validate configuration
        if not self.validate_config():
            self.logger.error("❌ Configuration validation failed!")
            return []
        
        # Connect to email
        mail = self.connect_to_email()
        if not mail:
            return []
        
        try:
            # Search for emails
            email_ids = self.search_credit_card_emails(mail, days_back)
            
            if not email_ids:
                self.logger.info("📭 No credit card emails found")
                return []
            
            # Extract PDFs
            pdf_files = self.extract_pdf_attachments(mail, email_ids)
            
            # Save summary report
            self.save_summary_report(pdf_files, len(email_ids), days_back)
            
            # Final summary
            duration = datetime.now() - start_time
            self.logger.info(f"✅ Process completed in {duration}")
            self.logger.info(f"📊 Results: {len(email_ids)} emails → {len(pdf_files)} PDFs")
            
            # Bank-wise summary
            bank_counts = {}
            for pdf in pdf_files:
                bank = pdf['bank']
                bank_counts[bank] = bank_counts.get(bank, 0) + 1
            
            for bank, count in bank_counts.items():
                self.logger.info(f"🏦 {bank}: {count} files")
            
            return pdf_files
            
        finally:
            # Always close connection
            try:
                mail.close()
                mail.logout()
                self.logger.info("🔐 Email connection closed")
            except:
                pass


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Credit Card Payment History - Email Fetcher"
    )
    parser.add_argument(
        '--config', '-c',
        default='config/email_config.json',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--days', '-d',
        type=int,
        default=365,
        help='Number of days to search back (default: 365)'
    )
    parser.add_argument(
        '--test-connection', '-t',
        action='store_true',
        help='Test email connection only'
    )
    parser.add_argument(
        '--create-config', '-cc',
        action='store_true',
        help='Create default configuration file'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize fetcher
        fetcher = CreditCardEmailFetcher(args.config)
        
        if args.create_config:
            print(f"✅ Configuration file created: {args.config}")
            print("📝 Please update with your email credentials and run again!")
            return
        
        if args.test_connection:
            print("🔌 Testing email connection...")
            if fetcher.validate_config():
                mail = fetcher.connect_to_email()
                if mail:
                    mail.close()
                    mail.logout()
                    print("✅ Email connection test successful!")
                else:
                    print("❌ Email connection test failed!")
            return
        
        # Run the complete process
        print("🚀 Starting Phase 1: Email Fetching")
        print(f"📧 Email: {fetcher.config['email_address']}")
        print(f"📅 Search period: {args.days} days")
        print("=" * 60)
        
        pdf_files = fetcher.run_complete_fetch(args.days)
        
        print("=" * 60)
        print(f"✅ Phase 1 Complete!")
        print(f"📁 Files saved to: {fetcher.config['download_folder']}")
        print(f"📊 Total PDFs downloaded: {len(pdf_files)}")
        
        if pdf_files:
            print("\n🏦 Bank-wise Summary:")
            bank_counts = {}
            for pdf in pdf_files:
                bank = pdf['bank']
                bank_counts[bank] = bank_counts.get(bank, 0) + 1
            
            for bank, count in sorted(bank_counts.items()):
                total_size = sum(pdf['size'] for pdf in pdf_files if pdf['bank'] == bank)
                print(f"   {bank}: {count} files ({total_size/1024/1024:.1f} MB)")
        
        print("\n🎯 Next Steps:")
        print("✅ Phase 1 Complete - Email fetching done!")
        print("📋 Phase 2 - PDF processing and password handling")
        print("📊 Phase 3 - Data extraction and ETL pipeline")
        print("📈 Phase 4 - Dashboard creation")
        
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.getLogger(__name__).exception("Unexpected error occurred")


if __name__ == "__main__":
    main()