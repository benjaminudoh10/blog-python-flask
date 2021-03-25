# This project is simply a clone of the medium blogging site.

## How to start the project
- Install python3 on your system.
- Create a virtual environemnt using `python3 -m venv <env-path>`.
- Activate the virtual environment using `source <env-path>/bin/activate` (unix).
- Install the required libraries using `pip3 install -r requirements.txt`.
- Run `flask db migrate`.
- Run `flask db upgrade` to create the db.
- Run the command `flask run` which starts the server on port 5000 in debug mode.
