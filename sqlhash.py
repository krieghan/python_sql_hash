import sqlparse

state = {}

def set_state(in_state):
  global state 
  state = in_state

def execute(query):
  tokens = [x for x in sqlparse.parse(query)[0].tokens if not x.is_whitespace()]
  token_types = get_token_types(tokens) 
  if token_types[0] == "Token.Keyword.DML":
    if tokens[0].value.lower() == "select":
      select_query = SelectQuery()

      if str(tokens[1].ttype) == 'Token.Wildcard':
        select_query.to_project = '*'
      elif tokens[1].__class__.__name__ == 'IdentifierList': 
        select_query.to_project = [identifier.value for identifier in tokens[1].get_sublists()]
      else:
        select_query.to_project = [tokens[1].value]

      select_query.source = tokens[3].value
      select_query.conditions = []
      where = [x for x in tokens if x.__class__.__name__ == "Where"]
      if len(where) > 0:
        select_query.conditions = []
        for condition in list(where[0].get_sublists()):
          select_query.conditions.append([x for x in condition.flatten() if not x.is_whitespace()])

      rows = state[select_query.source]
      selected_rows = []
      for row in rows:
        match_failed = False
        for condition in select_query.conditions:
          if row[condition[0].value] != condition[2].value.replace("'", ""):
            match_failed = True
            break
        if not match_failed:
          selected_rows.append(row)

      projected_rows = [] 
      if select_query.to_project == '*':
        projected_rows = selected_rows
      else:
        for row in selected_rows:
          projected_row = dict((column_name, row[column_name]) for column_name in select_query.to_project)
          projected_rows.append(projected_row)

      return projected_rows

    else:
      raise QueryGrammarNotRecognized(token_types)
  else:
    raise QueryGrammarNotRecognized(token_types)
 
def get_token_types(tokens):
  token_types = []
  for token in tokens:
    if token.ttype is None:
      token_types.append(token.__class__.__name__)
    else:
      token_types.append(str(token.ttype))
  return token_types
#  import pdb; pdb.set_trace()
#  print token_types

class SelectQuery(object):
  def __init__(self):
    self.to_project = None
    self.source = None
    self.conditions = []


class QueryGrammarNotRecognized(Exception):
  pass
      
