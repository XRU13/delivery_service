from fastapi import APIRouter
from app.tasks.price_tasks import update_delivery_prices

tasks_router = APIRouter()

@tasks_router.post('/price-update', status_code=202)
async def trigger_update_delivery_prices():
    task = update_delivery_prices.delay()
    return {'status': 'submitted', 'task_id': task.id}
