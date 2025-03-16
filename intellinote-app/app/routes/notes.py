# app/routes/notes.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas, ai_services, auth
from app.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    # Fetch user
    result = await db.execute(select(models.User).filter(models.User.user_id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/notes", response_model=schemas.NoteOut)
async def create_note(note: schemas.NoteCreate,
                      db: AsyncSession = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)):
    note_obj = models.Note(
        user_id=current_user.user_id,
        title=note.title,
        content=note.content
    )
    db.add(note_obj)
    await db.commit()
    await db.refresh(note_obj)
    return note_obj

@router.get("/notes", response_model=List[schemas.NoteOut])
async def read_notes(db: AsyncSession = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Note).filter(models.Note.user_id == current_user.user_id))
    notes = result.scalars().all()
    return notes

@router.get("/notes/{note_id}", response_model=schemas.NoteOut)
async def read_note(note_id: uuid.UUID,
                    db: AsyncSession = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Note).filter(
        models.Note.note_id == note_id,
        models.Note.user_id == current_user.user_id
    ))
    note_obj = result.scalars().first()
    if not note_obj:
        raise HTTPException(status_code=404, detail="Note not found")
    return note_obj

@router.put("/notes/{note_id}", response_model=schemas.NoteOut)
async def update_note(note_id: uuid.UUID,
                      note_update: schemas.NoteUpdate,
                      db: AsyncSession = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Note).filter(
        models.Note.note_id == note_id,
        models.Note.user_id == current_user.user_id
    ))
    note_obj = result.scalars().first()
    if not note_obj:
        raise HTTPException(status_code=404, detail="Note not found")

    note_obj.title = note_update.title
    note_obj.content = note_update.content
    await db.commit()
    await db.refresh(note_obj)
    return note_obj

@router.delete("/notes/{note_id}")
async def delete_note(note_id: uuid.UUID,
                      db: AsyncSession = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Note).filter(
        models.Note.note_id == note_id,
        models.Note.user_id == current_user.user_id
    ))
    note_obj = result.scalars().first()
    if not note_obj:
        raise HTTPException(status_code=404, detail="Note not found")

    await db.delete(note_obj)
    await db.commit()
    return {"detail": "Note deleted"}

@router.post("/notes/{note_id}/chatgpt-summarize", response_model=schemas.NoteOut)
async def chatgpt_summarize_note(note_id: uuid.UUID,
                                 db: AsyncSession = Depends(get_db),
                                 current_user: models.User = Depends(get_current_user)):
    # Retrieve note
    result = await db.execute(select(models.Note).filter(
        models.Note.note_id == note_id,
        models.Note.user_id == current_user.user_id
    ))
    note_obj = result.scalars().first()
    if not note_obj:
        raise HTTPException(status_code=404, detail="Note not found")

    # Summarize with ChatGPT
    summary = ai_services.chatgpt_summarize(note_obj.content)
    note_obj.summary = summary
    await db.commit()
    await db.refresh(note_obj)
    return note_obj