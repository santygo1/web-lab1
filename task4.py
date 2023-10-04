from taskexecutor import execute


query = f"""
    WITH get_books_rating AS (
        SELECT book.*, 
            (CASE 
                WHEN book.handle <= 2 THEN  book.handle*2
                WHEN book.handle > 2 THEN book.handle*4
                END ) + ifnull(mr.multi_read, 0) * 3 as rating 
        FROM (
            SELECT *, count(borrow_date) as handle FROM book_reader
            GROUP BY book_id
        ) as book
        LEFT OUTER JOIN (
            SELECT book_id, 1 as multi_read FROM book_reader
            GROUP BY reader_id, book_id
            HAVING count(borrow_date) > 1
        ) as mr on mr.book_id = book.book_id
    )

    SELECT
        author_name as Автор,
        sum(br.rating) as Рейтинг
    FROM (get_books_rating) as br
    NATURAL JOIN book 
    NATURAL JOIN author
    GROUP BY author.author_name
    ORDER BY br.rating DESC, author.author_name
"""

execute(query)
