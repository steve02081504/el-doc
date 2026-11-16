import unittest

from pygments import lex
from pygments.token import Keyword, Name

from hooks.el_lexer import ELLexer, ELReplLexer


class ELLexerTests(unittest.TestCase):
	def test_declaration_keywords_with_names_and_destructuring(self):
		code = 'let settings = @{ minimum: 3 }\nlet { minimum = 1 } = settings\nconst [first] = values'
		for lexer, source in [(ELLexer(), code), (ELReplLexer(), '> ' + code.replace('\n', '\n> '))]:
			with self.subTest(lexer=lexer.name):
				tokens = list(lex(source, lexer))
				self.assertEqual([value for token, value in tokens if token is Keyword.Declaration], ['let', 'let', 'const'])
				self.assertIn((Name.Variable, 'settings'), tokens)


if __name__ == '__main__':
	unittest.main()
