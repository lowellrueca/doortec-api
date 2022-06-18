from math import ceil
from typing import List, Any
from marshmallow_jsonapi import Schema
from starlette.requests import Request
    

async def default_or_paginate(data: List[Any], schema: Schema):
    # retrieve the request context from schema
    request: Request = schema.context["request"]
    url_path = request.url.path

    # retrieve the query for page number and page size
    page_number_query = request.query_params.get("page_number")
    page_size_query = request.query_params.get("page_size")

    # cast page number and page size query into integer
    page_number = int(str(page_number_query))
    page_size = int(str(page_size_query))
    
    # define start and end for paging
    total_count = len(data)
    start = (page_number -1) * page_size
    end = start + page_size

    # paginate data
    paginated_data = data[start:end]

    # define total no. of pages
    if page_size == 0:
        pages = 0

    else:
        pages = int(ceil(total_count / float(page_size)))

    # define metadata
    metadata = {
        "total": total_count,
        "count": page_size,
        "pages": pages,
        "links": {}
    }

    # define first page
    metadata["links"]["first"] = f"{url_path}?page_number=1&page_size={page_size}"

    # define last page
    metadata["links"]["last"] = f"{url_path}?page_number={pages}&page_size={page_size}"

    if end >= total_count:
        metadata["links"]["next"] = None

        if page_number > 1:
            metadata["links"]["previous"] = f"{url_path}?page_number={page_number-1}&page_size={page_size}"
        else:
            metadata["links"]["previous"] = None

    else:
        if page_number > 1:
            metadata["links"]["previous"] = f"{url_path}?page_number={page_number-1}&page_size={page_size}"
        else:
            metadata["links"]["previous"] = None
        metadata["links"]["next"] = f"{url_path}?page_number={page_number+1}&page_size={page_size}"

    # map paginated data for serialization
    mapped_data = list(map(lambda x: {
                "id": x.id, 
                "series": x.series, 
                "price": x.price, 
                "metadata": metadata}, 
            paginated_data
        )
    )

    content = schema.dump(mapped_data)
    return content
