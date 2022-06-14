from starlette.applications import Starlette as App
from starlette.routing import Mount


def create_app():
    # imports
    from service.config import DEBUG
    from service.routes import schema, door
    from service.events import on_startup, on_shutdown


    routes = [
        Mount(path="/schema", routes=schema.routes),
        Mount(path="/api/door", routes=door.routes)
    ]

    # instatiate app
    app = App(
        debug=DEBUG, 
        routes=routes, 
        on_startup=[on_startup], 
        on_shutdown=[on_shutdown]
    )

    # return app instance
    return app
