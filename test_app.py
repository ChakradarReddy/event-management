#!/usr/bin/env python3
"""
Simple test script for EventHub Flask application
"""

import requests
import time
import sys

def test_flask_app():
    """Test if the Flask application is running and responding"""
    
    print("🚀 Testing EventHub Flask Application...")
    print("=" * 50)
    
    # Test if app is running
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Application is running successfully!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Time: {response.elapsed.total_seconds():.2f}s")
            
            # Check if it's our EventHub app
            if 'EventHub' in response.text:
                print("✅ Confirmed: This is EventHub application")
            else:
                print("⚠️  Warning: Response doesn't contain 'EventHub'")
                
        else:
            print(f"❌ Application responded with status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Application is not running on localhost:5000")
        print("   Please start the application with: python app.py")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Application took too long to respond")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")
    return True

def main():
    """Main function"""
    print("EventHub - College Event Management System")
    print("Test Script")
    print()
    
    success = test_flask_app()
    
    if success:
        print("\n🎉 Application is working correctly!")
        print("   You can now:")
        print("   - Open http://localhost:5000 in your browser")
        print("   - Register as a student or organizer")
        print("   - Create and manage events")
        print("   - Test all functionality")
    else:
        print("\n💥 Application test failed!")
        print("   Please check the error messages above")
        sys.exit(1)

if __name__ == "__main__":
    main()
