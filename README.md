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

The project is organized into the following directories and files:

### Source Code (`.py` files)

-   `main.py`: The main entry point to launch the application.
-   `app.py`: Defines the main Tkinter GUI, its layout, and event handling.
-   `migration.py`: Contains functions for importing and exporting data between the database and local files.
-   `export.py`: Handles the logic for exporting database tables to CSV format.
-   `listados.py`: Manages the generation of various data listings and reports.
-   `pdf.py`: Custom modifications or extensions for PDF generation functionalities.
-   `users_generator.py`: A utility for generating fake user data for testing purposes.
-   `aux_functions.py`: A collection of helper and utility functions used across the application.
-   `models.py`: Defines the data models, likely for database interaction (e.g., User model).
-   `orders.py`: Manages the structuring and filtering of data orders or queries.
-   `tolltip.py`: A custom modification of the Tkinter Tooltip class for enhanced UI feedback.

### Data and Asset Directories

-   `csv/`: Default directory for storing and reading CSV data files.
-   `doc/`: Storage for generated Word documents.
-   `excel/`: Default directory for storing and reading Excel files (`.xlsx`, `.xls`).
-   `fonts/`: Contains font files used by the application (e.g., for PDF generation).
-   `images/`: Stores images used within the application's GUI.
-   `pdfs/`: Default directory for storing generated PDF files.
-   `sql/`: Contains SQL scripts, such as `create_tables.sql`, for database setup.
-   `tables/`: Directory for storing data exported from database tables.

### Configuration

-   `requirements.txt`: Lists all the Python dependencies required to run the project.

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

## Downloads

To use the application without installing Python or its dependencies, you can download the pre-compiled executable for your operating system.

1.  Go to the **[Releases](https://github.com/fernanpemo/DB_app/releases)** page of this repository.
2.  Find the latest release (e.g., `v1.0.0`).
3.  In the **Assets** section, download the appropriate file for your system:
    -   **Windows**: `DB_app-windows.zip`
    -   **Linux**: `DB_app-linux.tar.gz`
    -   **macOS**: `DB_app.dmg`
4.  Once downloaded, decompress the file (`.zip` or `.tar.gz`) or mount the `.dmg` file.
5.  Run the `DB_app` executable inside the resulting folder.

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
