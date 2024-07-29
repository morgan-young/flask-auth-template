# Equipped Powerlifting App

This application is designed to help powerlifters log their workouts, track equipment usage, and manage their configurations. Built with Flask and PostgreSQL, it provides a robust backend to support user authentication and data management.

## Features

- User registration and authentication
- Logging workouts and exercises
- Managing equipment and logging reps in equipment
- Viewing user-specific data
- Configurable options for powerlifting preferences

## Technologies Used

- Flask
- Flask-Login
- Flask-SQLAlchemy
- PostgreSQL
- AWS SSM Parameter Store for configuration management

## Setup

(You must have the serverless framework installed to deploy this)

1. Clone the repository:

```sh
git clone https://github.com/your-repo/equipped-powerlifting-app.git
cd equipped-powerlifting-app
```

2. Install the required Python packages:

```sh
poetry install
```

3. Set up environment variables and configuration using AWS SSM Parameter Store:

Ensure you have the necessary parameters set in SSM Parameter Store:
- `/equipped-powerlifting-app/user-authentication-key`
- `/equipped-powerlifting-app/{STAGE}/database-uri`

4. Run the application:

```sh
sls deploy
```

## API Endpoints

### User Management

- `POST /register`: Register a new user
- `POST /login`: Log in an existing user
- `GET /logout`: Log out the current user

### Workout Logging

- `POST /log_set`: Log a new set
- `GET /list_workouts`: List all workouts for the current user

### Equipment Management

- `POST /add-equipment`: Add new equipment
- `POST /log-reps-in-equipment`: Log repetitions in a specific piece of equipment
- `GET /view-equipment`: View all equipment for the current user

## Error Handling

The application includes robust error handling and logging to help diagnose issues. Errors are returned as JSON responses with appropriate HTTP status codes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.