# KitabKendra

KitabKendra is a Library Management System web application project designed to efficiently manage library resources. It facilitates tasks such as adding, removing, and editing books and sections within the library. Users can easily search for books and make requests through the application's intuitive interface.

**Note:** This is a project and not the end product. It serves as a demonstration of the capabilities and features of a library management system.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Project Contributions](#project-contributions)
- [Contact](#contact)

## Features

- **User Authentication**: Implemented secure user authentication using Flask-Login.
- **CRUD Operations**: Enabled administrators to perform CRUD operations on books and sections for effective management.
- **Search Functionality**: Provided users with robust search capabilities to find books based on various criteria.
- **Request Management**: Facilitated users in making book requests and managed these requests efficiently.
- **Admin and User Dashboards**: Separate dashboards for admins and users, with the first registered user being assigned admin privileges.
- **Admin Functionality**: Admins have the ability to manage the entire library system, including adding, removing, and editing books and sections, approving or denying book requests, and managing user accounts.
- **API Endpoints**: Exposed RESTful API endpoints for interacting with the library's resources programmatically.



## Technologies Used

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-RESTful
- **Frontend**: HTML/CSS, Bootstrap
- **Database**: SQLite

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Zephyrr4/kitabKendra.git
    ```
2. Navigate to the project directory:
    ```bash
    cd kitabKendra
    ```
3. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Set up the database:
   ```bash
   python initialize_db.py
   ```
7. Run the application:
    ```bash
    python app.py
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:5000/`
2. Register a new user. The first registered user will be assigned admin privileges.
3. Admin users can access the admin dashboard to manage books and sections, while regular users can access the user dashboard to browse and request books.

## API Endpoints

KitabKendra exposes a RESTful API for interacting with the library's resources. Below are the available endpoints:

### Book Endpoints

- **[GET] /api/book/{book_id}**
  - Retrieve details of a specific book by its ID.

- **[PUT] /api/book/{book_id}**
  - Update details of a specific book.

- **[DELETE] /api/book/{book_id}**
  - Delete a specific book from the database.

- **[POST] /api/book**
  - Add a new book to the database.

### Section Endpoints

- **[GET] /api/section/{section_id}**
  - Retrieve details of a specific section by its ID.

- **[PUT] /api/section/{section_id}**
  - Update details of a specific section.

- **[DELETE] /api/section/{section_id}**
  - Delete a specific section from the database.

- **[POST] /api/section**
  - Add a new section to the database.

### User Endpoints

- **[GET] /api/user/{user_id}**
  - Retrieve details of a specific user by their ID.

## Screenshots

Here are some screenshots of the KitabKendra application to give you a visual overview of its interface:

![Login Screen](screenshots/Login_screen.png)
![User Dashboard](screenshots/User_Dashboard.png)
![Admin Dashboard](screenshots/Admin_Dashboard.png)

## Project Contributions

I contributed to both frontend and backend development. On the frontend, I designed and implemented the user interface using HTML/CSS and Bootstrap, ensuring a intuitive design. For the backend, I leveraged Flask and Flask-SQLAlchemy to manage data and interactions with the SQLite database. This approach ensured seamless integration and smooth functionality across the application.



## Contact

If you have any questions or suggestions, feel free to reach out.

- **Email**: itsmepawan.jh@gmail.com
- **GitHub**: [epawan](https://github.com/epawan)

---

Thank you !
