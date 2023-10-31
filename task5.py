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
            monthno,
            julianday(lead(borrow_date, 1 ) OVER(PARTITION BY monthno ORDER BY borrow_date)) - julianday(borrow_date) as count
        FROM (SELECT * , strftime('%m', borrow_date) as monthno FROM book_reader)
        )
        
    SELECT
        monthno as Месяц,
        count(monthno) as Количество,
        max(ifnull(count, 0)) as Максимальный_перерыв
    FROM get_book_max_delay
    GROUP BY monthno
    ORDER BY monthno
"""

execute(query)
