from taskexecutor import execute

"""
    Вывести книги, которые были взяты в библиотеке в октябре месяце.
    Указать фамилии читателей, которые их взяли,
    а также дату, когда их взяли. Столбцы назвать Название, Читатель, Дата соответственно.
    Информацию отсортировать сначала по возрастанию даты, потом в алфавитном порядке по фамилиям читателей,
    и, наконец, по названиям книг тоже в алфавитном порядке.
"""

query = """
      SELECT 
        title as Название,
        reader_name as Читатель,
        borrow_date as Дата
      FROM book_reader
      JOIN reader using(reader_id)
      JOIN book using(book_id)
      WHERE strftime('%m', borrow_date) = '10'
      ORDER BY borrow_date, reader_name , title
"""

execute(query)
