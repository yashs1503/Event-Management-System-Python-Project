# Event Management System (Python)

## 📌 Project Overview

The **Event Management System** is a console-based Python application designed to manage events efficiently.
It allows **Admins**, **Organizers**, and **Participants** to interact with the system and perform different operations such as creating events, managing participants, registering for events, and providing feedback.

This project demonstrates **Object-Oriented Programming (OOP)** concepts, **file handling**, and **modular programming in Python**.

---

## 🚀 Features

### 👨‍💼 Admin

* Secure admin login
* Add new events
* View available events
* Delete events
* Add event organizers
* View organizer details
* Assign organizers to events

### 🧑‍💻 Organizer

* Organizer authentication
* Manage assigned events
* Add participants to events
* View participants of events
* Update event details

### 👤 Participant

* View available events
* Register for events
* Cancel event registration
* View personal registrations
* Payment simulation (Cash/Card)
* Submit feedback for events

---

## 🛠 Technologies Used

* **Python**
* **JSON** (for data storage)
* **File Handling**
* **Object-Oriented Programming (OOP)**

Python Standard Libraries Used:

* `json`
* `getpass`



## 📂 Project Structure

---

event-management-system/
│
├── main.py
├── admin.py
├── organizer.py
├── participant.py
│
├── data/
│   ├── events.json
│   ├── organizers.json
│   ├── participants.json
│   └── registrations.json
│
├── feedback.txt
└── README.md

---

## ⚙️ How the System Works

1. The program starts from **main.py**.
2. The user selects one of the roles:

   * Admin
   * Organizer
   * Participant
3. Based on the role, different functionalities become available.

---

## 🔐 Default Admin Login

---

Username: admin
Password: 1234

---

## 💳 Payment Simulation

Participants can register for events using:

* **Cash Payment**
* **Card Payment (Dummy Validation)**

This simulates a simple payment workflow.

---

## 📊 Data Storage

The system stores data using **JSON files**.

* `events.json` → Stores event information
* `organizers.json` → Stores organizer details
* `participants.json` → Stores participant records
* `registrations.json` → Stores event registrations

---

## 📈 Learning Outcomes

This project helped practice:

* Python modular programming
* Object-Oriented Programming
* JSON data storage
* Console-based UI design
* Input validation
* File handling

---

## 👨‍💻 Author

**Yash Sawant**



