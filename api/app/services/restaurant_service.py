from app.core.errors import AppError
from app.models.restaurant import Restaurant
from app.models.user import User

def verify_restaurant_ownership(restaurant: Restaurant, user: User):
    """
    Provjerava je li korisnik vlasnik restorana ili admin.
    Ovo je ključno za sigurnost (da jedan vlasnik ne mijenja tuđi meni).
    """
    if user.role == "admin":
        return True
        
    if restaurant.owner_id != user.id:
        raise AppError(
            code="forbidden",
            message="Niste vlasnik ovog restorana",
            status_code=403
        )
    return True
