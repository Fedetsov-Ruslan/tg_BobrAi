from sqlalchemy import DateTime, String, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    

class SaveCity(Base):
    __tablename__ = "save_city"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    

class Logs(Base):
    __tablename__ = "logs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    request: Mapped[str] = mapped_column(String(255), nullable=False)
    response: Mapped[str] = mapped_column(String(2000), nullable=False)    
