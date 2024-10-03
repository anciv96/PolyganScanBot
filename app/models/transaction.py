from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, BigInteger

from app.models.database import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, nullable=True)

    def __repr__(self) -> str:
        return str(f'<Transaction transaction_id={self.transaction_id}')
