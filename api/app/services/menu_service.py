from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import restaurant_repo, menu_repo
from app.services.restaurant_service import verify_restaurant_ownership
from app.models.user import User
from app.core.errors import AppError

async def add_item_to_menu(db: AsyncSession, restaurant_id: int, user: User, item_data: dict):
    """
    Orkestracija: dohvati restoran, provjeri vlasništvo, dodaj jelo.
    """
    restaurant = await restaurant_repo.get_by_id(db, restaurant_id)
    if not restaurant:
        raise AppError("not_found", "Restoran ne postoji", 404)
    
    # Koristimo postojeću provjeru vlasništva iz restaurant_service
    verify_restaurant_ownership(restaurant, user)
    
    return await menu_repo.create(
        db, 
        name=item_data["name"], 
        price=item_data["price"], 
        restaurant_id=restaurant_id
    )
