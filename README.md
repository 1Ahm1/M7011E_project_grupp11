# Project Information

## Course Details

- **Course Name:** Dynamic Web Systems (M7011E)
- **Instructor:** Sandeep Patil
- **Semester/Year:** LP2/2023

## Project Team

### Students

1. **Ahmad Allahham**
   - **Email:** ahmall-0@student.ltu.se

2. **Arian Asghari**
   - **Email:** ariasg-0@student.ltu.se

# Requirements

## Project Overview

This project focuses on creating a dynamic web system using modern technologies. It emphasizes client-server communication, secure user information handling, and an intuitive user interface. The application will be developed with Python (FastAPI framework) for the backend, Angular for the frontend, and MySQL as the relational database.

## Objectives

- Build a dynamic web system with a client-server architecture.
- Develop a secure authentication and authorization system.
- Implement CRUD operations through APIs for database interactions.
- Integrate third-party packages to enhance functionality.
- Demonstrate an understanding of ethical considerations related to sensitive user data.
- Model, simulate, predict, and evaluate the web system's performance.

## Setup Instructions

### MySQL Installation

- Download and install MySQL from the [official MySQL Installer](https://dev.mysql.com/downloads/installer/).
- Add MySQL to the system's PATH variables during installation.

### Python Installation

- Download and install the latest version of Python from [Python Downloads](https://www.python.org/downloads/).
- Add Python to the system's PATH variables during installation.

### Backend Requirements

1. Navigate to the Fastapi-project1 subdirectory within the project directory:
    ```bash
    cd [project-directory]/Fastapi-project1
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Node.js Installation

- Download and install Node.js from [Node.js Downloads](https://nodejs.org/en/download/).

### Angular Installation

- Install the Angular CLI globally using the following command:
    ```bash
    npm install -g @angular/cli
    ```

- Navigate to the library-front subdirectory within the project directory:
    ```bash
    cd [project-directory]/library-front
    ```

- Install the necessary Node.js packages:
    ```bash
    npm install
    ```

## Code Structure

The project is organized to maintain a clean and modular codebase. Below is an overview of the project's structure:

## Project Directory

- **Fastapi-project1:** Contains the FastAPI backend code, handling server-side logic, API endpoints, and database interactions.

- **library-front:** Houses the Angular frontend code, responsible for the user interface and client-side interactions.

### Backend Structure

The backend is structured to separate concerns and enhance maintainability.

- **main.py:** Main entry point for the FastAPI application, including configurations and settings.

- **domain:** Contains domain-specific logic, organized into subdirectories:

  - **user:** Manages user-related functionality, including authentication, authorization, and profile management.

  - **utils:** Includes utility functions, communication modules, and configuration settings used throughout the backend.

  - **enums.py:** Enumerations for maintaining constants and predefined values.

  - **communication.py:** Handles communication tasks, such as sending emails and notifications.

  - **configs.py:** Centralized configuration settings for the application.

  - **general.py:** Houses general utility functions and common functionalities.

- **tests:** Contains unit tests and integration tests.

### Frontend Structure

The frontend follows Angular's best practices for maintainability and scalability.

- **src:** Contains the source code for the Angular application.

  - **app:** Main application module orchestrating different components.

  - **components:** Directory for organizing reusable UI components.

  - **services:** Houses Angular services responsible for communication with the backend.

  - **views:** Contains the views or pages of the application.

  - **assets:** Holds static assets like images, stylesheets, and other resources.

  - **environments:** Configuration files for different environments.

- **angular.json:** Configuration file for Angular CLI settings.

- **package.json:** NPM package configuration file.

### Additional Notes

- **diagrams.pdf:** Includes diagrams illustrating the architecture and relationships between different components.

- **run.bat:** A script to automate the setup and execution processes, making it convenient to run the entire project locally.

Feel free to explore each directory for more detailed information and comments within the code files.

## Run Project

Execute the project by double-clicking on the provided run batch file. The script automates the following processes:

1. Creation of the database with initial data.
2. Launching the app server with Python.
3. Launching the website.

**Note:** Adjust the `[project-directory]` placeholder with the actual path as needed.
