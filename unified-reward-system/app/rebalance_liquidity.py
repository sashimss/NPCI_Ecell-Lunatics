from app import db, create_app
from app.models import LiquidityPool, Merchant

def rebalance_liquidity():
    """Adjust liquidity pools based on supply-demand every 24 hours."""
    app = create_app()
    with app.app_context():
        merchants = Merchant.query.all()
        updates = []

        for merchant in merchants:
            pool = LiquidityPool.query.filter_by(merchant_id=merchant.id).first()
            if not pool:
                continue

            balance_change = int(min(100, abs(merchant.supply - merchant.demand) * 0.02))  # ✅ Prevents excessive changes
            pool.balance += balance_change if merchant.supply > merchant.demand else -balance_change
            updates.append(pool)

        if updates:
            db.session.bulk_save_objects(updates)
            db.session.commit()

    print("✅ Liquidity Pools Rebalanced")
