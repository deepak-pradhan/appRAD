from typing import Optional
from datetime import date
from backend.models.bases.bmodel import BModel
from sqlmodel import Field, Column, String

class LoanOrCredit(BModel, table=True):
    __tablename__ = "loan_or_credit"

    amount: float = Field(default=0.0)
    currency: str = Field(default="USD")
    lender_name: str = Field(default=None)
    borrower_name: str = Field(default=None)
    date_issued: date = Field(default=None)
    repayment_frequency: str = Field(default=None)
    repayment_term: str = Field(default=None)
    interest_rate: float = Field(default=0.0)
    loan_term: int = Field(default=None)  # in months

    def validate(self) -> None:
        super().validate()
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero")

class Loan(LoanOrCredit, table=True):
    __tablename__ = "loan"
    
    collateral: Optional[str] = Field(default=None)

class Credit(LoanOrCredit, table=True):
    __tablename__ = "credit"
    
    credit_limit: float = Field(default=0.0)

    def validate(self) -> None:
        super().validate()
        if self.credit_limit < 0:
            raise ValueError("Credit limit cannot be negative")