from application import app
from application.models import *
from application.config import *
from application.logic.validation import require_role

from flask import \
    render_template, \
    request, \
    url_for

# PURPOSE: Shows specific chemical and all containers of said chemical.
@app.route('/a/ViewChemical/<string:chemical>/', methods = ['GET'])
@require_role('systemUser')
def aViewChemical(chemical):
  return render_template("views/a/aViewChemicalView.html", config = config)

