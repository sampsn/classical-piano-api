from sqlmodel import SQLModel, Field, create_engine
from enum import Enum


DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)


class Composer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    composer_id: int
    home_country: str


class NewComposerRequest(SQLModel):
    name: str
    home_country: str


class Piece(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    alt_name: str | None
    difficulty: int
    composer_id: int | None = Field(default=None, foreign_key="composer.composer_id")


class NewPieceRequest(SQLModel):
    name: str
    alt_name: str
    difficulty: int
    composer_id: int


SQLModel.metadata.create_all(engine)
