from fastapi import Query, Request

class Pagination:
    def __init__(self, request: Request, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
        self.page = page
        self.page_size = page_size
        self.request = request

    def get_next_url(self, total_pages):
        if self.page < total_pages:
            return str(self.request.url.include_query_params(page=self.page + 1))
        return None

    def get_prev_url(self):
        if self.page > 1:
            return str(self.request.url.include_query_params(page=self.page - 1))
        return None        