from .models import Restaurant


def search_restaurants(q="", neighborhood=""):
    filters = ["is_active = 1"]

    if q:
        filters.append(f"(name LIKE '%{q}%' OR cuisine LIKE '%{q}%' OR description LIKE '%{q}%')")

    if neighborhood:
        filters.append(f"neighborhood = '{neighborhood}'")

    sql = """
        SELECT *
        FROM reservations_restaurant
        WHERE {where_clause}
        ORDER BY rating DESC, name ASC
        LIMIT 30
    """.format(where_clause=" AND ".join(filters))

    return list(Restaurant.objects.raw(sql))
