import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') = 'db24c608640f5034b30b8e1e1eb5618ed0ffdbf5'
    MONGO_URI = os.environ.get('MONGO_URI') = 'mongodb+srv://yogeshnade34:Iiitsuratcs51yn@cluster0.rfz6m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    
    # API Keys
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or "ebde2f3c54a9426abb4bb84becd4c61d"
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY') or "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"
    
    # Email Configuration (for future implementation)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@codejurist.com'