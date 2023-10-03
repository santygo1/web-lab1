from taskexecutor import execute

not_returned_books = """
    SELECT book_id, COUNT(book_id) as not_returned FROM book
    NATURAL JOIN (SELECT * FROM book_reader where NOT borrow_date IS NULL AND return_date is NULL)
    GROUP BY book_id
"""

query = f"""
    SELECT 
        title as Книга,
        group_concat(author_name, ', ') as Авторы,
        genre_name as Жанр, 
        publisher_name as Издательство,
        (ifnull(nr.not_returned,0) + available_numbers) as Количество 
    FROM book
    LEFT OUTER JOIN ({not_returned_books}) as nr on nr.book_id = book.book_id 
    NATURAL JOIN genre
    NATURAL JOIN publisher
    JOIN book_author ba on book.book_id = ba.book_id
    JOIN (SELECT * from author ORDER BY author_name ASC) a on a.author_id = ba.author_id
    
    GROUP BY ba.book_id --группируем чтобы собрать авторов  
    ORDER BY title, author_name
"""

execute(query)
