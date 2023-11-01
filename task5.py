from taskexecutor import execute

"""
    Получить информацию о том, как часто брали читатели книги в библиотеке каждый месяц.
    Вывести, сколько экземпляров книг было взято в течение месяца.
    Также указать максимальное количество дней перерыва между днями,
    когда читатели брали книги. Столбцы назвать Месяц, Количество,
    Максимальный_перерыв. Информацию отсортировать по возрастанию номера месяца.
"""

query = """
    WITH get_book_max_delay AS ( 
        SELECT 
            borrow_date,
            julianday(lead(borrow_date, 1 ) OVER(PARTITION BY strftime('%m', borrow_date) ORDER BY borrow_date)) - julianday(borrow_date) as count
        FROM  book_reader
        )
        
    SELECT
        strftime('%m', borrow_date) as Месяц,
        count(borrow_date) as Количество,
        max(ifnull(count, 0)) as Максимальный_перерыв
    FROM get_book_max_delay
    GROUP BY Месяц
    ORDER BY Месяц
"""

execute(query)
