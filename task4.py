from taskexecutor import execute


query = f"""
--     CREATE TABLE IF NOT EXISTS rating(
--         rating_id INTEGER PRIMARY KEY autoincrement, 
--         author_id INTEGER REFERENCES author(author_id),
--         rating INTEGER
--     );
--     INSERT INTO rating(author_id, rating) 
    WITH 
    -- Книги которые один читатель брал несколько раз, возвращает сколько раз книга была взята одним автором больше чем один раз (x-1)
    get_books_reader_borrow_repeatedly AS (
        SELECT book_id, count(book_reader_id) - 1 as repeatedly_borrow_count FROM book_reader
        GROUP BY book_id, reader_id 
    ),
    
    -- Общее количество взятых экземляров книг для каждой книги
    get_books_count_reads AS (
        SELECT book_id, count(book_reader_id) as borrow_count FROM book_reader
        GROUP BY book_id
    )
    
    -- Высчитываем суммарный рейтинг авторов
    SELECT author_id, sum(author_rating) FROM (
        -- высчитываем рейтинг авторов для каждой его книги
        SELECT 
            author_id,
            CASE 
                WHEN borrow_count < 3 THEN borrow_count*2
                WHEN borrow_count > 2 THEN borrow_count*4
                END + repeatedly_borrow_count*3 as author_rating
        FROM book_author
        JOIN author using(author_id)
        JOIN book using(book_id)
        JOIN get_books_reader_borrow_repeatedly using (book_id)
        JOIN get_books_count_reads using (book_id)
    )
    GROUP BY author_id
"""


execute(query)
