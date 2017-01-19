from application.models.util import *
from application.logic.sortPost import *

class Users (Model):
    userId       = PrimaryKeyField()
    username     = TextField(null = False, unique = True)
    auth_level   = TextField(null = False)
    emailadd     = TextField(null = True)
    approve      = BooleanField(default = False)
    created_date = DateTimeField(null = True)
    end_date     = DateTimeField(null = True)
    reportto     = TextField(null = False)
    created_by   = TextField(null = True)

    class Meta:
        database = getDB("inventory", "dynamic")

def createUser(data, createdBy, approval, authLevel = "systemUser"):
    """Used to check containers in and out

    Args:
        data (dict): A dictionary with keys for each field in users, and values for a specific user instance
        createdBy (str): Username of the user that has accessed the page that calls this function
        approval (bool): True for admin, False for superUser
    Returns:
        tuple:
            element[0]: Message to flash to user
            element[1]: Formatting for the flash message
    """ #should return something else for unit testing later
    modelData, extraData = sortPost(data, Users)
    modelData['approve'] = approval
    modelData['username'] = modelData['username'].lower()
    modelData['created_by'] = createdBy
    modelData['created_date'] = datetime.date.today()
    if 'auth_level' not in modelData:
        modelData['auth_level'] = authLevel
    # Peewee has a get_or_create function. Would that be more useful than putting this in a try/except?
    if modelData['end_date'] >= datetime.date.today():
        return("Error: User could not be added. End Date must be later than today.", 'list-group-item list-group-item-danger')
    try:
        Users.create(**modelData)
        return("Success: User added successfully.", 'list-group-item list-group-item-success')
    except:
        return("Error: User could not be added.", 'list-group-item list-group-item-danger')

def approveUsers(user):
    try:
        query = Users.update(approve = True).where(Users.userId == user)
        query.execute()
        return("Success: User approved.", 'list-group-item list-group-item-success')
    except:
        return("Error: User could not be approved.", 'list-group-item list-group-item-danger')

def denyUsers(user):
    try:
        query = Users.delete().where(Users.userId == user)
        query.execute()
        return("Success: User has been denied.", 'list-group-item list-group-item-success')
    except:
        return("Error: User could not be removed.", 'list-group-item list-group-item-danger')
