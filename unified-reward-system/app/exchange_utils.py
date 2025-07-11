from app import db
from app.models import UserPoints, LiquidityPool, SmartExchange, Merchant
import requests
import logging
from flask import flash, redirect, url_for
from flask_login import current_user
from app.bpv_updater import get_merchant_bpv  # ✅ Fetch BPV dynamically
from app.tasks import process_smart_exchanges  # ✅ Ensure Celery task is correctly imported

# ✅ Initialize Logging
logging.basicConfig(level=logging.INFO)

def update_merchant_api(from_merchant, to_merchant):
    """Sends updated user points to merchants after an exchange."""
    merchants = {m.id: m for m in Merchant.query.all()}

    for merchant_id, merchant in merchants.items():
        user_points = UserPoints.query.filter_by(user_id=current_user.id, merchant_id=merchant.id).first()
        points = user_points.points if user_points else 0

        payload = {
            "user_phone": current_user.phone,
            "points_change": points  # ✅ Fixed key
        }

        merchant_url = f"{merchant.api_url}/rewards/update"  # ✅ Ensure correct API path
        print(f"🚀 Sending API Update to {merchant.name}: {merchant_url} with {payload}")

        try:
            response = requests.post(merchant_url, json=payload)
            response_data = response.json() if response.status_code == 200 else {}

            print(f"✅ API Update for {merchant.name}: {response.status_code}, {response_data}")

        except Exception as e:
            print(f"❌ Failed to update {merchant.name}: {e}")

def process_instant_exchange(from_merchant, to_merchant, amount, converted_amount):
    """Handles instant exchange by transferring points and updating liquidity pools."""
    logging.info(f"🔹 Instant Exchange: {amount} points {from_merchant.name} → {to_merchant.name}")

    try:
        with db.session.begin_nested():  # ✅ Use `begin_nested()` to prevent conflicts
            from_pool = LiquidityPool.query.filter_by(merchant_id=from_merchant.id).with_for_update().first()
            to_pool = LiquidityPool.query.filter_by(merchant_id=to_merchant.id).with_for_update().first()

            if not from_pool or not to_pool or from_pool.balance < amount:
                return {"error": "Liquidity pool issue, try Smart Exchange."}, 400

            user_points_from = UserPoints.query.filter_by(user_id=current_user.id, merchant_id=from_merchant.id).with_for_update().first()
            user_points_to = UserPoints.query.filter_by(user_id=current_user.id, merchant_id=to_merchant.id).with_for_update().first()

            if not user_points_from or user_points_from.points < amount:
                return {"error": "Not enough points."}, 400

            # ✅ Ensure user_points_to exists
            if not user_points_to:
                user_points_to = UserPoints(user_id=current_user.id, merchant_id=to_merchant.id, points=0)
                db.session.add(user_points_to)

            # ✅ Process exchange
            user_points_from.points -= amount
            user_points_to.points += converted_amount
            from_pool.balance -= amount
            to_pool.balance += converted_amount

            db.session.commit()  # ✅ Commit AFTER exiting the transaction block

        # ✅ Update Merchant APIs AFTER committing database changes
        update_merchant_api(from_merchant, to_merchant)

        return {"success": True, "message": f"Converted {amount} points from {from_merchant.name} to {converted_amount} {to_merchant.name} points."}, 200
    except Exception as e:
        db.session.rollback()  # ✅ Rollback transaction if there's an error
        logging.error(f"❌ Instant Exchange Failed: {e}")
        return {"error": "Transaction failed, please try again."}, 500

def process_smart_exchange(from_merchant, to_merchant, amount):
    """Handles Smart Exchange request and triggers Celery."""
    logging.info(f"🔹 Smart Exchange: {amount} points {from_merchant.name} → {to_merchant.name}")

    try:
        with db.session.begin():  # ✅ Use `begin()` instead of `begin_nested()`
            # ✅ Fetch BPV for both merchants
            from_bpv = get_merchant_bpv(from_merchant)
            to_bpv = get_merchant_bpv(to_merchant)

            # ✅ Calculate exchange rate using BPV (Fair conversion)
            conversion_rate = from_bpv / max(to_bpv, 0.0001)  # Prevent division errors
            converted_amount = int(amount * conversion_rate)

            # ✅ Store Smart Exchange request in DB
            new_order = SmartExchange(
                user_id=current_user.id,
                from_merchant_id=from_merchant.id,
                to_merchant_id=to_merchant.id,
                amount=amount,
                status="pending"
            )
            db.session.add(new_order)

            db.session.commit()  # ✅ Ensure transaction is committed before Celery task

        flash(f"Smart Exchange request for {amount} points submitted. Processing...", "info")

        # ✅ Trigger Celery task to process cyclic matching
        process_smart_exchanges.delay()

    except Exception as e:
        db.session.rollback()  # ✅ Rollback transaction on error
        logging.error(f"❌ Smart Exchange Failed: {e}")
        flash("Transaction failed, please try again.", "error")

    return redirect(url_for("main.dashboard"))
