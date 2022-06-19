from math import ceil
from typing import Any, List
from starlette.requests import Request
from marshmallow_jsonapi.schema import Schema


class Pagination:
    _meta: dict = {}

    def __init__(self, data: List[Any], schema:Schema) -> None:
        self._data = data
        self._schema = schema
        self._request: Request = self._schema.context["request"]
        self._total_count: int = len(self._data)
        self._page_number: int = 1
        self._page_size: int = 10

    @property
    def page_number(self):
        self._page_number = int(str(self._request.query_params.get("page_number")))
        return self._page_number
    
    @page_number.setter
    def page_number(self, val):
        self._page_number = val

    @property
    def page_size(self):
        self._page_size = int(str(self._request.query_params.get("page_size")))
        return self._page_size

    @page_size.setter
    def page_size(self, val):
        self._page_size = val

    @property
    def total_pages(self) -> int:
        return int(ceil(self._total_count) / float(self.page_size))

    def _slice_data(self) -> List[Any]:
        start = (self.page_number - 1) * self.page_size
        end = start + self.page_size
        return self._data[start:end]

    def _create_pagination_link(self, page_no: int, page_sz:int):
        url = self._request.url
        self.page_number = page_no
        self.page_size = page_sz
        return str(url.replace_query_params(page_number=self.page_number, page_size=self.page_size))

    def _init_pagination_meta(self):
        links: dict[str, Any] = {}
        links["first"] = self._create_pagination_link(page_no=1, page_sz=self.page_size)
        links["next"] = None
        links["previous"] = None
        links["last"] = self._create_pagination_link(page_no=self.total_pages, page_sz=self.page_size)

        has_next: bool = self._page_number < self.total_pages
        if has_next:
            links["next"] = self._create_pagination_link(page_no=self._page_number+1, page_sz=self.page_size)

        has_previous: bool = self._page_number > 1
        if has_previous:
            links["previous"] = self._create_pagination_link(page_no=self._page_number-1, page_sz=self.page_size)

        self._meta = {
            "total_items": self._total_count,
            "item_count": self.page_size,
            "total_pages": self.total_pages,
            "has_next": has_next,
            "has_previous": has_previous,
            "links": links 
        }

    def _mapped_data(self):
        self._init_pagination_meta()
        data = self._slice_data()
        mapped_attr = list(map(lambda a: {k:v for k, v in a.__dict__.items() if not (k.startswith("_"))}, data))
        return [dict(ma, **{"metadata": self._meta}) for ma in mapped_attr] 

    def _dump_default(self):
        data = self._data
        return self._schema.dump(data)

    def dump(self, paginate: bool):
        data: List[Any] = []

        if paginate:
            data = self._mapped_data()
            return self._schema.dump(data)

        data = self._dump_default()
        return data
