from application import app
from application.models.buildingsModel import Buildings
from application.models.floorsModel import Floors
from application.models.roomsModel import Rooms
from application.models.storagesModel import Storages
from application.models.util import *
from application.config import *
from application.logic.validation import require_role
from application.logic.sortPost import *

from flask import \
    render_template, \
    redirect, \
    request, \
    url_for

@app.route('/ma/delete/<location>/<lId>/', methods = ['GET', 'POST']) #Called from delete location modals
def maDelete(location, lId):
    if request.method == "GET": #Calls delete queries based on what type of location is being deleted.
        if location == "Building":
            building = Buildings.delete().where(Buildings.bId == lId)
            building.execute()
        elif location == "Floor":
            floor = Floors.delete().where(Floors.fId == lId)
            floor.execute()
        elif location == "Room":
            room = Rooms.delete().where(Rooms.rId == lId)
            room.execute()
        elif location == "Storage":
            storage = Storages.delete().where(Storages.sId == lId)
            storage.execute()
    return redirect("ma/Home/")