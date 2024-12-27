"""
Main server file which will be used to run the server
"""

from app import create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
