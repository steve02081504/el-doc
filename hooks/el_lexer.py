"""Pygments lexers and MkDocs hook for EL source code blocks.

The site uses ```el fences throughout. Pygments has no built-in EL lexer, so
this hook registers small RegexLexers before rendering: `el` for source, `eol`
for the data literal format used by project files, and `repl` for interactive
session transcripts. Keeping them here means the site stays self-contained and
no extra package is needed on CI.
"""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import (
    Comment,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Whitespace,
)
from pygments.lexers import _lexer_cache
from pygments.lexers._mapping import LEXERS


# Shared between the source lexer and the REPL lexer's input state.
_EL_CODE_RULES = [
    (r"\s+", Whitespace),
    (r"//[^\n]*", Comment.Single),
    (r"/\*", Comment.Multiline, "comment"),
    (r"`(?:[^`\\]|\\.)*`", String.Backtick),
    (r'"(?:[^"\\]|\\.)*"', String.Double),
    (r"'(?:[^'\\]|\\.)*'", String.Single),
    (r"@[\[({]", Punctuation),
    (r"@[A-Za-z_\u0080-\uffff][\w:]*", Name.Decorator),
    (
        r"\b(fn|class|interface)(\s+)([A-Za-z_\u0080-\uffff][\w]*)",
        bygroups(Keyword.Declaration, Text, Name.Function),
    ),
    (
        r"\b(let|const)(\s+)([A-Za-z_\u0080-\uffff][\w]*)",
        bygroups(Keyword.Declaration, Text, Name.Variable),
    ),
    (
        r"\b(import|export)(\s+)(extern|from|lazy)\b",
        bygroups(Keyword.Namespace, Whitespace, Keyword.Namespace),
    ),
    (
        r"\b(import|export|from|as|extern|lazy)\b",
        Keyword.Namespace,
    ),
    (
        r"\b(if|else|while|do|for|in|switch|case|default|break|continue|"
        r"return|throw|try|catch|finally|new|delete|is|isnot|take|ref|"
        r"rvalue|virtual|override|implicit|super|constructor|destructor|"
        r"operator|static|public|data|match|prove|calc|use|extends|"
        r"implements|enum|typeof|discard)\b",
        Keyword,
    ),
    (r"\b(t|nil|void|true|false|any)\b", Keyword.Constant),
    (r"\b(0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+)\b", Number.Hex),
    (
        r"\b\d[\d_]*(?:\.[\d_]+)?(?:[eE][+-]?\d+)?\b",
        Number,
    ),
    (r"\b[A-Z][A-Za-z0-9_]*\b", Name.Class),
    (r"[A-Za-z_\u0080-\uffff][\w]*", Name),
    (r"===|!==|<=>|\.\.\||\.\.|=>|==|!=|<=|>=|<<|>>|&&|\|\||\+\+|--|"
     r"\?\?=|\?\?|\?\.|\+=|-=|\*=|/=|%=|&=|\|=|\^=|\*\.|\.\*|\./|\.\^|"
     r"[-+*/%^&|!<>=?.:]", Operator),
    (r"[(){}\[\],;]", Punctuation),
]

_COMMENT_RULES = [
    (r"[^*/]+", Comment.Multiline),
    (r"\*/", Comment.Multiline, "#pop"),
    (r"[*/]", Comment.Multiline),
]


class ELLexer(RegexLexer):
    name = "EL"
    aliases = ["el", "els", "evil", "eol"]
    filenames = ["*.el", "*.els", "*.eol", "*.eod"]
    mimetypes = ["text/x-el"]

    tokens = {
        "root": _EL_CODE_RULES,
        "comment": _COMMENT_RULES,
    }


class ELReplLexer(RegexLexer):
    """Interactive `el repl` transcript: `>` prompts, then output lines."""

    name = "EL REPL"
    aliases = ["repl", "el-repl"]
    filenames = []
    mimetypes = ["text/x-el-repl"]

    tokens = {
        "root": [
            (r"^> ", Generic.Prompt, "input"),
            (r"^\.\.\. ", Generic.Prompt, "input"),
            (r"[^\n]+", Generic.Output),
            (r"\n", Whitespace),
        ],
        "input": [
            (r"\n", Whitespace, "#pop"),
            *_EL_CODE_RULES,
        ],
        "comment": _COMMENT_RULES,
    }


# `get_lexer_by_name` walks the LEXERS table and then reads its cache, so
# pre-seeding both is enough and avoids importing this module again by path.
LEXERS["ELLexer"] = (
    "hooks.el_lexer",
    "EL",
    tuple(ELLexer.aliases),
    tuple(ELLexer.filenames),
    tuple(ELLexer.mimetypes),
)
LEXERS["ELReplLexer"] = (
    "hooks.el_lexer",
    "EL REPL",
    tuple(ELReplLexer.aliases),
    tuple(ELReplLexer.filenames),
    tuple(ELReplLexer.mimetypes),
)
_lexer_cache["EL"] = ELLexer
_lexer_cache["EL REPL"] = ELReplLexer


def on_config(config):
    return config
