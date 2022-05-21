from starlette.applications import Starlette as App
from starlette.routing import Mount
from tortoise.contrib.starlette import register_tortoise

def create_app():
    # imports
    from service.config import DEBUG
    from service.db import DB_CONFIG
    from service.routes import schema, door

    routes = [
        Mount(path="/schema", routes=schema.routes),
        Mount(path="/api/door", routes=door.routes)
    ]

    # instatiate app
    app = App(debug=DEBUG, routes=routes)
    
    # register models
    register_tortoise(app=app, config=DB_CONFIG, generate_schemas=True)
    
    # return app instance
    return app
