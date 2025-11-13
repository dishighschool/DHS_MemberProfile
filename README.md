# Project Title: dhs-personPage 3.0

## Description
dhs-personPage 3.0 is a comprehensive Flask web application for DisHighSchool member management. It features Discord OAuth authentication, member profile management, tag system, testimonials, and **Discord Bot integration** for automatic tag assignment based on Discord roles. This system provides both a public-facing member showcase and a powerful admin backend.

## Project Structure
```
dhs-personPage
├── app.py                # Entry point for the application
├── config.py             # Configuration settings for the application
├── requirements.txt      # List of required Python packages
├── static                # Static files (CSS, JS, images)
│   ├── css
│   │   └── style.css     # CSS styles for the application
│   ├── js
│   │   └── main.js       # JavaScript for front-end interactions
│   └── images            # Folder for image resources
├── templates             # HTML templates
│   ├── base.html        # Base template for the application
│   ├── home.html        # Home page template
│   └── error.html       # Error page template
├── models                # Data models
│   └── user.py          # User model definition
├── routes                # Application routes
│   ├── __init__.py      # Initializes the routes module
│   └── main.py          # Main route definitions
├── services              # Application services
│   └── __init__.py      # Initializes the services module
├── utils                 # Utility functions
│   └── helpers.py       # Helper functions for the application
├── tests                 # Test cases
│   └── test_app.py      # Application test cases
└── README.md             # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd dhs-personPage
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Features

### Core Features
- **Discord OAuth2 Authentication**: Secure login via Discord
- **Member Profiles**: Customizable profiles with social links, bio, and tags
- **Tag System**: Categorize members with customizable tags
- **Admin Dashboard**: Comprehensive backend for managing users, tags, and content
- **Testimonials**: Member feedback system with approval workflow
- **Public Homepage**: Showcase all active members with filtering capabilities

### 🆕 Discord Bot Integration (New in 3.0)
- **Automatic Tag Assignment**: Assign tags based on Discord server roles
- **Bot Token Configuration**: Easy setup through admin panel
- **Server Selection**: Choose which Discord server to integrate with
- **Role-Tag Mapping**: Map Discord roles to system tags
- **Auto-sync on Registration**: Automatically assign tags when new members register
- **Manual Sync**: One-click sync for existing members (individual or batch)

For detailed Discord Bot setup and usage, see [DISCORD_BOT_GUIDE.md](DISCORD_BOT_GUIDE.md)

## Usage

### Running the Application
```bash
python app.py
```
Visit `http://127.0.0.1:2005` or `http://<server-ip>:2005` in your browser.

### Production Deployment
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

### Database Migration
If upgrading from a previous version, run the Discord Bot migration:
```bash
python migrations/add_discord_tables.py
```

### Testing Discord Integration
To test Discord Bot functionality before configuring in the admin panel:
```bash
python test_discord_integration.py
```
