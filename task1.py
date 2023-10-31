from taskexecutor import execute

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
