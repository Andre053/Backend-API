from flask import Flask, Response, json # Flask for instantiating the app, Response and json for responding to calls
from api import ApiConnection # connection to the API and memory cache
import threading, time # used to have a reset for our cache
import enums # the sort and direction options
import tests # test endpoints


# our global variables
app = Flask(__name__) # instance of Flask
conn = ApiConnection() # our api connection

# Route for ping response
@app.route("/api/ping")
def ping():
    js = {
            "success": True
        }
    return Response(
        json.dumps(js),
        status=200,
        mimetype='application/json'
    )

# Covers many different route options
@app.route("/api/posts/")
@app.route("/api/posts/<string:tags>")
@app.route("/api/posts/<string:tags>/<string:sortBy>")
@app.route("/api/posts/<string:tags>/<string:sortBy>/<string:direction>")
async def posts(tags=None, sortBy="id", direction="asc"): # TODO: test input parameters
    """
    This function is triggered whenever the above URLs are visited
    """
    response = await build_response(tags, sortBy, direction) #

    return response


async def build_response(tags, sortBy, direction):
    """
    Checks inputs for errors, if none, continues to gather the requested results
    """
    # Error handling
    if not tags: return error("The tags parameter is required.")
    tags = tags.split(',')
    if sortBy in enums.Sort.__members__ and direction in enums.Direction.__members__:
        sort = enums.Sort[sortBy]
        dirct = enums.Direction[direction]
    else: return error("The sortBy or direction parameter is invalid.")

    return await gather_results(tags, sort, dirct)

async def gather_results(tags, sort, dirct):
    """
    Calls the API endpoint which gathers all results based on our tag list
    After results have been retreived, the sorter function sorts based on the parameters we have
    """
    results = await conn.gather(tags)
    
    sorter(results['posts'], sort, dirct) # sorts the posts list, which is mutable and passed by object reference

    # now our result has been aquired and sorted, we can start returning up to the original route call    
    return Response(
        json.dumps(results, indent=4),
        status=200,
        mimetype='application/json'
    )

def sorter(posts, sort, dirct):
    # if direction is ascending, reverse is false, otherwise it is true
    if dirct.name == "asc": rev = False
    else: rev = True

    # Lambda function used as the key will sort based on the parameter we want to sort by
    posts.sort(key=lambda x: x[sort.name], reverse=rev) 

def error(error_string):
    # handles errors that occur from the /api/posts route
    js = {
            "error": error_string
        }
    return Response(
        json.dumps(js),
        status=400,
        mimetype='application/json'
    )

def cache_set():
    """
    Runs on personal thread, resetting cache after a certain amount of time
    Time is set to 30 to demonstrate the reset, in reality it would likely 
    exist for a longer period of time, with an option of resetting based on size
    """
    while True: 
        conn.cache = dict() # resets the cache variable in the API instance
        time.sleep(30) # after x amount of time, we reset again

# second thread will not start until tests have been passed
# if any tests fail the server will not start
with app.test_client() as client:
    print("Running tests")
    tests.test_ping_request(client)
    tests.test_posts_requests_empty(client)
    tests.test_posts_requests_order(client)
    tests.test_posts_requests_sort(client)
    tests.test_posts_requests_tags(client)
    print("Tests passed")

thread = threading.Thread(target=cache_set)
thread.start() # thread for resetting the cache

