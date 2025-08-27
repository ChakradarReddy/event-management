#!/usr/bin/env python3
"""
Test script for certificate generation
This script tests the PDF certificate generation functionality
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db, User, Event, Registration
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    
    print("✅ All imports successful!")
    
    # Test certificate template rendering
    with app.app_context():
        # Create test data
        test_data = {
            'certificate_number': 'CERT-000001',
            'participant_name': 'John Doe',
            'event_title': 'Tech Conference 2024',
            'event_type': 'Conference',
            'event_date': 'December 15, 2024',
            'event_venue': 'Main Auditorium',
            'issue_date': datetime.now().strftime('%B %d, %Y')
        }
        
        # Render template
        from flask import render_template
        certificate_html = render_template('certificate_template.html', **test_data)
        
        print("✅ Template rendering successful!")
        
        # Test PDF generation
        try:
            font_config = FontConfiguration()
            pdf = HTML(string=certificate_html).write_pdf(
                stylesheets=[],
                font_config=font_config
            )
            
            # Save test PDF
            test_pdf_path = 'test_certificate.pdf'
            with open(test_pdf_path, 'wb') as f:
                f.write(pdf)
            
            print(f"✅ PDF generation successful! Test file saved as: {test_pdf_path}")
            
            # Clean up test file
            if os.path.exists(test_pdf_path):
                os.remove(test_pdf_path)
                print("✅ Test file cleaned up")
                
        except Exception as e:
            print(f"❌ PDF generation failed: {str(e)}")
            print("This might be due to missing system dependencies for WeasyPrint")
            print("On macOS, you might need: brew install cairo pango gdk-pixbuf libffi")
            print("On Ubuntu/Debian: sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info")
            
    print("\n🎉 Certificate system test completed!")
    
except ImportError as e:
    print(f"❌ Import error: {str(e)}")
    print("Please install required dependencies:")
    print("pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
    print("Please check your setup and try again")
