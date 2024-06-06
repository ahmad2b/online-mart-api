# Auth Service

This is the Auth Service for the Online Mart API. It handles user authentication, registration, and password management using an event-driven microservices architecture. The service leverages Kafka for inter-service communication and FastAPI for API development.

## Features

- User registration
- User login
- Password recovery and reset
- Event-driven communication using Kafka

## Architecture

The Auth Service is a microservice within the Online Mart API project. It uses Kafka for event-driven communication with other services, such as the User Service. The main components include:

- **FastAPI**: For building the API endpoints.
- **Kafka Producers**: For producing events related to user actions.
- **Kafka Consumers**: For consuming relevant events from other services.

## Technologies

- FastAPI
- SQLModel
- Kafka (AIOKafka)
- Docker
- PostgreSQL

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository**:

```bash
git clone <repo-url>
cd auth-service
```

2. **Create a `.env`** file in the root directory and populate it with the necessary environment variables (see .env.example file).

3. **Build and run the services**:

```bash
docker-compose up --build
```

4. **Access the service**:

The service should now be running on http://localhost:8007.

## API Endpoints

### Auth Routes

- #### Register User

    - **POST** `/api/v1/register`
    - Description: Register a new user.

- #### Login User

    - **POST** `/api/v1/login/access-token`
    - Description: Authenticates a user and returns an access token.

- #### Password Recovery

    - **POST** `/api/v1/password-recovery`
    - Description: Initiates the password recovery process.

- #### Password Reset

    - **POST** `/api/v1/reset-password`
    - Description: Resets the user's password using a reset token.

- #### Test Token (Optional)

    - **POST** `/api/v1/login/test-token`
    - Description: Tests the validity of an access token.

## Kafka Events

### Producers

- User Registered
    - Topic: user_registered
    - Event Data: Details of the newly registered user.

- User Logged In
    - Topic: user_logged_in
    - Event Data: Details of the user who logged in and the authentication token.

- (TODO): Password Reset Requested
    - Topic: password_reset_requested
    - Event Data: Details of the user who requested a password reset.

- (TODO): Password Reset Completed
    - Topic: password_reset_completed
    - Event Data: Details of the user whose password was reset.

### Consumers

- (TODO): User Deactivated
    - Topic: user_deactivated
    - Event Data: Details of the user who was deactivated.

- (TODO): User Updated
    - Topic: user_updated
    - Event Data: Updated details of the user.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.


## License

This project is licensed under the MIT License.