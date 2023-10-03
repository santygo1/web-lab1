from taskexecutor import execute

# Количество книг которые взял каждый читатель
max_book_count = """
    SELECT count(reader_id) as count FROM book_reader 
    GROUP BY reader_id
    ORDER BY count DESC 
    LIMIT 1
"""

active_readers = f"""
    SELECT reader_id FROM (SELECT *, count(reader_id) as count FROM book_reader GROUP BY reader_id)
    WHERE count = ({max_book_count})
"""

books = f"""
    SELECT 
    DISTINCT book.* 
    FROM ({active_readers}) as reader
    NATURAL JOIN book_reader
    NATURAL JOIN book
"""

query = f"""
    SELECT
    book.title as Название,
    group_concat(author_name, ', ') as Авторы 
    FROM ({books}) as book
    JOIN book_author ba on book.book_id = ba.book_id
    JOIN (SELECT * from author ORDER BY author_name ASC) a on a.author_id = ba.author_id
    GROUP BY ba.book_id --группируем чтобы собрать авторов  
"""

execute(query)
