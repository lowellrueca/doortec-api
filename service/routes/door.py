from marshmallow import ValidationError
from service.models import Door
from service.resources.schema import DoorSchema
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import Response, JSONResponse
from tortoise.exceptions import DoesNotExist


async def get_many(request: Request) -> Response:
    """
    summary: Retrieves a list of door products.
    responses:
      200:
        description: Ok.
        content:
          application/vnd.api+json:
            schema: DoorSchema
      204:
        description: No content.
    """
    doors = await Door.all()

    if len(doors) == 0:
        return Response(content=None, status_code=204)

    content = DoorSchema(many=True).dump(doors)
    headers = {"Content-Type": "application/vnd.api+json"}
    return JSONResponse(content=content, status_code=200, headers=headers)


async def get(request: Request) -> Response:
    """
    summary: Retrieves a single door product.
    responses:
      200:
        description: Ok.
        content:
          application/vnd.api+json:
            schema: DoorSchema
      404:
        description: Door not found.
    """
    try:
        id = request.path_params["id"]
        door = await Door.get(id=id)

    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Door not found")

    content = DoorSchema().dump(door)
    headers = {"Content-Type": "application/vnd.api+json"}
    return JSONResponse(content=content, status_code=200, headers=headers)


async def post(request: Request) -> Response:
    """
    summary: Create a door product.
    responses:
      201:
        description: Successfully created.
        content:
          application/vnd.api+json:
            schema: DoorSchema
      422:
        description: Unprocessable entity.
    """
    json_body = await request.json()
    schema = DoorSchema()
    
    try:
        data = schema.load(json_body)

    except ValidationError:
        raise HTTPException(status_code=422, detail="Unprocessable entity")

    door = Door()

    series = data.get("series")
    if series:
        door.series = series

    await door.save()
    content = schema.dump(door)
    headers = {"Content-Type": "application/vnd.api+json"}
    return JSONResponse(content=content, status_code=201, headers=headers)


async def patch(request: Request) -> Response:
    """
    summary: Updates a door product.
    responses:
      200:
        description: Ok.
        content:
          application/vnd.api+json:
            schema: DoorSchema
      404:
        description: Door not found.
      422:
        description: Unprocessable entity.
    """
    id = request.path_params["id"]

    try:
        door = await Door.get(id=id)

    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Door not found")

    schema = DoorSchema()
    json_body = await request.json()

    try:
        data = schema.load(json_body)

    except ValidationError:
        raise HTTPException(status_code=422, detail="Unprocessable entity")

    series = data.get("series")
    if series:
        door.series = series

    await door.save()
    content = DoorSchema().dump(door)
    headers = {"Content-Type": "application/vnd.api+json"}
    return JSONResponse(content=content, status_code=200, headers=headers)


async def delete(request: Request) -> Response:
    """
    summary: Delete a door product.
    responses:
      204:
        description: No content.
      404:
        description: Door not found.
    """
    id = request.path_params["id"]

    try:
        door = await Door.get(id=id)

    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Door not found")

    await door.delete()
    return Response(content=None, status_code=204)


routes = [
    Route("/", endpoint=get_many, methods=["GET"]),
    Route("/{id}", endpoint=get, methods=["GET"]),
    Route("/", endpoint=post, methods=["POST"]),
    Route("/{id}", endpoint=patch, methods=["PATCH"]),
    Route("/{id}", endpoint=delete, methods=["DELETE"]),
]
