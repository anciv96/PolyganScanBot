from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, BigInteger

from app.models.database import Base


class OurToken(Base):
    __tablename__ = 'our_token'

    id = Column(Integer, primary_key=True)
    token_id = Column(String, nullable=True)

    def __repr__(self) -> str:
        return str(f'<OurToken token_id={self.token_id}')
