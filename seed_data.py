"""
Скрипт для генерации тестовых данных
"""
import asyncio
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.models import Activity, Building, Organization, OrganizationPhone
from app.models.associations import organization_activities


class DataFactory:
    """Фабрика для создания тестовых данных"""

    ACTIVITIES_DATA = [
        {"name": "Торговля", "level": 1, "parent_id": None},
        {"name": "Услуги", "level": 1, "parent_id": None},
        {"name": "Производство", "level": 1, "parent_id": None},

        {"name": "Продукты питания", "level": 2, "parent_id": 1},
        {"name": "Одежда и обувь", "level": 2, "parent_id": 1},
        {"name": "Электроника", "level": 2, "parent_id": 1},

        {"name": "Медицинские услуги", "level": 2, "parent_id": 2},
        {"name": "Образование", "level": 2, "parent_id": 2},
        {"name": "Финансовые услуги", "level": 2, "parent_id": 2},

        {"name": "Супермаркеты", "level": 3, "parent_id": 4},
        {"name": "Рестораны", "level": 3, "parent_id": 4},
        {"name": "Поликлиники", "level": 3, "parent_id": 7},
        {"name": "Школы", "level": 3, "parent_id": 8},
        {"name": "Банки", "level": 3, "parent_id": 9},
    ]

    BUILDINGS_DATA = [
        {"address": "ул. Тверская, 1", "latitude": 55.7558,
         "longitude": 37.6176},
        {"address": "ул. Арбат, 15", "latitude": 55.7520,
         "longitude": 37.5925},
        {"address": "пр. Мира, 25", "latitude": 55.7818,
         "longitude": 37.6338},
        {"address": "ул. Ленинский проспект, 50", "latitude": 55.7067,
         "longitude": 37.5858},
        {"address": "ул. Новый Арбат, 10", "latitude": 55.7520,
         "longitude": 37.5925},
        {"address": "ул. Кузнецкий мост, 5", "latitude": 55.7616,
         "longitude": 37.6205},
        {"address": "ул. Петровка, 20", "latitude": 55.7652,
         "longitude": 37.6145},
        {"address": "ул. Сретенка, 30", "latitude": 55.7652,
         "longitude": 37.6205},
        {"address": "ул. Маросейка, 12", "latitude": 55.7558,
         "longitude": 37.6325},
        {"address": "ул. Никольская, 8", "latitude": 55.7558,
         "longitude": 37.6205},
        {"address": "ул. Ильинка, 15", "latitude": 55.7558,
         "longitude": 37.6255},
        {"address": "ул. Варварка, 25", "latitude": 55.7520,
         "longitude": 37.6255},
        {"address": "ул. Покровка, 35", "latitude": 55.7652,
         "longitude": 37.6325},
        {"address": "ул. Мясницкая, 40", "latitude": 55.7652,
         "longitude": 37.6205},
        {"address": "ул. Большая Дмитровка, 18", "latitude": 55.7558,
         "longitude": 37.6145},
    ]

    PHONE_NUMBERS = [
        "+7(495)123-45-67", "+7(495)234-56-78", "+7(495)345-67-89",
        "+7(495)456-78-90", "+7(495)567-89-01", "+7(495)678-90-12",
        "+7(495)789-01-23", "+7(495)890-12-34", "+7(495)901-23-45",
        "+7(495)012-34-56", "+7(495)111-22-33", "+7(495)222-33-44",
        "+7(495)333-44-55", "+7(495)444-55-66", "+7(495)555-66-77",
        "+7(495)666-77-88", "+7(495)777-88-99", "+7(495)888-99-00",
        "+7(495)999-00-11", "+7(495)000-11-22", "+7(495)111-33-44",
        "+7(495)222-44-55", "+7(495)333-55-66", "+7(495)444-66-77",
        "+7(495)555-77-88"
    ]

    ORGANIZATION_NAMES_STATIC = [
        "ООО Торговый дом Продукты", "ИП Компания Одежда",
        "ЗАО Группа Электроника", "ОАО Холдинг Мебель",
        "ПАО Корпорация Медицина", "АО Ассоциация Образование",
        "ТОО Союз Финансы", "ЧП Фонд Транспорт", "ООО Центр Связь",
        "ИП Институт Стройматериалы", "ЗАО Торговый дом Автозапчасти",
        "ОАО Компания Книги", "ПАО Группа Спорттовары",
        "АО Холдинг Косметика", "ТОО Корпорация Игрушки",
        "ЧП Ассоциация Продукты", "ООО Союз Одежда",
        "ИП Фонд Электроника", "ЗАО Центр Мебель",
        "ОАО Институт Медицина", "ПАО Торговый дом Образование",
        "АО Компания Финансы", "ТОО Группа Транспорт",
        "ЧП Холдинг Связь", "ООО Корпорация Стройматериалы"
    ]


async def create_activities(session: AsyncSession) -> List[Activity]:
    """Создает виды деятельности"""
    activities = []

    for activity_data in DataFactory.ACTIVITIES_DATA:
        activity = Activity(
            name=activity_data["name"],
            level=activity_data["level"],
            parent_id=activity_data["parent_id"]
        )
        session.add(activity)
        activities.append(activity)

    await session.commit()
    return activities


async def create_buildings(session: AsyncSession) -> List[Building]:
    """Создает здания"""
    buildings = []

    for building_data in DataFactory.BUILDINGS_DATA:
        building = Building(
            address=building_data["address"],
            latitude=building_data["latitude"],
            longitude=building_data["longitude"]
        )
        session.add(building)
        buildings.append(building)

    await session.commit()
    return buildings


async def create_organizations(
    session: AsyncSession,
    buildings: List[Building],
    activities: List[Activity]
) -> List[Organization]:
    """Создает организации"""
    organizations = []

    for i in range(25):
        building = buildings[i % len(buildings)]

        org = Organization(
            name=DataFactory.ORGANIZATION_NAMES_STATIC[i],
            building_id=building.id
        )
        session.add(org)
        organizations.append(org)

    await session.commit()

    for i, org in enumerate(organizations):
        phone_count = (i % 3) + 1
        for j in range(phone_count):
            phone = OrganizationPhone(
                phone_number=DataFactory.PHONE_NUMBERS[
                    (i * 3 + j) % len(DataFactory.PHONE_NUMBERS)
                ],
                organization_id=org.id
            )
            session.add(phone)

        activity_count = (i % 3) + 1
        start_idx = i % len(activities)
        end_idx = start_idx + activity_count
        selected_activities = activities[start_idx:end_idx]
        if len(selected_activities) < activity_count:
            selected_activities = activities[:activity_count]

        for activity in selected_activities:
            stmt = organization_activities.insert().values(
                organization_id=org.id,
                activity_id=activity.id
            )
            await session.execute(stmt)

    await session.commit()
    return organizations


async def seed_database():
    """Основная функция для заполнения БД тестовыми данными"""
    async with AsyncSessionLocal() as session:
        print("Создание видов деятельности...")
        activities = await create_activities(session)
        print(f"Создано {len(activities)} видов деятельности")

        print("Создание зданий...")
        buildings = await create_buildings(session)
        print(f"Создано {len(buildings)} зданий")

        print("Создание организаций...")
        organizations = await create_organizations(
            session, buildings, activities
        )
        print(f"Создано {len(organizations)} организаций")

        print("Тестовые данные успешно созданы!")


if __name__ == "__main__":
    asyncio.run(seed_database())
