from dataclasses import dataclass


@dataclass
class Payment:
    payment_id: str
    customer_id: str
    amount: float
    payment_method: str
    status: str = "created"
    failure_reason: str | None = None
    attempts: int = 0