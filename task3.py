from taskexecutor import execute

"""
    Вывести название книг и их авторов (если авторов несколько – то указать их через запятую),
    заказанных самыми активными читателями. Самыми активными считать читателей, которые взяли больше всех книг.
"""

query = f"""
    WITH 
    get_readers_books_count AS (
        SELECT reader_id, count(*) as books_count FROM book_reader
        GROUP BY reader_id),
    get_readers_max_books_count AS (
        SELECT * FROM get_readers_books_count
        JOIN (SELECT max(books_count) as books_count FROM get_readers_books_count) using(books_count)
    ),
    get_books_authors(book_id, authors) AS (
            SELECT book_id, group_concat(author_name, ', ') FROM book_author
            JOIN (SELECT * FROM author ORDER BY author_name) using (author_id)
            GROUP BY book_id
        )
    
    
    SELECT DISTINCT title as Книга, authors as Авторы FROM book_reader
    JOIN get_readers_max_books_count using (reader_id)
    JOIN book using (book_id)
    JOIN get_books_authors using (book_id)
"""

execute(query)
