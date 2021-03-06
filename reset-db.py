# WARNING
# This script deletes the database file and configures empty
# tables for the models defined in the models module.
from application.models import classes
from application.config import *
from application.models import *
from application.models.usersModel import Users
import datetime

def init_db ():
  # First, we create the databases.
  for database in config.databases.dynamic:
    filename = config.databases.dynamic[database].filename

    """Initializes the database."""
    # Remove the DB
    if os.path.isfile(filename):
      os.remove(filename)

    # Create an empty DB file
    open(filename, 'a').close()

  # Now, go through the modules we've discovered in the models directory.
  # Create tables for each model.
  for c in classes:
    c.create_table(True)

  # Create a Users entry in the database for Scott Heggen as the admin
  # The database written to is inventory.sqlite
  (Users.create(username="heggens",
    first_name="Scott",
    last_name="Heggen",
    auth_level="admin",
    emailadd="heggens@berea.edu",
    approve=True,
    created_date=2022-01-31,
    end_date=2025-01-30,
    reportto="Idk",
    created_by="heggens"))

if __name__ == "__main__":
  init_db()
