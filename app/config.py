import os


class Config:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'mysql+pymysql://myuser:mypassword@localhost:3306/disaster_alert_db')
