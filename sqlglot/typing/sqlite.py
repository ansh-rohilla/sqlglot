from __future__ import annotations

import typing as t

from sqlglot import exp
from sqlglot.typing import EXPRESSION_METADATA

if t.TYPE_CHECKING:
    from sqlglot.optimizer.annotate_types import TypeAnnotator


ANONYMOUS_RETURNS: dict[str, exp.DType] = {
    "CHANGES": exp.DType.BIGINT,
    "DATETIME": exp.DType.VARCHAR,
    "FORMAT": exp.DType.VARCHAR,
    "JULIANDAY": exp.DType.DOUBLE,
    "LAST_INSERT_ROWID": exp.DType.BIGINT,
    "PRINTF": exp.DType.VARCHAR,
    "QUOTE": exp.DType.VARCHAR,
    "RANDOMBLOB": exp.DType.BLOB,
    "SQLITE_COMPILEOPTION_GET": exp.DType.VARCHAR,
    "SQLITE_COMPILEOPTION_USED": exp.DType.INT,
    "SQLITE_OFFSET": exp.DType.BIGINT,
    "SQLITE_SOURCE_ID": exp.DType.VARCHAR,
    "STRFTIME": exp.DType.VARCHAR,
    "TIME": exp.DType.VARCHAR,
    "TIMEDIFF": exp.DType.VARCHAR,
    "TOTAL": exp.DType.DOUBLE,
    "TOTAL_CHANGES": exp.DType.BIGINT,
    "UNIXEPOCH": exp.DType.BIGINT,
    "ZEROBLOB": exp.DType.BLOB,
}


def _annotate_anonymous(self: TypeAnnotator, expression: exp.Anonymous) -> exp.Expr:
    name = expression.name.upper()
    if name in ANONYMOUS_RETURNS:
        return self._set_type(expression, ANONYMOUS_RETURNS[name])
    if name in ("LIKELY", "UNLIKELY", "LIKELIHOOD") and expression.expressions:
        return self._set_type(expression, expression.expressions[0].type)

    return self._set_type(expression, self.schema.get_udf_type(expression))


EXPRESSION_METADATA = {
    **EXPRESSION_METADATA,
    **{
        expr_type: {"returns": exp.DType.VARCHAR}
        for expr_type in {
            exp.Date,
            exp.Hex,
            exp.Replace,
            exp.Soundex,
        }
    },
    **{
        expr_type: {"returns": exp.DType.BIGINT}
        for expr_type in {
            exp.Rand,
        }
    },
    **{
        expr_type: {"returns": exp.DType.BLOB}
        for expr_type in {
            exp.Unhex,
        }
    },
    exp.Anonymous: {"annotator": _annotate_anonymous},
}
