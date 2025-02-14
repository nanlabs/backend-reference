def get_bus_stops_query():
    """SQL query to fetch bus stops for a specific bus line."""
    return """
        SELECT * FROM bus_stop 
        WHERE %(line_number)s IS NULL OR "L1" = %(line_number)s 
        ORDER BY "L2"
    """
