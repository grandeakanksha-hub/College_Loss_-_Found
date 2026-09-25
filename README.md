# Campus Lost & Found System

A web-based **Campus Lost & Found System** developed using **Python Flask**, **SQLite**, **Bootstrap 5**, **HTML**, **CSS**, and **JavaScript**. The system helps students and staff report lost or found items, upload images, search items, submit claim requests, and manage item status through an admin dashboard.

---

## Features

* User Registration & Login
* Secure session-based authentication
* Report Lost Item with image upload
* Report Found Item with image upload
* Browse all lost and found items
* Search and filter items
* Submit claim requests
* Update item status (Lost, Found, Claimed)
* Admin management dashboard
* Responsive Bootstrap user interface

---

## Tech Stack

| Technology  | Purpose                  |
| ----------- | ------------------------ |
| Python      | Backend programming      |
| Flask       | Web framework            |
| SQLite      | Database                 |
| HTML5       | Web page structure       |
| CSS3        | Styling                  |
| Bootstrap 5 | Responsive UI            |
| JavaScript  | Client-side interactions |
| Jinja2      | Dynamic templates        |

---

## Project Structure

campus_lost_found/

├── app.py

├── database.db

├── uploads/

│ └── (Uploaded item images)

├── static/

│ ├── css/

│ │ └── style.css

│ ├── js/

│ │ └── script.js

│ └── uploads/

├── templates/

│ ├── login.html

│ ├── register.html

│ ├── dashboard.html

│ ├── browse_items.html

│ ├── report_lost.html

│ ├── report_found.html

│ └── claim_item.html

└── README.md

---

## Database Schema

### Users Table

* **id** – INTEGER (Primary Key)
* **name** – TEXT
* **email** – TEXT (Unique)
* **password** – TEXT

### Items Table

* **id** – INTEGER (Primary Key)
* **title** – TEXT
* **description** – TEXT
* **category** – TEXT
* **location** – TEXT
* **date** – TEXT
* **status** – TEXT (Lost / Found / Claimed)
* **image** – TEXT
* **reported_by** – TEXT

### Claims Table

* **id** – INTEGER (Primary Key)
* **item_id** – INTEGER
* **claimer_name** – TEXT
* **contact** – TEXT
* **message** – TEXT

---

## Installation

1. Download or clone the project.
2. Open the folder in VS Code.
3. Install Flask using pip.
4. Run the project with `python app.py`.
5. Open your browser and visit `http://127.0.0.1:5000`.

---

## How to Use

1. Register a new account.
2. Log in to the system.
3. Open the dashboard.
4. Report a lost or found item with details and an image.
5. Browse all available items.
6. Use search and filters to find matching items.
7. Submit a claim request if an item belongs to you.
8. Admin can verify and update the item status to Claimed.

---

## Modules

* Login
* Register
* Dashboard
* Report Lost Item
* Report Found Item
* Browse Items
* Search & Filter
* Claim Request
* Admin Management

---

## CRUD Operations

**Create:** Report new lost or found items.

**Read:** View and search all reported items.

**Update:** Edit item details and update status.

**Delete:** Remove incorrect or resolved records.

---

## Future Enhancements

* Email notifications for claim approval
* QR code-based item identification
* Multiple image upload
* Real-time search
* Role-based access (Student & Admin)
* AI image matching for similar items

---

## Author

**Grande Akanksha**

B.Tech – Computer Science & Engineering

Sri Mittapalli College of Engineering

---

## License

This project is developed for **academic and educational purposes only**.
