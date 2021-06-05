import random
import logging
import coloredlogs
from aiohttp import web

logger = logging.getLogger("API")
logger.setLevel(logging.INFO)

coloredlogs.install(level="INFO", logger=logger)
routes = web.RouteTableDef()

eightball_answers = [
    "probably",
    "probably not",
    "maybe",
    "i'm unsure",
    "who knows",
    "let me think about it",
    "what",
    "absolutely not",
    "yes, defenetely",
    "100%, yes"
    "i don't think so",
    "i think so"
]

def log(request):
    try:
        message = dict(request.headers)["message"]
    except:
        logger.info(f"\"{request.remote}\" accessed endpoint \"{request.path}\"")
    else:
        logger.info(f"\"{request.remote}\" accessed endpoint \"{request.path}\" with message \"{message}\"")

@routes.post("/mock")
async def mock(request):
    log(request)
    try:
        message = dict(request.headers)["message"]
    except KeyError:
        return web.json_response({"message": None, "error": f"Missing required argument \"message\""}, status=400, content_type="application/json")
    else:
        msg = "".join(m.upper() if random.randint(1,2) == 1 else m.lower() for m in message)
        return web.json_response({"message": msg, "error": None}, status=200, content_type="application/json")

@routes.post("/owoify")
async def owo(request):
    log(request)
    try:
        message = dict(request.headers)["message"]
    except KeyError:
        return web.json_response({"message": None, "error": f"Missing required argument \"message\""}, status=400, content_type="application/json")
    else:
        msg = message.replace("l", "w").replace("r", "w")
        return web.json_response({"message": msg, "error": None}, status=200, content_type="application/json")

@routes.post("/spoiler")
async def spoiler(request):
    log(request)
    try:
        message = dict(request.headers)["message"]
    except KeyError:
        return web.json_response({"message": None, "error": f"Missing required argument \"message\""}, status=400, content_type="application/json")
    else:
        msg = "".join(f"||{m}||" for m in message)
        return web.json_response({"message": msg, "error": None}, status=200, content_type="application/json")

@routes.get("/8ball")
async def eightball(request):
    log(request)
    answer = random.choice(eightball_answers)
    return web.json_response({"message": answer}, status=200, content_type="application/json")

@routes.get("/pp")
async def pp(request):
    log(request)
    size = "".join("=" for x in range(random.randrange(0,10)))
    pp = f"8{size}D"
    return web.json_response({"message": pp}, status=200, content_type="application/json")

@routes.get("/endpoints")
async def endpoints(request):
    log(request)
    rootes = {}
    for route in list(routes):
        rootes[str(route.path)] = route.method
    return web.json_response(rootes, status=200, content_type="application/json")

@routes.get("/")
async def index(request):
    log(request)
    rootes = {}
    for route in list(routes):
        rootes[str(route.path)] = route.method
    text = "\n".join(f"{endpoint} - {rootes[endpoint]}" for endpoint in rootes)
    return web.Response(text=f"""
Routes: {len(routes)}
GET Routes: {''.join(route for route in rootes if rootes[route] == "GET")}
POST Routes: {''.join(route for route in rootes if rootes[route] == "POST")}

{text}
""", status=200, content_type="application/json")

app = web.Application()
app.add_routes(routes)
web.run_app(app)