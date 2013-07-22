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
      #SELECT * FROM table
      if token_types == ['Token.Keyword.DML', 'Token.Wildcard', 'Token.Keyword', 'Identifier']:
        table_name = tokens[3].value
        return state[table_name]
      #SELECT column FROM table
      elif token_types == ['Token.Keyword.DML', 'Identifier', 'Token.Keyword', 'Identifier']:
        table_name = tokens[3].value
        column_name = tokens[1].value
        return [{column_name : row[column_name]} for row in state[table_name]]
      else:
        raise QueryGrammarNotRecognized(token_types)
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

class QueryGrammarNotRecognized(Exception):
  pass
      
