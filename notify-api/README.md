# Notify API

This project is a Django-based API that sends notifications to the admin via email or SMS when a failure occurs. 

## Project Structure

```
notify-api
├── notify
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── apps
│       ├── __init__.py
│       └── notifications
│           ├── __init__.py
│           ├── admin.py
│           ├── apps.py
│           ├── models.py
│           ├── tests.py
│           ├── views.py
│           └── utils
│               ├── __init__.py
│               ├── email_sender.py
│               └── sms_sender.py
├── manage.py
└── README.md
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd notify-api
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```
   python manage.py migrate
   ```

5. **Start the development server**:
   ```
   python manage.py runserver
   ```

## Usage

- The API will listen for failure events and trigger notifications to the admin.
- Configure email and SMS settings in `settings.py` to enable notifications.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.