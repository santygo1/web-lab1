from taskexecutor import execute

query = """
      SELECT 
      b.title as Название,
      r.reader_name as Читатель,
      borrow_date as Дата
      FROM book_reader
      NATURAL JOIN reader as r
      NATURAL JOIN book as b
      WHERE strftime('%m', borrow_date) = '10'
      ORDER BY Дата, Читатель, Название
"""

execute(query)