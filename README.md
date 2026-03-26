# Learning Log

![Tests](https://github.com/rongonzalez/learning_log/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)

## Overview

**Learning Log** is a Django web application that allows users to create topics and record entries about what they are learning.

This project demonstrates professional software engineering practices, including automated testing, continuous integration, and maintainable test architecture using factories.

The application evolved from a learning exercise into a production-style project showcasing:

* Django web development
* Automated testing with pytest
* Test data factories using factory_boy
* Continuous Integration using GitHub Actions
* High test coverage and safe refactoring practices

---

## Features

* User registration and authentication
* Create, edit, and delete learning topics
* Create, edit, and delete entries
* Authorization checks to protect user data
* Automated test suite
* Continuous Integration pipeline
* Factory-based test data generation
* High code coverage (99%)

---

## Tech Stack

* **Python 3.12**
* **Django**
* **pytest**
* **factory_boy**
* **pytest-django**
* **coverage.py**
* **GitHub Actions**
* **SQLite**

---

## Project Structure

```
learning_log/
├── learning_logs/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── users/
│   ├── views.py
│   └── urls.py
│
├── tests/
│   ├── factories.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_topics.py
│   ├── test_views.py
│   └── test_user_views.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/rongonzalez/learning_log.git
cd learning_log
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Create a superuser (optional):

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Then open:

```
http://127.0.0.1:8000
```

---

## Running Tests

Run the full test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov
```

Example output:

```
23 passed
Coverage: 99%
```

---

## Continuous Integration

This project uses **GitHub Actions** to automatically run tests on every push.

The CI pipeline:

* Installs dependencies
* Runs pytest
* Generates coverage
* Fails the build if tests fail

Workflow file:

```
.github/workflows/tests.yml
```

---

## Test Architecture

The test suite follows a production-style structure using factories and fixtures.

### Factories

Test data is generated using:

* UserFactory
* TopicFactory
* EntryFactory

Defined in:

```
tests/factories.py
```

Factories allow tests to be written concisely and consistently.

Example:

```python
entry = EntryFactory()
```

Instead of:

```python
user = User.objects.create_user(...)
topic = Topic.objects.create(...)
entry = Entry.objects.create(...)
```

---

## Security and Authorization Testing

The application includes tests that verify:

* Users cannot access other users' data
* Users cannot edit or delete unauthorized entries
* Login protection is enforced
* Proper HTTP responses are returned

These tests help ensure safe multi-user behavior.

---

## Development Workflow

This project uses a safe, incremental development process:

```
Write test
Run pytest
Commit changes
Push to GitHub
Verify CI passes
```

This workflow ensures reliability and prevents regressions.

---

## Example Commands

Run development server:

```bash
python manage.py runserver
```

Run migrations:

```bash
python manage.py migrate
```

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov
```

---

## Future Enhancements

Potential next steps for the project:

* Parameterized test scenarios
* API endpoints
* Playwright UI automation
* Docker containerization
* Cloud deployment
* Performance testing
* Test data seeding utilities

---

## Release History

Releases listed in chronological order (oldest to newest).

## v1.0.0 — Core Application Foundation

Established the initial Django Learning Log application with authenticated user workflows, automated testing, and continuous integration to support reliable development and deployment practices.

Features:

Core Django application structure with Topics and Entries models

User authentication and registration workflows

User-specific data ownership and access control

Template-based UI for creating and viewing learning logs

Initial pytest test suite for application behavior

GitHub Actions CI pipeline for automated test execution

Structured repository layout supporting maintainable development

Version-controlled release workflow using Git tags

Baseline production-ready CRUD functionality

~99% test coverage established

## v1.1.0 — Pagination Feature

Added pagination support to improve usability when viewing large numbers of entries and to ensure consistent performance as datasets grow.

Features:

Entry pagination on topic detail page

Configurable page size for result sets

Navigation controls (Next / Previous)

Consistent handling of paginated query results

pytest validation for pagination behavior

CI pipeline validation for pagination workflows

Maintained stable user experience for large datasets

~99% test coverage maintained

## v1.2.0 — Delete Workflow

Implemented a safe and controlled delete workflow to protect user data and prevent accidental record removal.

Features:

Delete entry confirmation page

POST-only delete enforcement for safe operations

Cancel navigation support for user recovery

Authorization protection for delete operations

Ownership validation before deletion

pytest validation for delete workflow behavior

CI pipeline validation for delete functionality

Improved user safety and workflow reliability

~99% test coverage maintained

## v1.3.0 — REST API Integration

Introduced a secure REST API using Django REST Framework to support programmatic access, automation workflows, and future system integrations.

Features:

Django REST Framework (DRF) integration

REST API endpoints for Topics and Entries

Full CRUD operations via API

Authentication required for all API endpoints

User ownership filtering and data isolation

Server-side ownership assignment on create

Permission validation for update and delete operations

JSON-based request and response handling

pytest API test suite for endpoint validation

CI pipeline validation for API functionality

Established foundation for automation and external integrations

~99% test coverage maintained

## v1.4.0 — Search, Filtering, and Ordering Support

Enhanced the REST API with flexible query capabilities to improve data retrieval, usability, and scalability. This release introduces production-style query patterns commonly used in modern APIs and strengthens the system’s operational maturity.

Features:

Search filtering for Topics and Entries using query parameters

Field-based filtering to retrieve records by related data

Ordering support to control result sorting using API query parameters

Pagination compatibility with search and filtering operations

Token authentication for secure API access

Session authentication support for browser-based usage

User ownership authorization enforcement for all API queries

Consistent response behavior across filtered and ordered datasets

pytest validation for search, filtering, and ordering functionality

Negative test coverage for authentication and authorization enforcement

CI pipeline validation for query behavior and security rules

Stable versioned release with rollback capability via Git tags

Clean repository state with merged feature branches

Maintained disciplined development workflow

~99% test coverage maintained

Supported Query Patterns:

GET /api/topics/?search=python

GET /api/entries/?topic=3

GET /api/topics/?ordering=date_added

GET /api/topics/?ordering=-date_added

GET /api/topics/?search=django&ordering=date_added

Security:

IsAuthenticated enforcement for all API endpoints

Ownership-based data filtering to ensure users access only their own records

Token authentication validation for API clients

Authorization checks for update and delete operations

Protection against unauthorized data exposure

Testing:

Search functionality tests

Filtering behavior tests

Ordering validation tests

Authentication enforcement tests

Authorization protection tests

Negative behavior tests for invalid query scenarios

All tests passing in local and CI environments

Operational Impact:

Expanded API usability for real-world data retrieval scenarios

Improved developer and automation workflow support

Strengthened production readiness and reliability

Maintained disciplined release and version control practices

Established foundation for future automation and performance enhancements

## Author

Ron Gonzalez

---

## License

This project is for educational and portfolio purposes.
