import pandas as pd
from app.database import session, Order

def export_orders_to_excel(file_name: str = "orders.xlsx"):
    # Bazadan barcha buyurtmalarni olish
    orders = session.query(Order).all()
    
    if not orders:
        return

    # Ma'lumotlarni tayyorlash
    data = []
    for order in orders:
        data.append({
            "ID": order.id,
            "Mijoz ismi": order.customer_name,
            "Baklashka soni": order.water_quantity,
        })

    # DataFrame yaratish
    df = pd.DataFrame(data)

    # Excel faylga yozish
    df.to_excel(file_name, index=False)
