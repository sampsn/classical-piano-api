import json
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, desc

from models import Composer, NewComposerRequest, Piece, NewPieceRequest, engine

app = FastAPI()


# with open("composers.json", "r") as f:
#     composers_list: list[dict] = json.load(f)
#
# composers: list[Composer] = [Composer(**composer) for composer in composers_list]
#
# with open("pieces.json", "r") as f:
#     piece_list: list[dict] = json.load(f)
#
# pieces: list[Piece] = [Piece(**piece) for piece in piece_list]
#
# with Session(bind=engine) as session:
#     for composer in composers:
#         session.add(composer)
#         session.commit()
#         session.refresh(composer)
#
# with Session(bind=engine) as session:
#     for piece in pieces:
#         session.add(piece)
#         session.commit()
#         session.refresh(piece)


@app.get("/composers")
async def get_composers():
    with Session(bind=engine) as session:
        composers = session.exec(select(Composer)).all()
        return composers


@app.get("/pieces")
async def get_pieces(comp_id: int | None = None):
    if comp_id is None:
        with Session(bind=engine) as session:
            pieces = session.exec(select(Piece)).all()
            return pieces
    else:
        with Session(bind=engine) as session:
            pieces = session.exec(
                select(Piece).where(Piece.composer_id == comp_id)
            ).all()
            return pieces


@app.post("/composers")
async def create_composer(new_composer: NewComposerRequest):
    with Session(bind=engine) as session:
        last_composer = session.exec(
            select(Composer).order_by(desc(Composer.composer_id))
        ).first()
        new_composer_obj = Composer(
            name=new_composer.name,
            composer_id=last_composer.composer_id + 1,
            home_country=new_composer.home_country,
        )
        session.add(new_composer_obj)
        session.commit()
        session.refresh(new_composer_obj)


@app.post("/pieces")
async def create_piece(new_piece: NewPieceRequest):
    with Session(bind=engine) as session:
        new_piece_obj = Piece(
            name=new_piece.name,
            alt_name=new_piece.alt_name,
            difficulty=new_piece.difficulty,
            composer_id=new_piece.composer_id,
        )
        session.add(new_piece_obj)
        session.commit()
        session.refresh(new_piece_obj)


@app.put("/composers/{composer_id}")
async def update_composer(composer_id: int, updated_composer: NewComposerRequest):
    with Session(bind=engine) as session:
        composer = session.exec(
            select(Composer).where(Composer.composer_id == composer_id)
        ).one()
        composer.name = updated_composer.name
        composer.home_country = updated_composer.home_country
        session.add(composer)
        session.commit()
        session.refresh(composer)


@app.put("/pieces/{piece_name}")
async def update_piece(piece_name: str, updated_piece: Piece):
    with Session(bind=engine) as session:
        piece = session.exec(select(Piece).where(Piece.piece_name == piece_name)).one()
        piece.name = updated_piece.name
        piece.home_country = updated_piece.home_country
        session.add(piece)
        session.commit()
        session.refresh(piece)


@app.delete("/composers/{composer_id}")
async def delete_composer(composer_id: int):
    with Session(bind=engine) as session:
        composer: Composer | None = session.exec(
            select(Composer).where(Composer.composer_id == composer_id)
        ).one_or_none()
        if composer is None:
            raise HTTPException(
                status_code=404, detail="No composer with that ID found."
            )

        session.delete(composer)
        session.commit()
        return {"detail": "Composer deleted successfully."}


@app.delete("/pieces/{piece_name}")
async def delete_piece(piece_name: str):
    with Session(bind=engine) as session:
        piece: Piece | None = session.exec(
            select(Piece).where(Piece.name == piece_name)
        ).one_or_none()
        if piece is None:
            raise HTTPException(
                status_code=404, detail="No piece with that name found."
            )
        session.delete(piece)
        session.commit()
        return {"detail": "Piece deleted successfully."}
