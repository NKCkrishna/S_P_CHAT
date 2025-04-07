import ee
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

def authenticate_gee(project_id=None):
    try:
        print("🔐 Starting Google Earth Engine authentication...")
        ee.Authenticate()
        print("✅ Authentication successful!")
        print("\nNow initializing Earth Engine...")
        if project_id:
            ee.Initialize(project=project_id)
        else:
            ee.Initialize()
        print("✅ Earth Engine initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error during authentication: {str(e)}")
        print("\nPlease make sure you have:")
        print("1. Signed up for Google Earth Engine at https://earthengine.google.com/")
        print("2. Created a Google Cloud Project")
        print("3. Enabled the Earth Engine API for your project")
        print("\nIf you have a project ID, you can run this script with:")
        print("python authenticate_gee.py YOUR_PROJECT_ID")
        return False

if __name__ == "__main__":
    import sys
    project_id = sys.argv[1] if len(sys.argv) > 1 else None
    authenticate_gee(project_id) 