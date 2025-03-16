from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas, auth
from app.database import get_db

router = APIRouter()

# Configure templates (assuming your templates folder is at the project root)
templates = Jinja2Templates(directory="templates")

# GET endpoint to serve the registration form
@router.get("/register")
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# POST endpoint to process the registration form
@router.post("/register", response_model=schemas.UserOut)
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Check if user already exists
    result = await db.execute(select(models.User).filter(models.User.email == email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Create a new user
    hashed_password = auth.get_password_hash(password)
    user_obj = models.User(
        username=username,
        email=email,
        password_hash=hashed_password
    )
    db.add(user_obj)
    await db.commit()
    await db.refresh(user_obj)
    return user_obj

# GET endpoint to serve the login form
@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# POST endpoint to process the login form
@router.post("/login", response_model=schemas.Token)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Look up user by email
    result = await db.execute(select(models.User).filter(models.User.email == email))
    user = result.scalars().first()
    if not user or not auth.verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create JWT token
    access_token = auth.create_access_token(data={"user_id": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}