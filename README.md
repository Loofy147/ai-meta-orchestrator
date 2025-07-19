# Project Title

A brief description of what this project does and who it's for.

## Project Structure

The project is organized into the following directories:

- `src/orchestrator`: Contains the backend Flask application.
- `src/services/frontend`: Contains the frontend vanilla JavaScript application.
- `.github/workflows`: Contains the CI/CD pipeline configuration.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Installing and Running

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd your-repository
    ```
3.  Build and run the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

The frontend will be available at `http://localhost:80` and the backend at `http://localhost:5000`.

## Running the tests

### Backend Tests

To run the backend tests, run the following command from the root of the project:

```bash
docker-compose exec orchestrator pytest
```

### Frontend Tests

To run the frontend tests, run the following command from the root of the project:

```bash
docker-compose exec frontend npm test
```

## Built With

*   [Flask](https://flask.palletsprojects.com/) - The web framework used for the backend.
*   [Vanilla JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Used for the frontend.
*   [Docker](https://www.docker.com/) - Containerization platform.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your-username/your-repository/tags).

## Authors

*   **Your Name** - *Initial work* - [your-username](https://github.com/your-username)

See also the list of [contributors](https://github.com/your-username/your-repository/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
