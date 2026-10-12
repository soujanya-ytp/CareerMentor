from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.ext.compiler import compiles


@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(_type, _compiler, **_kw) -> str:
    return "JSON"


@compiles(PGUUID, "sqlite")
def compile_uuid_sqlite(_type, _compiler, **_kw) -> str:
    return "CHAR(36)"
