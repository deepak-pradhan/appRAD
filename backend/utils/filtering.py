from sqlalchemy import or_
from sqlmodel import select
from backend.utils.exceptions import CustomHTTPException

def apply_filters(query, filters):
    try:
        for field, value in filters.items():
            if isinstance(value, list):
                query = query.filter(getattr(query.model_class, field).in_(value))
            elif isinstance(value, dict):
                op = value.get('op', 'eq')
                if op == 'eq':
                    query = query.filter(getattr(query.model_class, field) == value['value'])
                elif op == 'ne':
                    query = query.filter(getattr(query.model_class, field) != value['value'])
                elif op == 'gt':
                    query = query.filter(getattr(query.model_class, field) > value['value'])
                elif op == 'lt':
                    query = query.filter(getattr(query.model_class, field) < value['value'])
                elif op == 'ge':
                    query = query.filter(getattr(query.model_class, field) >= value['value'])
                elif op == 'le':
                    query = query.filter(getattr(query.model_class, field) <= value['value'])
                elif op == 'like':
                    query = query.filter(getattr(query.model_class, field).like(f"%{value['value']}%"))
                elif op == 'ilike':
                    query = query.filter(getattr(query.model_class, field).ilike(f"%{value['value']}%"))
            else:
                query = query.filter(getattr(query.model_class, field) == value)
    except AttributeError:
        raise CustomHTTPException(status_code=400, detail=f"Invalid filter field: {field}")
    except ValueError:
        raise CustomHTTPException(status_code=400, detail=f"Invalid filter value for field: {field}")
    return query   