from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette_apispec import APISpecSchemaGenerator


async def schema(request: Request) -> Response:
    # api spec
    spec = APISpec(
        title="DoorTec API", 
        version="1.0.0", 
        openapi_version="3.0.0", 
        info={
            "description": "An API of door products for a door manufacturer"
        },
        plugins=[MarshmallowPlugin()]
    )

    # door product resource
    spec.path(
        path="/api/door/{id}", 
        parameters=[
            {"in":"path", "name": "id", "description": "The door product"}
        ]
    )

    # generate schema
    schema = APISpecSchemaGenerator(spec=spec)

    # open api response
    return schema.OpenAPIResponse(request)


routes = [
    Route(path="/", endpoint=schema, methods=["GET"], include_in_schema=False)
]
