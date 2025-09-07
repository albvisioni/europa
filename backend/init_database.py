#!/usr/bin/env python3
"""
Database initialization script for Europa
Creates initial data including countries, sample users, and news
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# World countries data
WORLD_COUNTRIES = [
    # Ballkani dhe Europa Juglindore
    {'code': 'AL', 'name': 'Shqipëria', 'flag': '🇦🇱', 'regions': ['Tirana', 'Shkodra', 'Korça', 'Vlora'], 'capital': 'Tirana'},
    {'code': 'XK', 'name': 'Kosova', 'flag': '🇽🇰', 'regions': ['Prishtina', 'Prizren', 'Peja', 'Gjilan'], 'capital': 'Prishtina'},
    {'code': 'MK', 'name': 'Maqedonia e Veriut', 'flag': '🇲🇰', 'regions': ['Shkupi', 'Kumanova', 'Tetova', 'Ohri'], 'capital': 'Shkupi'},
    {'code': 'RS', 'name': 'Serbia', 'flag': '🇷🇸', 'regions': ['Beograd', 'Novi Sad', 'Kragujevac', 'Subotica'], 'capital': 'Beograd'},
    {'code': 'GR', 'name': 'Greqia', 'flag': '🇬🇷', 'regions': ['Athina', 'Selanik', 'Patras', 'Kreta'], 'capital': 'Athina'},
    {'code': 'ME', 'name': 'Mali i Zi', 'flag': '🇲🇪', 'regions': ['Podgorica', 'Cetinja', 'Bar', 'Ulqin'], 'capital': 'Podgorica'},
    {'code': 'BA', 'name': 'Bosnja dhe Hercegovina', 'flag': '🇧🇦', 'regions': ['Sarajeva', 'Banja Luka', 'Tuzla', 'Mostar'], 'capital': 'Sarajeva'},
    {'code': 'SI', 'name': 'Sllovenia', 'flag': '🇸🇮', 'regions': ['Ljubljana', 'Maribor', 'Celje', 'Kranj'], 'capital': 'Ljubljana'},
    {'code': 'HR', 'name': 'Kroacia', 'flag': '🇭🇷', 'regions': ['Zagreb', 'Split', 'Rijeka', 'Osijek'], 'capital': 'Zagreb'},
    {'code': 'RO', 'name': 'Rumania', 'flag': '🇷🇴', 'regions': ['Bukuresht', 'Cluj-Napoca', 'Timisoara', 'Iasi'], 'capital': 'Bukuresht'},
    {'code': 'BG', 'name': 'Bulgaria', 'flag': '🇧🇬', 'regions': ['Sofia', 'Plovdiv', 'Varna', 'Burgas'], 'capital': 'Sofia'},

    # Europa Lindore
    {'code': 'TR', 'name': 'Turqia', 'flag': '🇹🇷', 'regions': ['Istanbul', 'Ankara', 'Izmir', 'Bursa'], 'capital': 'Ankara'},
    {'code': 'MD', 'name': 'Moldavia', 'flag': '🇲🇩', 'regions': ['Chisinau', 'Tiraspol', 'Balti', 'Bender'], 'capital': 'Chisinau'},
    {'code': 'UA', 'name': 'Ukraina', 'flag': '🇺🇦', 'regions': ['Kiev', 'Kharkiv', 'Odesa', 'Dnipro'], 'capital': 'Kiev'},
    {'code': 'BY', 'name': 'Bjellorusia', 'flag': '🇧🇾', 'regions': ['Minsk', 'Gomel', 'Mogilev', 'Vitebsk'], 'capital': 'Minsk'},
    {'code': 'LV', 'name': 'Letonia', 'flag': '🇱🇻', 'regions': ['Riga', 'Daugavpils', 'Liepaja', 'Jelgava'], 'capital': 'Riga'},
    {'code': 'EE', 'name': 'Estonia', 'flag': '🇪🇪', 'regions': ['Tallinn', 'Tartu', 'Narva', 'Parnu'], 'capital': 'Tallinn'},
    {'code': 'LT', 'name': 'Lituania', 'flag': '🇱🇹', 'regions': ['Vilnius', 'Kaunas', 'Klaipeda', 'Siauliai'], 'capital': 'Vilnius'},
    {'code': 'RU', 'name': 'Rusia', 'flag': '🇷🇺', 'regions': ['Moskva', 'Sankt-Petersburg', 'Novosibirsk', 'Ekaterinburg'], 'capital': 'Moskva'},

    # Europa Qendrore
    {'code': 'HU', 'name': 'Hungaria', 'flag': '🇭🇺', 'regions': ['Budapest', 'Debrecen', 'Szeged', 'Miskolc'], 'capital': 'Budapest'},
    {'code': 'PL', 'name': 'Polonia', 'flag': '🇵🇱', 'regions': ['Varshava', 'Krakow', 'Lodz', 'Wroclaw'], 'capital': 'Varshava'},
    {'code': 'SK', 'name': 'Sllovakia', 'flag': '🇸🇰', 'regions': ['Bratislava', 'Kosice', 'Presov', 'Zilina'], 'capital': 'Bratislava'},
    {'code': 'CZ', 'name': 'Republika Çeke', 'flag': '🇨🇿', 'regions': ['Praga', 'Brno', 'Ostrava', 'Plzen'], 'capital': 'Praga'},

    # Europa Perëndimore
    {'code': 'DE', 'name': 'Gjermania', 'flag': '🇩🇪', 'regions': ['Berlin', 'München', 'Hamburg', 'Köln'], 'capital': 'Berlin'},
    {'code': 'FR', 'name': 'Franca', 'flag': '🇫🇷', 'regions': ['Paris', 'Lyon', 'Marseille', 'Toulouse'], 'capital': 'Paris'},
    {'code': 'CH', 'name': 'Zvicra', 'flag': '🇨🇭', 'regions': ['Bern', 'Zürich', 'Basel', 'Genève'], 'capital': 'Bern'},
    {'code': 'AT', 'name': 'Austria', 'flag': '🇦🇹', 'regions': ['Wien', 'Graz', 'Linz', 'Salzburg'], 'capital': 'Wien'},
    {'code': 'IT', 'name': 'Italia', 'flag': '🇮🇹', 'regions': ['Roma', 'Milano', 'Napoli', 'Torino'], 'capital': 'Roma'},
    {'code': 'GB', 'name': 'Anglia', 'flag': '🇬🇧', 'regions': ['Londra', 'Manchester', 'Birmingham', 'Liverpool'], 'capital': 'Londra'},
    {'code': 'IE', 'name': 'Irlanda', 'flag': '🇮🇪', 'regions': ['Dublin', 'Cork', 'Galway', 'Limerick'], 'capital': 'Dublin'},
    {'code': 'NL', 'name': 'Holanda', 'flag': '🇳🇱', 'regions': ['Amsterdam', 'Rotterdam', 'Haga', 'Utrecht'], 'capital': 'Amsterdam'},
    {'code': 'BE', 'name': 'Belgjika', 'flag': '🇧🇪', 'regions': ['Bruksel', 'Antwerp', 'Ghent', 'Charleroi'], 'capital': 'Bruksel'},
    {'code': 'ES', 'name': 'Spanja', 'flag': '🇪🇸', 'regions': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], 'capital': 'Madrid'},
    {'code': 'PT', 'name': 'Portugalia', 'flag': '🇵🇹', 'regions': ['Lisbona', 'Porto', 'Braga', 'Coimbra'], 'capital': 'Lisbona'},

    # Europa Veriore
    {'code': 'NO', 'name': 'Norvegjia', 'flag': '🇳🇴', 'regions': ['Oslo', 'Bergen', 'Trondheim', 'Stavanger'], 'capital': 'Oslo'},
    {'code': 'SE', 'name': 'Suedia', 'flag': '🇸🇪', 'regions': ['Stockholm', 'Gothenburg', 'Malmö', 'Uppsala'], 'capital': 'Stockholm'},
    {'code': 'FI', 'name': 'Finlanda', 'flag': '🇫🇮', 'regions': ['Helsinki', 'Espoo', 'Tampere', 'Vantaa'], 'capital': 'Helsinki'},
    {'code': 'DK', 'name': 'Danimarka', 'flag': '🇩🇰', 'regions': ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg'], 'capital': 'Copenhagen'},
    {'code': 'IS', 'name': 'Islanda', 'flag': '🇮🇸', 'regions': ['Reykjavik', 'Akureyri', 'Keflavik', 'Hafnarfjordur'], 'capital': 'Reykjavik'},

    # Ishujt Evropianë
    {'code': 'CY', 'name': 'Qipro', 'flag': '🇨🇾', 'regions': ['Nicosia', 'Limassol', 'Larnaca', 'Paphos'], 'capital': 'Nicosia'},
    {'code': 'MT', 'name': 'Malta', 'flag': '🇲🇹', 'regions': ['Valletta', 'Birkirkara', 'Mosta', 'Qormi'], 'capital': 'Valletta'},

    # Major world countries
    {'code': 'US', 'name': 'SHBA', 'flag': '🇺🇸', 'regions': ['Washington DC', 'New York', 'Los Angeles', 'Chicago'], 'capital': 'Washington DC'},
    {'code': 'CA', 'name': 'Kanadaja', 'flag': '🇨🇦', 'regions': ['Ottawa', 'Toronto', 'Montreal', 'Vancouver'], 'capital': 'Ottawa'},
    {'code': 'CN', 'name': 'Kina', 'flag': '🇨🇳', 'regions': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen'], 'capital': 'Beijing'},
    {'code': 'JP', 'name': 'Japonia', 'flag': '🇯🇵', 'regions': ['Tokyo', 'Osaka', 'Kyoto', 'Yokohama'], 'capital': 'Tokyo'},
    {'code': 'BR', 'name': 'Brazili', 'flag': '🇧🇷', 'regions': ['Brasilia', 'São Paulo', 'Rio de Janeiro', 'Salvador'], 'capital': 'Brasilia'},
    {'code': 'IN', 'name': 'India', 'flag': '🇮🇳', 'regions': ['New Delhi', 'Mumbai', 'Bangalore', 'Chennai'], 'capital': 'New Delhi'},
    {'code': 'AU', 'name': 'Australia', 'flag': '🇦🇺', 'regions': ['Canberra', 'Sydney', 'Melbourne', 'Brisbane'], 'capital': 'Canberra'},
    {'code': 'EG', 'name': 'Egjipti', 'flag': '🇪🇬', 'regions': ['Cairo', 'Alexandria', 'Giza', 'Luxor'], 'capital': 'Cairo'},
    {'code': 'ZA', 'name': 'Afrika e Jugut', 'flag': '🇿🇦', 'regions': ['Cape Town', 'Johannesburg', 'Durban', 'Pretoria'], 'capital': 'Cape Town'}
]

# Sample news
INITIAL_NEWS = [
    {
        'title': 'Mirë se erdhët në Europa!',
        'content': 'Europa është një lojë strategjike në browser që ju lejon të drejtoni vendin tuaj në një botë virtuale. Krijoni kompani, merrni pjesë në beteja, dhe ndikoni në politikën!',
        'type': 'politics',
        'author': 'Sistema e Lajmeve',
        'is_global': True,
        'countries': []
    },
    {
        'title': 'Sistemi ekonomik është aktiv',
        'content': 'Filloni të krijoni kompanitë tuaja dhe të punoni për të fituar para dhe përvojë. Sistemi ekonomik të Europa ofron mundësi të panumërta për t\'u pasuruar!',
        'type': 'economy',
        'author': 'Ekonomisti Kryesor',
        'is_global': True,
        'countries': []
    },
    {
        'title': 'Betejet janë gati për të filluar',
        'content': 'Sistemi ushtarak është aktiv! Administratorët mund të krijojnë beteja të reja dhe lojtarët mund të marrin pjesë për të ndihmuar vendin e tyre.',
        'type': 'military',
        'author': 'Komandanti i Përgjithshëm',
        'is_global': True,
        'countries': []
    }
]

async def init_database():
    """Initialize the Europa database with countries and initial data"""
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'europa_db')
    
    if not mongo_url:
        raise ValueError("MONGO_URL environment variable not set")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print(f"Connected to MongoDB: {db_name}")
    
    try:
        # Initialize countries
        print("Initializing countries...")
        countries_collection = db.countries
        
        # Check if countries already exist
        existing_count = await countries_collection.count_documents({})
        if existing_count > 0:
            print(f"Countries already exist ({existing_count} found). Skipping country initialization.")
        else:
            # Insert countries
            countries_to_insert = []
            for country_data in WORLD_COUNTRIES:
                country = {
                    'code': country_data['code'],
                    'name': country_data['name'],
                    'flag': country_data['flag'],
                    'regions': country_data['regions'],
                    'capital': country_data['capital'],
                    'total_power': 0,
                    'total_players': 0,
                    'current_president': None,
                    'created_at': datetime.utcnow()
                }
                countries_to_insert.append(country)
            
            result = await countries_collection.insert_many(countries_to_insert)
            print(f"Inserted {len(result.inserted_ids)} countries")
        
        # Initialize news
        print("Initializing news...")
        news_collection = db.news
        
        # Check if news already exist
        existing_news = await news_collection.count_documents({})
        if existing_news > 0:
            print(f"News already exist ({existing_news} found). Skipping news initialization.")
        else:
            # Insert initial news
            news_to_insert = []
            for news_data in INITIAL_NEWS:
                news = {
                    'title': news_data['title'],
                    'content': news_data['content'],
                    'type': news_data['type'],
                    'author': news_data['author'],
                    'is_global': news_data['is_global'],
                    'countries': news_data['countries'],
                    'timestamp': datetime.utcnow()
                }
                news_to_insert.append(news)
            
            result = await news_collection.insert_many(news_to_insert)
            print(f"Inserted {len(result.inserted_ids)} news articles")
        
        # Create admin user if it doesn't exist
        print("Checking for admin user...")
        users_collection = db.users
        
        admin_email = "admin@europa.com"
        existing_admin = await users_collection.find_one({"email": admin_email})
        
        if existing_admin:
            print("Admin user already exists")
        else:
            # Create admin user
            admin_user = {
                'username': 'EuropaAdmin',
                'email': admin_email,
                'password': pwd_context.hash('admin123'),  # Change this in production!
                'country': 'al',  # Albania
                'level': 50,
                'experience': 100000,
                'gold': 50000,
                'strength': 1000,
                'rank': 'Supreme Commander',
                'political_party': None,
                'companies': [],
                'achievements': ['system_administrator', 'founder'],
                'is_admin': True,
                'is_banned': False,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            result = await users_collection.insert_one(admin_user)
            print(f"Created admin user with ID: {result.inserted_id}")
            print("Admin credentials: admin@europa.com / admin123")
        
        # Create indexes for better performance
        print("Creating database indexes...")
        
        # User indexes
        await users_collection.create_index("email", unique=True)
        await users_collection.create_index("username", unique=True)
        await users_collection.create_index("country")
        await users_collection.create_index("experience")
        
        # Country indexes
        await countries_collection.create_index("code", unique=True)
        await countries_collection.create_index("total_players")
        
        # Battle indexes
        battles_collection = db.battles
        await battles_collection.create_index("status")
        await battles_collection.create_index("start_time")
        
        # Company indexes
        companies_collection = db.companies
        await companies_collection.create_index("owner")
        await companies_collection.create_index("country")
        
        # News indexes
        await news_collection.create_index("timestamp")
        await news_collection.create_index("type")
        await news_collection.create_index("is_global")
        
        print("Database indexes created successfully")
        
        print("\n✅ Europa database initialized successfully!")
        print("\n🎮 You can now:")
        print("1. Register new users on the website")
        print("2. Login as admin with: admin@europa.com / admin123")
        print("3. Create battles, manage countries, and moderate the game")
        print("4. Start playing Europa!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🚀 Initializing Europa Database...")
    asyncio.run(init_database())