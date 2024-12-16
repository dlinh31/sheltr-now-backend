from app import create_app, db
import os
from dotenv import load_dotenv

app = create_app()
load_dotenv(dotenv_path="./.env")
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")
    app.run(host=os.getenv("FLASK_RUN_HOST", "0.0.0.0"), port=int(os.getenv("FLASK_RUN_PORT", 5000)), debug=os.getenv("DEBUG", "False") == "True")
