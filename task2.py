from taskexecutor import execute

"""
    Посчитать общее количество экземпляров каждой книги в библиотеке.
    Общее количество экземпляров книги определяется как сумма доступного количества экземпляров книги в таблице book
    и количества экземпляров этой книги "на руках" у читателя. Вывести название книги (столбец Книга), ее авторов,
    если авторов несколько - перечислить их через запятую в алфавитном порядке, в одном поле (Авторы), жанр книги (Жанр),
    издательство (Издательство) и количество экземпляров (Количество).
    Информацию отсортировать сначала по названиям книг в алфавитном порядке, а затем по фамилиям автора тоже в алфавитном порядке.
"""

query = f"""
    WITH 
        get_books_with_total AS (
            SELECT book.*,(available_numbers + count(book_reader_id)) as total FROM book
            LEFT JOIN book_reader using (book_id) -- потому, что могут быть книги которые не брали
            WHERE book_reader_id IS NULL -- чтобы остались книги которые не брали вообще 
                OR (borrow_date IS NOT NULL AND return_date IS NULL ) -- книги которые взяли но не вернули
            GROUP BY book_id   
        ),
        get_books_authors(book_id, authors) AS (
            SELECT book_id, group_concat(author_name, ', ') FROM book_author
            JOIN (SELECT * FROM author ORDER BY author_name) using (author_id)
            GROUP BY book_id
        )
    
    SELECT 
        title as Книга,
        authors as Авторы,
        genre_name as Жанр,
        publisher_name as Издательство,
        total as Количество
    FROM get_books_with_total
    JOIN get_books_authors using(book_id)
    JOIN genre using(genre_id)
    JOIN publisher using(publisher_id)
    
    ORDER BY title, authors
"""

execute(query)
