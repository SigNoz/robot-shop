from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


import redis, json

r = None
try:
    r = redis.Redis(host='redis')
except:
    print ("Redis is not connected")

import pymongo
mongoClient = None
mongoConnected = False
try:
    mongoClient = pymongo.MongoClient("mongodb://mongodb:27017/")
    mongoConnected = True
except:
    mongoConnected = False
    print ("MongoDB is not connected")


@require_http_methods(["GET"])
def uniqueid(request):
    
    try:
        val = r.incr('anonymous-counter')
        response = {'uuid': 'anonymous-' + str(val)}
        return HttpResponse(json.dumps(response))
    except:
        response = "Error"
        return HttpResponse(status=500)


@require_http_methods(["GET"])
def checkId(request, id):
    
    db = mongoClient["users"]
    usersCollection = db['users']

    user = usersCollection.find_one({
                "name": id
            })
    if user:
        return HttpResponse("OK")
    else:
        return HttpResponseNotFound("user not found")




@csrf_exempt 
@require_http_methods(["POST"])
def login(request):

    body = json.loads(request.body)


    if ((body['name'] == None) or (body['password'] == None)):
        return HttpResponseBadRequest('name or passowrd not supplied')
    elif mongoConnected:

        db = mongoClient["users"]
        usersCollection = db['users']

        try:

            user = usersCollection.find_one({
                "name": body['name']
            })

            if user:

                if (user['password'] == body['password']):
                    id_obj = user.pop('_id')
                    user['uuid'] = str(id_obj)
                    return HttpResponse(json.dumps(user))
                else:
                    
                    return HttpResponseNotFound("incorrect password")
            else:
                return HttpResponseNotFound('name not found')
        except:
            
            return HttpResponseServerError("Error in getting collection")

    else:
        
        return HttpResponseServerError('database not available')
