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
  {
    code: 'DE',
    name: 'Germany',
    flag: '🇩🇪',
    players: 4521,
    regions: ['Bavaria', 'Berlin', 'Hamburg', 'Saxony'],
    capital: 'Berlin',
    power: 95432
  },
  {
    code: 'FR',
    name: 'France',
    flag: '🇫🇷',
    players: 3842,
    regions: ['Île-de-France', 'Provence', 'Normandy', 'Alsace'],
    capital: 'Paris',
    power: 87234
  },
  {
    code: 'GB',
    name: 'United Kingdom',
    flag: '🇬🇧',
    players: 3651,
    regions: ['England', 'Scotland', 'Wales', 'Northern Ireland'],
    capital: 'London',
    power: 78956
  },
  {
    code: 'IT',
    name: 'Italy',
    flag: '🇮🇹',
    players: 3204,
    regions: ['Lazio', 'Lombardy', 'Sicily', 'Tuscany'],
    capital: 'Rome',
    power: 72451
  },
  {
    code: 'ES',
    name: 'Spain',
    flag: '🇪🇸',
    players: 2987,
    regions: ['Madrid', 'Catalonia', 'Andalusia', 'Valencia'],
    capital: 'Madrid',
    power: 68934
  },
  {
    code: 'PL',
    name: 'Poland',
    flag: '🇵🇱',
    players: 2743,
    regions: ['Mazovia', 'Silesia', 'Greater Poland', 'Lesser Poland'],
    capital: 'Warsaw',
    power: 65287
  }
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