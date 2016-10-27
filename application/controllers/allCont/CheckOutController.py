from application import app
from application.models.chemicalsModel import *
from application.models.containersModel import *
from application.models.storagesModel import *
from application.models.buildingsModel import *
from application.models.historiesModel import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser

from flask import \
    render_template, \
    request, \
    jsonify, \
    url_for, \
    abort
    
# PURPOSE: Check out a container
@app.route('/checkOut/', methods=['GET', 'POST'])
def CheckOut():
    auth = AuthorizedUser()
    user = auth.getUser()
    userLevel = auth.userLevel()
    print user.username, userLevel
    
    if userLevel == "admin" or userLevel == "systemAdmin":
        storageList = Storages.select()
        buildingList = Buildings.select()
        if request.method == "POST":
            data = request.form
            cont = Containers.get(Containers.barcodeId == data['barcodeId'])
            Histories.create(movedFrom = cont.storageId,
                            movedTo = data['storageId'],
                            containerId = cont.conId,
                            modUser = user.username,
                            action = "Checked Out",
                            pastQuantity = "%s %s" %(cont.currentQuantity, cont.currentQuantityUnit))
            cont.storageId = data['storageId']
            cont.checkedOut = True
            cont.checkOutReason = data['forClass']
            cont.forProf = data['forProf']
            cont.checkedOutBy = data['user']
            cont.save()
        return render_template("views/CheckOutView.html",
                               config = config,
                               contConfig = contConfig,
                               container = None, #container = None is needed as a placeholder for the page before the barcode is entered.
                               buildingList = buildingList,
                               storageList = storageList,
                               pageConfig = checkOutConfig,
                               authLevel = userLevel,
                               user = user)
    else:
        # This will later have a slightly different render_template. To allow for all other users to access a specific checkout page.
        abort(403)
