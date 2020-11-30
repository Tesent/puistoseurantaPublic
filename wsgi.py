# Entry point to the application
from app import create_app

if __name__ == "__main__":
    application = app.create_app();
    application.run()
