def format_date(date):
    """Format a date object into a string."""
    return date.strftime("%Y-%m-%d")

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    import random
    import string
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def validate_email(email):
    """Validate an email address."""
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def calculate_age(birthdate):
    """Calculate age from birthdate."""
    from datetime import datetime
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age