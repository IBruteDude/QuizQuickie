
# QuizQuickie

QuizQuickie is a quizzing api that allows for creating quizzes, creating user groups, schedualing quizzes for users, user statistics and progression profile.

## Run Locally

* ### Clone the project

```bash
 git clone https://github.com/IBruteDude/QuizQuickie
```

* ### Go to the project directory

```bash
 cd QuizQuickie/
```

* ### For MySQL user and database setup

* #### For Windows

    ```powershell
     type db_setup.sql | mysql -uroot -p
    ```

* #### For Linux/WSL

    ```bash
     cat db_setup.sql | mysql -uroot -p
    ```

* ### Ensure python and pip are installed

    ```bash
     python --version
     pip --version
    ```

* ### Install the virtualenv package

    ```bash
     pip install virtualenv
    ```

* ### Create a python virtual environment

    ```bash
     python -m venv venv
    ```

* ### Activate the virtual environment

  * #### For Windows

    ```powershell
     venv\Scripts\activate
    ```

  * #### For Linux/WSL

    ```bash
     source venv/bin/activate
    ```

* ### Install the required dependencies

    ```bash
     pip install -r requirements.txt
    ```

* ### Run the flask server

    ```bash
     python -m run
    ```

## Swagger API Docs

* #### Access the Swagger UI at: <http://localhost:5000/apidocs/>
