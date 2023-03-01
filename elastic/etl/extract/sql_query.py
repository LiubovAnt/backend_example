modified = """
SELECT modified \n
FROM content.{table} \n
ORDER BY modified \n
LIMIT 1;
"""

producer_count = """
SELECT COUNT(*) \n
FROM content.{table} \n
WHERE modified > %s;
"""

producter = """
SELECT id, modified \n
FROM content.{table} \n
WHERE modified > %s \n
ORDER BY modified \n
OFFSET %s \n
LIMIT %s;
"""

enricher_fw = """
SELECT tb.person_id as id, fw.modified \n
FROM content.film_work fw \n
LEFT JOIN content.person_film_work tb ON tb.film_work_id = fw.id \n
WHERE fw.id IN %s \n
ORDER BY fw.modified \n
OFFSET %s \n
LIMIT %s;
"""

enricher_count = """
SELECT COUNT(*) FROM content.film_work as fw \n
LEFT JOIN content.{table} as tb ON tb.film_work_id = fw.id \n
WHERE tb.{id} IN %s;
"""

enricher_count_fw = """
SELECT COUNT(*) FROM content.film_work as fw \n
LEFT JOIN content.{table} as tb ON tb.film_work_id = fw.id \n
WHERE fw.id IN %s;
"""

person = """
SELECT p.id as id, \n
p.full_name as full_name, \n
p.modified as modified, \n
pfw.role as role, \n
pfw.film_work_id as film_ids \n
FROM content.person p \n
LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id \n
WHERE p.id IN %s \n
ORDER BY p.modified;
"""

genre = """
SELECT id, name, description, modified \n
FROM content.genre \n
WHERE modified > %s \n
ORDER BY modified \n
OFFSET %s \n
LIMIT %s;
"""

film = """
SELECT fw.id as id, \n
fw.rating as imdb_rating, \n
g.name as genre, \n
g.id as genre_id, \n
fw.title as title, \n
fw.description as description, \n
fw.type as type, \n
fw.created as created, \n
fw.modified as modified, \n
pfw.role as role, \n
p.id as person_id, \n
p.full_name as full_name \n
FROM content.film_work fw \n
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id \n
LEFT JOIN content.person p ON p.id = pfw.person_id \n
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id \n
LEFT JOIN content.genre g ON g.id = gfw.genre_id \n
WHERE fw.id IN %s \n
ORDER BY fw.modified;
"""

enricher = """
SELECT fw.id, fw.modified \n
FROM content.film_work fw \n
LEFT JOIN content.{table} tb ON tb.film_work_id = fw.id \n
WHERE tb.{id} IN %s \n
ORDER BY fw.modified \n
OFFSET %s \n
LIMIT %s;
"""
