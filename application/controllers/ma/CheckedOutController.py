from application import app
from application.models.containersModel import *
from application.config import *
from application.logic.validation import require_role

from flask import \
    render_template, \
    request, \
    url_for

# PURPOSE: Display containers that are checked out
@app.route('/ma/CheckedOut/', methods = ['GET'])
@require_role('admin')
def maCheckedOut():
  containers = Containers.select().where(Containers.checkedOut == True)
  return render_template("views/ma/CheckedOutView.html",
                         config = config,
                         contConfig = contConfig,
                         containers = containers)

