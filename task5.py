from taskexecutor import execute


book_delay = """
    SELECT
        *,
        julianday(lead(borrow_date, 1 ) OVER(PARTITION BY monthno ORDER BY borrow_date)) - julianday(borrow_date) as count
    FROM (SELECT * , strftime('%m', borrow_date) as monthno FROM book_reader) as book_month
"""

query = """
    SELECT
    monthno as Месяц,
    count(book_id) as Количество,
    max(ifnull(count, 0)) as Максимальный_перерыв
    FROM (
    SELECT
        *,
        julianday(lead(borrow_date, 1 ) OVER(PARTITION BY monthno ORDER BY borrow_date)) - julianday(borrow_date) as count
    FROM (SELECT * , strftime('%m', borrow_date) as monthno FROM book_reader) as book_month
    )
    GROUP BY monthno
"""


execute(query)