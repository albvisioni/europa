// Mock data for Europa game
export const mockUsers = [
  {
    id: 1,
    username: 'kaiser_wilhelm',
    email: 'wilhelm@europa.com',
    country: 'germany',
    level: 12,
    experience: 2847,
    gold: 1250,
    strength: 845,
    rank: 'Lieutenant'
  }
];

export const mockCountries = [
  // Ballkani dhe Europa Juglindore
  { code: 'AL', name: 'Shqipëria', flag: '🇦🇱', players: 2156, regions: ['Tirana', 'Shkodra', 'Korça', 'Vlora'], capital: 'Tirana', power: 45234 },
  { code: 'XK', name: 'Kosova', flag: '🇽🇰', players: 1842, regions: ['Prishtina', 'Prizren', 'Peja', 'Gjilan'], capital: 'Prishtina', power: 32145 },
  { code: 'MK', name: 'Maqedonia e Veriut', flag: '🇲🇰', players: 1654, regions: ['Shkupi', 'Kumanova', 'Tetova', 'Ohri'], capital: 'Shkupi', power: 29876 },
  { code: 'RS', name: 'Serbia', flag: '🇷🇸', players: 2987, regions: ['Beograd', 'Novi Sad', 'Kragujevac', 'Subotica'], capital: 'Beograd', power: 58123 },
  { code: 'GR', name: 'Greqia', flag: '🇬🇷', players: 3245, regions: ['Athina', 'Selanik', 'Patras', 'Kreta'], capital: 'Athina', power: 62341 },
  { code: 'ME', name: 'Mali i Zi', flag: '🇲🇪', players: 987, regions: ['Podgorica', 'Cetinja', 'Bar', 'Ulqin'], capital: 'Podgorica', power: 18765 },
  { code: 'BA', name: 'Bosnja dhe Hercegovina', flag: '🇧🇦', players: 2134, regions: ['Sarajeva', 'Banja Luka', 'Tuzla', 'Mostar'], capital: 'Sarajeva', power: 41523 },
  { code: 'SI', name: 'Sllovenia', flag: '🇸🇮', players: 1876, regions: ['Ljubljana', 'Maribor', 'Celje', 'Kranj'], capital: 'Ljubljana', power: 35687 },
  { code: 'HR', name: 'Kroacia', flag: '🇭🇷', players: 2543, regions: ['Zagreb', 'Split', 'Rijeka', 'Osijek'], capital: 'Zagreb', power: 49123 },
  { code: 'RO', name: 'Rumania', flag: '🇷🇴', players: 3456, regions: ['Bukuresht', 'Cluj-Napoca', 'Timisoara', 'Iasi'], capital: 'Bukuresht', power: 66789 },
  { code: 'BG', name: 'Bulgaria', flag: '🇧🇬', players: 2876, regions: ['Sofia', 'Plovdiv', 'Varna', 'Burgas'], capital: 'Sofia', power: 55432 },

  // Europa Lindore
  { code: 'TR', name: 'Turqia', flag: '🇹🇷', players: 5432, regions: ['Istanbul', 'Ankara', 'Izmir', 'Bursa'], capital: 'Ankara', power: 98765 },
  { code: 'MD', name: 'Moldavia', flag: '🇲🇩', players: 1234, regions: ['Chisinau', 'Tiraspol', 'Balti', 'Bender'], capital: 'Chisinau', power: 23456 },
  { code: 'UA', name: 'Ukraina', flag: '🇺🇦', players: 4987, regions: ['Kiev', 'Kharkiv', 'Odesa', 'Dnipro'], capital: 'Kiev', power: 89432 },
  { code: 'BY', name: 'Bjellorusia', flag: '🇧🇾', players: 2345, regions: ['Minsk', 'Gomel', 'Mogilev', 'Vitebsk'], capital: 'Minsk', power: 43567 },
  { code: 'LV', name: 'Letonia', flag: '🇱🇻', players: 1432, regions: ['Riga', 'Daugavpils', 'Liepaja', 'Jelgava'], capital: 'Riga', power: 27654 },
  { code: 'EE', name: 'Estonia', flag: '🇪🇪', players: 1198, regions: ['Tallinn', 'Tartu', 'Narva', 'Parnu'], capital: 'Tallinn', power: 23876 },
  { code: 'LT', name: 'Lituania', flag: '🇱🇹', players: 1567, regions: ['Vilnius', 'Kaunas', 'Klaipeda', 'Siauliai'], capital: 'Vilnius', power: 29123 },
  { code: 'RU', name: 'Rusia', flag: '🇷🇺', players: 8765, regions: ['Moskva', 'Sankt-Petersburg', 'Novosibirsk', 'Ekaterinburg'], capital: 'Moskva', power: 156789 },

  // Europa Qendrore
  { code: 'HU', name: 'Hungaria', flag: '🇭🇺', players: 2987, regions: ['Budapest', 'Debrecen', 'Szeged', 'Miskolc'], capital: 'Budapest', power: 56234 },
  { code: 'PL', name: 'Polonia', flag: '🇵🇱', players: 4321, regions: ['Varshava', 'Krakow', 'Lodz', 'Wroclaw'], capital: 'Varshava', power: 78456 },
  { code: 'SK', name: 'Sllovakia', flag: '🇸🇰', players: 1876, regions: ['Bratislava', 'Kosice', 'Presov', 'Zilina'], capital: 'Bratislava', power: 34567 },
  { code: 'CZ', name: 'Republika Çeke', flag: '🇨🇿', players: 2654, regions: ['Praga', 'Brno', 'Ostrava', 'Plzen'], capital: 'Praga', power: 49876 },

  // Europa Perëndimore
  { code: 'DE', name: 'Gjermania', flag: '🇩🇪', players: 6543, regions: ['Berlin', 'München', 'Hamburg', 'Köln'], capital: 'Berlin', power: 123456 },
  { code: 'FR', name: 'Franca', flag: '🇫🇷', players: 5987, regions: ['Paris', 'Lyon', 'Marseille', 'Toulouse'], capital: 'Paris', power: 112345 },
  { code: 'CH', name: 'Zvicra', flag: '🇨🇭', players: 2134, regions: ['Bern', 'Zürich', 'Basel', 'Genève'], capital: 'Bern', power: 45678 },
  { code: 'AT', name: 'Austria', flag: '🇦🇹', players: 2345, regions: ['Wien', 'Graz', 'Linz', 'Salzburg'], capital: 'Wien', power: 43212 },
  { code: 'IT', name: 'Italia', flag: '🇮🇹', players: 5432, regions: ['Roma', 'Milano', 'Napoli', 'Torino'], capital: 'Roma', power: 98765 },
  { code: 'GB', name: 'Anglia', flag: '🇬🇧', players: 5678, regions: ['Londra', 'Manchester', 'Birmingham', 'Liverpool'], capital: 'Londra', power: 105432 },
  { code: 'IE', name: 'Irlanda', flag: '🇮🇪', players: 1654, regions: ['Dublin', 'Cork', 'Galway', 'Limerick'], capital: 'Dublin', power: 32145 },
  { code: 'NL', name: 'Holanda', flag: '🇳🇱', players: 3456, regions: ['Amsterdam', 'Rotterdam', 'Haga', 'Utrecht'], capital: 'Amsterdam', power: 65432 },
  { code: 'BE', name: 'Belgjika', flag: '🇧🇪', players: 2543, regions: ['Bruksel', 'Antwerp', 'Ghent', 'Charleroi'], capital: 'Bruksel', power: 47891 },
  { code: 'ES', name: 'Spanja', flag: '🇪🇸', players: 4876, regions: ['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], capital: 'Madrid', power: 89234 },
  { code: 'PT', name: 'Portugalia', flag: '🇵🇹', players: 2345, regions: ['Lisbona', 'Porto', 'Braga', 'Coimbra'], capital: 'Lisbona', power: 43567 },

  // Ishujt
  { code: 'CY', name: 'Qipro', flag: '🇨🇾', players: 987, regions: ['Nicosia', 'Limassol', 'Larnaca', 'Paphos'], capital: 'Nicosia', power: 18765 },
  { code: 'MT', name: 'Malta', flag: '🇲🇹', players: 543, regions: ['Valletta', 'Birkirkara', 'Mosta', 'Qormi'], capital: 'Valletta', power: 12345 },

  // Azia
  { code: 'CN', name: 'Kina', flag: '🇨🇳', players: 15432, regions: ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen'], capital: 'Beijing', power: 289765 },
  { code: 'JP', name: 'Japonia', flag: '🇯🇵', players: 7654, regions: ['Tokyo', 'Osaka', 'Kyoto', 'Yokohama'], capital: 'Tokyo', power: 145632 },
  { code: 'SA', name: 'Arabia Saudite', flag: '🇸🇦', players: 3456, regions: ['Riyadh', 'Jeddah', 'Mecca', 'Medina'], capital: 'Riyadh', power: 67891 },
  { code: 'IL', name: 'Izraeli', flag: '🇮🇱', players: 2134, regions: ['Jerusalem', 'Tel Aviv', 'Haifa', 'Beersheba'], capital: 'Jerusalem', power: 41234 },
  { code: 'PS', name: 'Palestina', flag: '🇵🇸', players: 1876, regions: ['Ramallah', 'Gaza', 'Hebron', 'Nablus'], capital: 'Ramallah', power: 35678 },
  { code: 'SY', name: 'Siria', flag: '🇸🇾', players: 2543, regions: ['Damascus', 'Aleppo', 'Homs', 'Latakia'], capital: 'Damascus', power: 47123 },
  { code: 'IR', name: 'Irani', flag: '🇮🇷', players: 4321, regions: ['Tehran', 'Isfahan', 'Mashhad', 'Shiraz'], capital: 'Tehran', power: 78945 },
  { code: 'IQ', name: 'Iraku', flag: '🇮🇶', players: 3245, regions: ['Baghdad', 'Basra', 'Erbil', 'Mosul'], capital: 'Baghdad', power: 59876 },

  // Afrika
  { code: 'EG', name: 'Egjipti', flag: '🇪🇬', players: 4567, regions: ['Cairo', 'Alexandria', 'Giza', 'Luxor'], capital: 'Cairo', power: 83451 },

  // Amerika Veriore
  { code: 'US', name: 'SHBA', flag: '🇺🇸', players: 12345, regions: ['Washington DC', 'New York', 'Los Angeles', 'Chicago'], capital: 'Washington DC', power: 234567 },
  { code: 'CA', name: 'Kanadaja', flag: '🇨🇦', players: 4321, regions: ['Ottawa', 'Toronto', 'Montreal', 'Vancouver'], capital: 'Ottawa', power: 78912 },
  { code: 'MX', name: 'Meksika', flag: '🇲🇽', players: 3456, regions: ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla'], capital: 'Mexico City', power: 65789 }
];

export const mockBattles = [
  {
    id: 1,
    region: 'Alsace',
    attacker: 'France',
    defender: 'Germany',
    status: 'ongoing',
    timeLeft: '2h 45m',
    attackerDamage: 45823,
    defenderDamage: 52341
  },
  {
    id: 2,
    region: 'Catalonia',
    attacker: 'Spain',
    defender: 'France',
    status: 'victory',
    result: 'Victory',
    attackerDamage: 98234,
    defenderDamage: 76543
  },
  {
    id: 3,
    region: 'Silesia',
    attacker: 'Poland',
    defender: 'Germany',
    status: 'defeat',
    result: 'Defeat',
    attackerDamage: 67890,
    defenderDamage: 89234
  }
];

export const mockCompanies = [
  {
    id: 1,
    name: 'Munich Steel Works',
    type: 'Raw Materials',
    owner: 'kaiser_wilhelm',
    employees: 45,
    dailyProfit: 2450,
    quality: 5,
    country: 'germany'
  },
  {
    id: 2,
    name: 'Berlin Tech Hub',
    type: 'Moving Tickets',
    owner: 'kaiser_wilhelm',
    employees: 32,
    dailyProfit: 1890,
    quality: 4,
    country: 'germany'
  },
  {
    id: 3,
    name: 'Hamburg Logistics',
    type: 'Food',
    owner: 'kaiser_wilhelm',
    employees: 28,
    dailyProfit: 1234,
    quality: 3,
    country: 'germany'
  }
];

export const mockPoliticalParties = [
  {
    id: 1,
    name: 'European Unity Party',
    country: 'germany',
    members: 245,
    ideology: 'Centrist',
    leader: 'angela_merkel_2024'
  },
  {
    id: 2,
    name: 'German Progressive Alliance',
    country: 'germany',
    members: 189,
    ideology: 'Liberal',
    leader: 'progressive_leader'
  },
  {
    id: 3,
    name: 'National Conservative Union',
    country: 'germany',
    members: 167,
    ideology: 'Conservative',
    leader: 'conservative_chief'
  }
];

export const mockNews = [
  {
    id: 1,
    title: 'France declares war on Spain over territory dispute',
    content: 'Tensions escalate as French forces mobilize along the Spanish border...',
    type: 'military',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
    author: 'EuropaNews'
  },
  {
    id: 2,
    title: 'New economic policies announced in Germany',
    content: 'The German government introduces new tax reforms to boost economic growth...',
    type: 'politics',
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
    author: 'PoliticalReporter'
  },
  {
    id: 3,
    title: 'Italy elects new president in close election',
    content: 'After a heated campaign, Italy chooses its new leader by a narrow margin...',
    type: 'politics',
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
    author: 'ElectionWatch'
  },
  {
    id: 4,
    title: 'Battle for Alsace region intensifies',
    content: 'Military forces clash in the strategic Alsace region as the conflict escalates...',
    type: 'military',
    timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000), // 8 hours ago
    author: 'MilitaryCorrespondent'
  }
];

// Mock authentication functions
export const mockAuth = {
  login: (credentials) => {
    const user = mockUsers.find(u => u.email === credentials.email);
    if (user && credentials.password) {
      return { success: true, user };
    }
    return { success: false, error: 'Invalid credentials' };
  },
  
  register: (userData) => {
    const newUser = {
      id: mockUsers.length + 1,
      username: userData.username,
      email: userData.email,
      country: userData.country,
      level: 1,
      experience: 0,
      gold: 100,
      strength: 10,
      rank: 'Recruit'
    };
    mockUsers.push(newUser);
    return { success: true, user: newUser };
  }
};

export const formatTimeAgo = (timestamp) => {
  const now = new Date();
  const diff = now - timestamp;
  const hours = Math.floor(diff / (1000 * 60 * 60));
  
  if (hours < 1) {
    const minutes = Math.floor(diff / (1000 * 60));
    return `${minutes} minutes ago`;
  } else if (hours < 24) {
    return `${hours} hours ago`;
  } else {
    const days = Math.floor(hours / 24);
    return `${days} days ago`;
  }
};