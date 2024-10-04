from sqlalchemy import desc

def apply_sorting(query, sort_string):
    """
    Apply sorting to a SQLAlchemy query based on a sort string.

    Args:
        query: The SQLAlchemy query to sort.
        sort_string: A comma-separated string of fields to sort by. Prefix with '-' for descending order.

    Returns:
        The sorted SQLAlchemy query.
    """
    if sort_string:
        sort_fields = sort_string.split(',')
        for field in sort_fields:
            if field.startswith('-'):
                query = query.order_by(desc(getattr(query.model_class, field[1:])))
            else:
                query = query.order_by(getattr(query.model_class, field))
    return query    