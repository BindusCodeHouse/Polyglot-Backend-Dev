# 📘 Dynamic Student Result Management System (Django)

## 🚀 Project Overview

The **Dynamic Student Result Management System** is a Django-based web application designed to simulate a real-life teacher utility tool. It allows teachers to generate student results dynamically based on any number of subjects without using a database.

This project focuses on **core Django concepts**, including template rendering, dynamic form generation, and backend logic handling.

---

## 🎯 Key Features

* ✅ Dynamic form generation based on number of subjects
* ✅ Accepts student details (Name, Standard/Class)
* ✅ Calculates total, percentage, and grade
* ✅ Works for **any number of subjects**
* ✅ No database required (pure logic-based system)
* ✅ Clean and simple UI for easy usage

---

## 🧠 Real-Life Use Case

This system can be used by:

* Teachers to quickly calculate student results
* Schools for basic result processing
* Students for practice and understanding grading systems

---

## 🔄 System Workflow

1. User enters:

   * Student Name
   * Standard/Class
   * Number of Subjects

2. System dynamically generates input fields for marks

3. User enters marks for each subject

4. System calculates:

   * Total Marks
   * Percentage
   * Grade

5. Result is displayed instantly

---

## 🛠️ Technologies Used

* **Backend:** Python, Django
* **Frontend:** HTML, CSS (Basic Styling)
* **Template Engine:** Django Templates

---

## 📂 Project Structure

```
RenderHtmlTemplate/
│
├── myApp/
│   ├── views.py
│   ├── urls.py
    ├── templates/
        ├── home.html
        ├── marks_form.html
        ├── result.html
 ├── myProject/ 
 │   ├── settings.py    
     ├── urls.py  
 ├── manage.py

 ```

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/BindusCodeHouse/Polyglot-Backend-Dev.git
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

* Windows:

```
venv\Scripts\activate
```

* Mac/Linux:

```
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```
pip install django
```

### 5️⃣ Run Server

```
python manage.py runserver
```

### 6️⃣ Open in Browser

```
http://127.0.0.1:8000/
```

---

## 🧮 Grading Logic

| Percentage | Grade    |
| ---------- | -------- |
| ≥ 75       | A        |
| ≥ 60       | B        |
| ≥ 50       | C        |
| < 50       | F (Fail) |

---

## 🔥 Learning Outcomes

This project helps you understand:

* Django views and URL routing
* Template rendering with dynamic data
* Form handling using POST method
* Loop-based dynamic input handling
* Real-world problem solving using backend logic

---

## 🚀 Future Enhancements

* Add subject names instead of just marks
* Add validation (marks ≤ 100)
* Store results using database (Django Models)
* Export result as PDF
* Add login system for teachers
* Convert into REST API

---

## 📌 Author

**Bindu Bhatia**
Backend Developer | Django Learner

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
