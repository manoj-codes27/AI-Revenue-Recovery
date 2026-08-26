from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

from payment import Payment

app = FastAPI()

# Temporary in-memory storage
payments = {}


class PaymentRequest(BaseModel):
    customer_id: str
    amount: float
    payment_method: str


@app.get("/")
def home():
    return {
        "message": "AI Revenue Recovery Agent API is running"
    }


@app.post("/payments")
def create_payment(request: PaymentRequest):

    payment_id = f"P{uuid4().hex[:8]}"

    payment = Payment(
        payment_id=payment_id,
        customer_id=request.customer_id,
        amount=request.amount,
        payment_method=request.payment_method
    )

    payments[payment_id] = payment

    return payment

class FailureRequest(BaseModel):
    failure_reason: str

@app.post("/payments/{payment_id}/retry")
def retry_payment(payment_id: str):

    if payment_id not in payments:
        return {
            "error": "Payment not found"
        }

    payment = payments[payment_id]

    payment.attempts += 1

    # For now, simulate a successful retry
    payment.status = "success"
    payment.failure_reason = None

    return payment
@app.post("/payments/{payment_id}/fail")
def fail_payment(payment_id: str, request: FailureRequest):

    if payment_id not in payments:
        return {
            "error": "Payment not found"
        }

    payment = payments[payment_id]

    payment.status = "failed"
    payment.failure_reason = request.failure_reason

    return payment