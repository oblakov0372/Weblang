from models.maintance import Maintenance
from repositories.repository import SQLAlchemyRepository


class MaintenanceRepository(SQLAlchemyRepository):
    model = Maintenance
