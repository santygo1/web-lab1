from taskexecutor import execute

query = f"""
    WITH get_active_readers (reader_id) AS (
        SELECT reader_id FROM (SELECT *, count(reader_id) as count FROM book_reader GROUP BY reader_id)
        WHERE count = (
            SELECT count(reader_id) as count FROM book_reader 
            GROUP BY reader_id
            ORDER BY count DESC 
            LIMIT 1
        )
    )
    
    SELECT
        book.title as Название,
        group_concat(author_name, ', ') as Авторы 
    FROM (
        SELECT 
        DISTINCT book.* 
        FROM (get_active_readers) as reader
        NATURAL JOIN book_reader
        NATURAL JOIN book
    ) as book
    JOIN book_author ba on book.book_id = ba.book_id
    JOIN (SELECT * from author ORDER BY author_name) a on a.author_id = ba.author_id
    GROUP BY ba.book_id --группируем чтобы собрать авторов  
"""

execute(query)
