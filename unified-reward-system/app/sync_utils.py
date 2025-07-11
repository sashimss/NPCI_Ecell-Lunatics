import requests
from concurrent.futures import ThreadPoolExecutor
from app import db
from app.models import UserPoints, Merchant

def sync_user_points(user, fetch_from_api=True):
    """Sync user points. Fetch from API only during registration, otherwise update API with DB values."""
    if not user or not user.phone:
        return  

    if fetch_from_api:  # Only during registration
        merchants = Merchant.query.all()
        for merchant in merchants:
            try:
                response = requests.get(f"{merchant.api_url}/{user.phone}")
                if response.status_code == 200:
                    points = response.json().get("points", 0)
                    user_points = UserPoints.query.filter_by(user_id=user.id, merchant_id=merchant.id).first()
                    if not user_points:
                        user_points = UserPoints(user_id=user.id, merchant_id=merchant.id, points=points)
                        db.session.add(user_points)
                    else:
                        user_points.points = points
                else:
                    print(f"⚠️ API fetch failed for {merchant.name}")
            except Exception as e:
                print(f"❌ Error fetching points from {merchant.name}: {e}")
        db.session.commit()
    
    else:  # Update API after exchange
        merchants = Merchant.query.all()
        for merchant in merchants:
            user_points = UserPoints.query.filter_by(user_id=user.id, merchant_id=merchant.id).first()
            points = user_points.points if user_points else 0
            try:
                requests.post(f"{merchant.api_url}/update", json={"user_phone": user.phone, "points": points})
            except Exception as e:
                print(f"❌ Failed to update {merchant.name}: {e}")
