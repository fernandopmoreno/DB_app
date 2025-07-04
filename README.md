# DB_app

This project is a Python-based data management and migration application designed to facilitate the import, export, and manipulation of information in a Supabase database. It includes a graphical interface developed with Tkinter and utilities for working with CSV and Excel files.

## Features

- **Data import** from Excel files (`.xlsx`, `.xls`) and CSV.
- **Export of database tables** to CSV files.
- **Graphical interface** with Tkinter.
- **Integration with Supabase** for data storage and queries.
- **Generation of fake data** for testing and demonstrations.
- **Data migration and transformation** with pandas.

## Project Structure

```
DB_app/
│
├── csv/                  # Storage for .csv data
├── doc/                  # Storage for Word documents
├── excel/                # Storage for .xlsx, .xls data
├── fonts/                # Font files
├── images/               # Images used
├── pdfs/                 # Storage for PDFs
├── sql/                  # .sql files for database table creation
├── tables/               # Exported table data
├── app.py                # Main application interface
├── aux_functions.py      # Auxiliary functions
├── listados.py           # Functions for dumping data to files
├── main.py               # Main application entry point
├── migration.py          # Data import and export functions
├── models.py             # User model for the database
├── orders.py             # Filter structuring
├── pdf.py                # PDF class modification
├── export.py             # Functions for exporting data to CSV
├── requirements.txt      # Project dependencies
├── tolltip.py            # Modification of Tkinter's TollTip class
└── users_generator.py    # Fake data generation
```

## Installation

0. **Pre-requirements**
    - Install Docker

1. **Clone the repository:**
    ```bash
    git clone [repository_URL]
    cd DB_app
    ```

2. **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate #source venv/bin/activate for linux
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Supabase:**
    ```bash
    git clone --depth 1 https://github.com/supabase/supabase
    cd supabase/docker
    copy .env.example .env #cp .env.example .env for linux
    docker compose up -d
    ```

5. **Database setup:**
    - Go to http://localhost:8000  
        ```bash
        User: supabase
        Password: this_password_is_insecure_and_should_be_updated
        ```
    - In the SQL Editor section, execute the SQL statements found in the file `sql/create_tables.sql` to create the tables.
    - In the Authentication section, create a new user. Example:
        ```bash
        Email adress: admin@admin.com
        User Password: admin1234
        ```

## Usage

1. Back to the main folder run the main application:
    ```bash
    python main.py
    ```

2. Login with the user created in the previous step.

3. Use the graphical interface to import, export, and manage data.

## Notes

- The included data files (`csv/`, `excel/`, `tables/`) contain **randomly generated fake data** and are for testing and demonstration purposes only.
- The application uses environment variables for database connection (the `.env` file is not included in the repository).
- To stop containers
    ```bash
    cd supabase/docker
    docker composer down --volumes
    ```

## License

This project **does not have a usage license**.  
The source code is published solely for consultation and display in the portfolio of Fernando Peñate Moreno.  
**Copying, modifying, distributing, or using this code for any purpose without the express authorization of the author is not permitted.**

---

**Developed by:** Fernando Peñate Moreno
