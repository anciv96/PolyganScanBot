from sqlalchemy import Column, Integer, String

from app.models.database import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    transaction_hash = Column(String)

    def __repr__(self) -> str:
        return str(f'<Transaction transaction_hash={self.transaction_hash}')
