from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import inflect

p = inflect.engine()

class CrumbMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path_parts = request.url.path.strip('/').split('/')
        breadcrumbs = [{'title': 'Home', 'url': '/'}]
        
        for i, part in enumerate(path_parts):
            if part.isdigit():
                continue
            if i == 0:  # First part is always plural (e.g., categories, products)
                title = part.replace('_', ' ').title()
            else:  # Subsequent parts might be singular (e.g., edit, show)
                title = part.replace('_', ' ').title()
                # title = p.singular_noun(part.replace('_', ' ').title()) or part.replace('_', ' ').title()
            url = '/' + '/'.join(path_parts[:i+1])
            breadcrumbs.append({'title': title, 'url': url})
        
        for route in request.app.routes:
            if route.path == request.url.path:
                breadcrumbs[-1]['route_name'] = route.name
                break
        
        request.state.breadcrumbs = breadcrumbs
        response = await call_next(request)
        return response