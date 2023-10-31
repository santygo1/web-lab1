from taskexecutor import execute

"""
    Создать таблицу rating с рейтингом авторов. Рейтинг определяется востребованностью книги в библиотеке 
    (только для тех книг, которые читатели брали хотя бы один раз). Баллы начисляются автору, когда его(ее)
    книгу берет в библиотеке читатель. Правило начисления баллов:

    - если книгу брали 1 или 2 раза, ее автору начисляется 2 балла за каждый взятый экземпляр;
    - если книгу брали больше двух раз, ее автору начисляется 4 балла за каждый взятый экземпляр;
    - если книгу какой-то читатель брал больше одного раза, автору этой книги 
        дополнительно начисляется еще 3 балла за каждую такую книгу.
    
    Полученные баллы суммируются.
    В таблицу включить фамилию автора и его рейтинг. Столбцы назвать Автор и Рейтинг соответственно.
    Информацию в таблице отсортировать сначала по убыванию рейтинга, затем по фамилии авторов в алфавитном порядке.
"""

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
