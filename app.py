# run.py
 # Ensure 'project' is a valid Python package and contains 'app'
from app.routes import app   # Import the Flask app instance
if __name__ == '__main__':
    # Debug=True allows auto-reloading during development
    # Turn off Debug=True for production deployment
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error occurred while running the app: {e}")