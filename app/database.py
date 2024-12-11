from sqlalchemy import Column, Integer, String, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///water_delivery.db")
Session = sessionmaker(bind=engine)
session = Session()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    water_quantity = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)  # Kenglik
    longitude = Column(Float, nullable=False)  # Uzunlik

def delete_order_by_id(order_id: int):
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        session.delete(order)
        session.commit()
        return f"✅ **Buyurtma {order_id} muvaffaqiyatli o'chirildi.**\n🧾 Ma'lumotlar bazasidan o'chirildi."
    else:
        return f"❌ **Buyurtma {order_id} topilmadi.**\n🔍 Iltimos, ID ni yana bir bor tekshirib ko'ring."

def update_order_quantity(order_id: int, new_quantity: int):
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        order.water_quantity = new_quantity
        session.commit()
        return f"✅ **Buyurtma {order_id} ning baklashkalari soni muvaffaqiyatli yangilandi.**\n🧾 Yangi son: {new_quantity} ta."
    else:
        return f"❌ **Buyurtma {order_id} topilmadi.**\n🔍 Iltimos, ID ni yana bir bor tekshirib ko'ring."


def init_db():
    print("Ma'lumotlar bazasi yaratilmoqda...")
    Base.metadata.create_all(engine)
    print("Ma'lumotlar bazasi tayyor!")
