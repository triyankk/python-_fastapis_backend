from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: int
    __name__: str

    # Generate tablename automatically if not defined in model
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
