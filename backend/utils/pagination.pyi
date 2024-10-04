from typing import Any
from fastapi import Query, Request

class Pagination:
    page: int
    page_size: int
    request: Request
    def __init__(self, request: Request, page: int = ..., page_size: int = ...) -> None: ...
    def get_next_url(self, total_pages: int) -> str | None: ...
    def get_prev_url(self) -> str | None: ...