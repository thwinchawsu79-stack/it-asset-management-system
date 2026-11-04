IT Asset Management System

1. Project Overview

The IT Asset Management System is a Python-based application designed to manage and track IT equipment.

The system helps users maintain asset records, monitor equipment status, manage employee assignments, and generate asset reports.

This project is developed as a practical learning project to demonstrate programming, data management, and IT asset administration skills.

2. Technologies Used

- Python – Application development
- JSON – Asset data storage
- CSV – Asset report export
- Unittest – Automated testing
- Git – Version control
- GitHub – Online source code management and project hosting

3. Key Features

- Register new IT assets
- View all registered assets
- Search assets by ID
- Update asset information and status
- Delete asset records
- Filter assets by category
- Assign assets to employees
- Unassign and return assets
- Generate asset summaries
- Export asset records to CSV
- Store asset data in JSON format
- Automated testing using Python Unittest

4. Asset Categories

- Laptop
- Desktop
- Monitor
- Printer
- Network Equipment
- Other

5. Asset Status

- Available
- In Use
- Under Maintenance
- Retired

6. Project Structure

it-asset-management-system/
│
├── main.py
├── asset_functions.py
├── assets.json
├── test_itams.py
├── asset_export.csv
├── README.md
└── .gitignore

7. How to Run the Project

1. Install Python 3.
1. Clone or download the project.
1. Open the project folder in VS Code.
1. Run the application:

python main.py

8. How to Run Tests

Execute the following command:

python -m unittest test_itams.py -v

9. Learning Objectives

Through this project, I aim to develop practical skills in:

- Python programming
- IT asset management
- Data storage and file handling
- Automated software testing
- Version control with Git
- Project management using GitHub

10. Project Status

Currently developed features include asset registration, searching, updating, deletion, assignment management, reporting, CSV export, and automated testing.

Git and GitHub integration will be completed as part of the project development process.

Testing Results

The application has been tested using Python's Unittest framework.

- Total automated tests: 20
- Test result: All tests passed
- Tested functionality includes asset registration, searching, updating, deletion, assignment, and status management.
