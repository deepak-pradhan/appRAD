from typing import Type, List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Request, UploadFile, File, requests
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from backend.models.base import CModel
from backend.utils.pagination import Pagination
from backend.utils.permissions import check_permission
from backend.utils.exceptions import CustomHTTPException
from backend.db.databases import get_db
from backend.utils.caching import cache
from backend.utils.filtering import apply_filters
from backend.utils.sorting import apply_sorting
from jinja2 import Template

class BaseController:
    def __init__(self, model: Type[CModel], resource_name: str):
        self.model = model
        self.resource_name = resource_name
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory="/home/dp/Documents/appRAD/sbox1/backend/templates")
        # self.routes = []  # self.register_routes()

    def register_routes(self):
        '''
        Syntax
        =======================================================================
        def add_route(self, path, endpoint, methods, name=None):
            self.routes.append({
                "path": path,
                "endpoint": endpoint,
                "methods": methods,
                "name": name
        })
        '''
        self.router.add_api_route(f"/{self.resource_name}", self.list, methods=["GET"])
        self.router.add_api_route(f"/{self.resource_name}/search", self.search, methods=["GET"])
        self.router.add_api_route(f"/{self.resource_name}", self.create, methods=["POST"])
        self.router.add_api_route(f"/{self.resource_name}/bulk", self.bulk_create, methods=["POST"])
        self.router.add_api_route(f"/{self.resource_name}/{{id}}", self.read, methods=["GET"])
        self.router.add_api_route(f"/{self.resource_name}/{{id}}", self.update, methods=["PUT"])
        self.router.add_api_route(f"/{self.resource_name}/bulk", self.bulk_update, methods=["PUT"])
        self.router.add_api_route(f"/{self.resource_name}/{{id}}", self.delete, methods=["DELETE"])
        self.router.add_api_route(f"/{self.resource_name}/bulk", self.bulk_delete, methods=["DELETE"])
        self.router.add_api_route(f"/{self.resource_name}/{{id}}/restore", self.restore, methods=["POST"])
        self.router.add_api_route(f"/{self.resource_name}/upload", self.upload_file, methods=["POST"])
        self.router.add_api_route(f"/{self.resource_name}/{{id}}/download", self.download_file, methods=["GET"])
        self.router.add_api_route(f"/{self.resource_name}/v{{version}}", self.list_versioned, methods=["GET"])
        self.router.add_api_route(f"/{self.resource_name}/v{{version}}/{{id}}", self.read_versioned, methods=["GET"])

    @cache(expire=300)
    async def list1(self
            , request: Request
            , db: Session = Depends(get_db)
            , pagination: Pagination = Depends()
            , filters: Dict[str, Any] = None
            , sort: str = None
            ):
        try:
            query = select(self.model)
            if filters:
                query = apply_filters(query, filters)
            if sort:
                query = apply_sorting(query, sort)
            result = self.model.paginate(db
                        , query=query
                        # , page=pagination.page
                        # , per_page=pagination.page_size
                    )
            return JSONResponse(content=result)
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def search(self, request: Request, db: Session = Depends(get_db), query: str = ""):
        try:
            check_permission(request, f"search_{self.resource_name}")
            result = self.model.advanced_query(db, filters=[{"field": "name", "op": "ilike", "value": f"%{query}%"}])
            return JSONResponse(content=[item.to_dict() for item in result])
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def create(self, request: Request, db: Session = Depends(get_db), item: Optional[Dict[str, Any]] = None):
        try:
            check_permission(request, f"create_{self.resource_name}")
            if item is None:
                raise ValueError("Item data is required")
            new_item = self.model.from_dict(item)
            new_item.save(db)
            return JSONResponse(content=new_item.to_dict(), status_code=201)
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except ValueError as e:
            return JSONResponse(status_code=400, content={"detail": str(e)})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def bulk_create(self, request: Request, db: Session = Depends(get_db), items: Optional[List[Dict[str, Any]]] = None):
        try:
            check_permission(request, f"bulk_create_{self.resource_name}")
            new_items = self.model.bulk_create(items)
            for item in new_items:
                item.save(db)
            return JSONResponse(content=[item.to_dict() for item in new_items], status_code=201)
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    @cache(expire=300)
    async def read(self, request: Request, id: int, db: Session = Depends(get_db)):
        try:
            check_permission(request, f"read_{self.resource_name}")
            item = self.model.get(db, id)
            if item:
                return JSONResponse(content=item.to_dict())
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def update(self, request: Request, id: int, db: Session = Depends(get_db), item_data: Optional[Dict[str, Any]] = None):
        try:
            check_permission(request, f"update_{self.resource_name}")
            item = self.model.get(db, id)
            if item:
                item.update(db, **item_data)
                return JSONResponse(content=item.to_dict())
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def bulk_update(self, request: Request, db: Session = Depends(get_db), items: Optional[List[Dict[str, Any]]] = None):
        try:
            check_permission(request, f"bulk_update_{self.resource_name}")
            self.model.bulk_update(db, items)
            return JSONResponse(content={"detail": "Bulk update successful"})
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def delete(self, request: Request, id: int, db: Session = Depends(get_db)):
        try:
            check_permission(request, f"delete_{self.resource_name}")
            item = self.model.get(db, id)
            if item:
                item.delete(db)
                return JSONResponse(content={"detail": "Item deleted successfully"})
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})
    async def bulk_delete(self, request: Request, db: Session = Depends(get_db), ids: List[int] = None):
        try:
            check_permission(request, f"bulk_delete_{self.resource_name}")
            for id in ids:
                item = self.model.get(db, id)
                if item:
                    item.delete(db)
            return JSONResponse(content={"detail": "Bulk delete successful"})
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def restore(self, request: Request, id: int, db: Session = Depends(get_db)):
        try:
            check_permission(request, f"restore_{self.resource_name}")
            item = self.model.get(db, id)
            if item:
                item.restore()
                item.save(db)
                return JSONResponse(content=item.to_dict())
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def upload_file(self, request: Request, file: UploadFile = File(...)):
        try:
            check_permission(request, f"upload_file_{self.resource_name}")
            # Implement file upload logic here
            return JSONResponse(content={"detail": "File uploaded successfully"})
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def download_file(self, request: Request, id: int):
        try:
            check_permission(request, f"download_file_{self.resource_name}")
            # Implement file download logic here
            return FileResponse(path="path/to/file", filename="filename.ext")
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def list_versioned(self, request: Request, version: int, db: Session = Depends(get_db), pagination: Pagination = Depends()):
        try:
            check_permission(request, f"list_{self.resource_name}")
            result = self.model.paginate_version(db, version, page=pagination.page, per_page=pagination.page_size)
            return JSONResponse(content=result)
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

    async def read_versioned(self, request: Request, version: int, id: int, db: Session = Depends(get_db)):
        try:
            check_permission(request, f"read_{self.resource_name}")
            item = self.model.get_version(db, id, version)
            if item:
                return JSONResponse(content=item.to_dict())
            return JSONResponse(status_code=404, content={"detail": "Item not found"})
        except CustomHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})   

    '''
    Ollama 3.1
    '''            
    def swap(self, template_name, context=None):
        """Swap the content of an element with another element."""
        '''
        To swap the content of an element, use the swap method. For example:

        class vendorsController(BaseController):
            def edit(self, id):
                return self.swap("vendors/edit.html", {"id": id})

        This would render the edit.html template
         , and replace the content of the element with the ID of the tenant with the ID passed in.

        This will replace the entire page with the response from the server.
        '''
        if context is None:
            context = {}
        return self.render_template(template_name, context)

    def push(self, template_name, context=None):
        """Push new content into an existing element."""
        '''
        To push new content into an existing element, use the push method. For example:

        class vendorsController(BaseController):
            def list(self):
                return self.push("vendors/list.html")

        This will append new list items to the page.
        '''
        if context is None:
            context = {'ddddd'}
        html = self.render_template(template_name, context)
        template = Template(open(template_name).read())
        html = template.render(context)
        # Assuming you have a JavaScript function to append HTML to the page
        return f"append('{html}')"

    def pull(self, template_name, context=None):
        """Pull new content from a server and replace an element with it."""
        '''
        To pull new content from a server and replace an element with it, use the pull method. For example:

        class vendorsController(BaseController):
            def info(self, id):
                return self.pull("vendors/info.html", {"id": id})

        This will replace the entire page with the response from the server.
        '''
        if context is None:
            context = {}
        html = self.render_template(template_name, context)
        # Assuming you have a JavaScript function to replace the HTML of an element
        return f"replaceWith('{html}')"

    def flash(self, message):
        """Flash a message on the page for a short duration."""        
        # Assuming you have a JavaScript function to display a flash message
        '''
        To flash a message on the page for a short duration, use the flash method. For example:

        class vendorsController(BaseController):
            def submit(self):
                return self.flash("Form submitted successfully!")

        This will display a message on the page after submitting a form.
        '''
        return f"displayFlashMessage('{message}')"

    def request(self, method, url, data=None):
        """Send an HTTP request to the server."""
        '''
        Request: To send an HTTP request to the server
        , use the request method. For example:

        class vendorsController(BaseController):
            def update(self, id):
                return self.request("PUT", "/vendors/{id}", {"name": "New Name"})

        This will send a PUT request to the server and replace the entire page with the response.
        '''
        if data is None:
            data = {}
        headers = {"Content-Type": "application/json"}
        response = requests.request(method, url, json=data, headers=headers)
        return response.json()

