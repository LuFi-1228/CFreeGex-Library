# 📘 Project README

## 🚀 Overview
This project provides an interactive web interface for parsing PDOp expressions, converting them into NPDAs, exporting XML representations, and executing simulations.  
You can run the application **locally without Docker**, or **using Docker Compose** if you prefer containerized execution.

---

# 📦 1. Running Without Docker

## 1.1 Requirements
Ensure you have:
- Python 3.10+
- pip
- virtualenv (optional but recommended)

## 1.2 Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate       # Windows
```

## 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

## 1.4 Run the Application
```bash
python app.py
```

Access the interface at:
```
http://127.0.0.1:5000/
```

---

# 🐳 2. Running With Docker Compose

## 2.1 Start the Application
```bash
docker-compose up --build
```

Access at:
```
http://localhost:5000/
```

## 2.2 Detached Mode
```bash
docker-compose up -d
```

## 2.3 Stop Containers
```bash
docker-compose down
```

---

# 🔧 3. Folder Structure
```
.
├── app.py
├── requirements.txt
├── static/
├── templates/
├── pdop/
│   ├── parser/
│   ├── converter/
│   ├── simulator/
│   ├── utils/
└── docker-compose.yml
```

---

# 📚 4. Documentation
Documentation is available in `/docs` or online if deployed.

---

# 🤝 5. Contributing
Pull requests and issues are welcome.

---

# 📄 6. License
This project is licensed under the chosen open-source model.
