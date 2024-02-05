# Flask API for Client Management

## Introduction

This Flask API provides a comprehensive system for managing clients, including operations such as creating, reading, updating, and deleting client information. It also features agent registration, login functionality, and JWT-based authentication for secure access to API endpoints.

## Installation

Ensure you have Python and pip installed on your system. Clone this repository to your local machine:

```bash
git clone <repository-url>
cd <repository-folder>
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Setup

Before running the application, you need to set up the database. Use the Flask CLI commands provided:

```bash
flask db_create
flask db_seed  # Optional: to seed the database with initial data
```

## Usage

To start the Flask application, run:

```bash
flask run
```

### Endpoints

- `/` - Test endpoint to verify the API is running.
- `/super_simple` - A simple GET endpoint returning a static message.
- `/clients` - GET all clients in the database.
- `/register` - POST an agent registration.
- `/login` - POST to authenticate an agent and receive an access token.
- `/client_details/<client_id>` - GET details of a specific client by ID.
- `/add_client` - POST a new client (JWT required).
- `/update_client` - PUT to update an existing client's details (JWT required).
- `/remove_client/<client_id>` - DELETE a client by ID (JWT required).

## Contributions

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

Ensure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
