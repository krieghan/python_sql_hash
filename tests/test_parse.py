import unittest
import sqlhash

class TestParse(unittest.TestCase):
  def test_select_from_empty_table(self):
    sqlhash.set_state({'empty_table' : []})
    query = "SELECT * FROM empty_table"
    result = sqlhash.execute(query)
    self.assertEquals([], result)

  def test_select_one_row_one_column(self):
    sqlhash.set_state({'a_table' : [{'a_column' : '1'}]})
    query = "SELECT a_column FROM a_table"
    result = sqlhash.execute(query)
    self.assertEquals([{'a_column' : '1'}], result)

  def test_select_with_where(self):
    sqlhash.set_state({'a_table' : [{'a_column' : '1'},
                                    {'a_column' : '2'}]})
    query = "SELECT a_column FROM a_table WHERE a_column = '1'"
    result = sqlhash.execute(query)
    self.assertEquals([{'a_column' : '1'}], result)
    
