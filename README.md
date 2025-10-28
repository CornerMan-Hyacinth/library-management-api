# 📚 Library Management System (FastAPI)

A simple yet powerful backend API for managing library operations — built with FastAPI and SQLAlchemy.
This system allows adding and managing books, readers, and categories, as well as handling book borrowing and returns.

## 🚀 Features

- ### 📘 Books Management
  - Add, view, update, delete, and search books
  - Track availability (available / borrowed)
- ### 🗂 Categories
  - Create and manage book categories
- ### 👤 Readers
  - Register and manage library readers
- ### 🔄 Borrowing System
  - Record book borrow and return actions
  - Automatically mark books as unavailable when borrowed

## 🏗️ Tech Stack

| Component          | Technology                                    |
| :----------------- | :-------------------------------------------- |
| Framework          | FastAPI                                       |
| Database           | SQLite (development), PostgreSQL (production) |
| ORM                | SQLAlchemy                                    |
| Schema Validation  | Pydantic                                      |
| Migrations         | Alembic                                       |
| Environment Config | python-dotenv                                 |
| Testing            | Pytest                                        |

## ⚙️ Installation & Setup

1. **Clone the Repository**

```bash
git clone https://github.com/CornerMan-Hyacinth/library-management-api.git
cd library-management-api
```

2. **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**
   Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./library.db
```

5. **Run Database Migrations**

```bash
alembic upgrade head
```

6. **Start the Server**

```bash
uvicorn app.main:app --reload
```

Server will be running at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

7. **Access the Interactive Docs**

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🔍 API Endpoints Overview

### Books

| Method   | Endpoint                     | Description      |
| :------- | :--------------------------- | :--------------- |
| `GET`    | `/books`                     | List all books   |
| `POST`   | `/books`                     | Add new book     |
| `GET`    | `/books/{id}`                | Get book details |
| `PUT`    | `/books/{id}`                | Update a book    |
| `DELETE` | `/books/{id}`                | Delete a book    |
| `GET`    | `/books/search?query=python` | Search books     |

### Categories

| Method | Endpoint      | Description     |
| :----- | :------------ | :-------------- |
| `GET`  | `/categories` | List categories |
| `POST` | `/categories` | Add category    |

### Readers

| Method | Endpoint   | Description  |
| :----- | :--------- | :----------- |
| `GET`  | `/readers` | List readers |
| `POST` | `/readers` | Add reader   |

### Borrowing

| Method | Endpoint              | Description          |
| :----- | :-------------------- | :------------------- |
| `POST` | `/borrow`             | Borrow a book        |
| `PUT`  | `/borrow/{id}/return` | Return borrowed book |

## 🧠 Future Improvements

- 🔒 Authentication & authorization (JWT)
- 📅 Borrowing due dates and reminders
- 📊 Admin dashboard with analytics

## 🤝 Contributing

Contributions are welcome!
If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to your branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 🧾 License

This project is licensed under the MIT License.
