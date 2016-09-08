from application import app
from application.models.buildingsModel import Buildings
from application.models.floorsModel import Floors
from application.models.roomsModel import Rooms
from application.models.storagesModel import Storages
from application.models.containersModel import Containers
from application.models.util import *
from application.config import *
from application.logic.validation import require_role
from application.logic.sortPost import *

from flask import \
    render_template, \
    redirect, \
    request, \
    flash, \
    url_for

@app.route('/ma/delete/<location>/<lId>/', methods = ['GET', 'POST']) #Called from delete location modals
@require_role('admin')
def maDelete(location, lId):
    state = 0
    if request.method == "GET": #Calls delete queries based on what type of location is being deleted.
        if location == "Building":
            floors = Floors.select().where(Floors.buildId == lId) #All floors of the current building
            for floor in floors:
                rooms = Rooms.select().where(Rooms.floorId == floor) #All rooms of current floor
                for room in rooms:
                    storages = Storages.select().where(Storages.roomId == room) #All storage locations of current room
                    for storage in storages:
                        try:
                            Containers.get(Containers.storageId == storage, #Try to get any containers associated with current storage location
                                           Containers.disposalDate == None)
                            state = 1
                        except:
                            pass
            if state != 1:
                building = Buildings.delete().where(Buildings.bId == lId)
                building.execute()
            else:
                flash("This building could not be deleted, as there are 1 or more containers still assigned to it.")
        elif location == "Floor":
            rooms = Rooms.select().where(Rooms.floorId == lId)
            for room in rooms:
                storages = Storages.select().where(Storages.roomId == room)
                for storage in storages:
                    try:
                        Containers.get(Containers.disposalDate == None,
                                       Containers.storageId == storage)
                        state = 1
                    except:
                        pass
            if state != 1:
                floor = Floors.delete().where(Floors.fId == lId)
                floor.execute()
            else:
                flash("This floor could not be deleted, as there are 1 or more containers still assigned to it.")
        elif location == "Room":
            storages = Storages.select().where(Storages.roomId == lId)
            for storage in storages:
                try:
                    Containers.get(Containers.disposalDate == None,
                                   Containers.storageId == storage)
                    state = 1
                except:
                    pass
            if state != 1:
                room = Rooms.delete().where(Rooms.rId == lId)
                room.execute()
            else:
                flash("This room could not be deleted, as there are 1 or more containers still assigned to it.")
        elif location == "Storage":
            try:
                Containers.get(Containers.disposalDate == None,
                               Containers.storageId == lId)
                state = 1
            except:
                pass
            if state != 1:
                storage = Storages.delete().where(Storages.sId == lId)
                storage.execute()
            else:
                flash("This storage location could not be deleted, as there are 1 or more containers still assigned to it.")
    return redirect("ma/Home/")