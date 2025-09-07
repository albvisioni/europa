# Europa - API Contracts & Integration Plan

## 1. DATABASE MODELS

### User Model
```javascript
{
  _id: ObjectId,
  username: String (unique),
  email: String (unique),
  password: String (bcrypt hashed),
  country: String (country code),
  level: Number (default: 1),
  experience: Number (default: 0),
  gold: Number (default: 100),
  strength: Number (default: 10),
  rank: String (default: "Recruit"),
  politicalParty: ObjectId (ref: PoliticalParty),
  companies: [ObjectId] (ref: Company),
  achievements: [String],
  createdAt: Date,
  updatedAt: Date,
  isAdmin: Boolean (default: false),
  isBanned: Boolean (default: false)
}
```

### Country Model
```javascript
{
  _id: ObjectId,
  code: String (unique),
  name: String,
  flag: String,
  regions: [String],
  capital: String,
  totalPower: Number,
  totalPlayers: Number,
  currentPresident: ObjectId (ref: User),
  createdAt: Date
}
```

### Battle Model
```javascript
{
  _id: ObjectId,
  region: String,
  attacker: String (country code),
  defender: String (country code),
  status: String (ongoing/victory/defeat),
  startTime: Date,
  endTime: Date,
  attackerDamage: Number,
  defenderDamage: Number,
  participants: [{
    user: ObjectId (ref: User),
    damage: Number,
    side: String (attacker/defender)
  }],
  winner: String (country code)
}
```

### Company Model
```javascript
{
  _id: ObjectId,
  name: String,
  type: String (Raw Materials/Food/Weapons/etc),
  owner: ObjectId (ref: User),
  country: String (country code),
  employees: [ObjectId] (ref: User),
  quality: Number (1-5),
  dailyProfit: Number,
  productivity: Number,
  createdAt: Date
}
```

### PoliticalParty Model
```javascript
{
  _id: ObjectId,
  name: String,
  country: String (country code),
  leader: ObjectId (ref: User),
  members: [ObjectId] (ref: User),
  ideology: String,
  description: String,
  createdAt: Date
}
```

### News Model
```javascript
{
  _id: ObjectId,
  title: String,
  content: String,
  type: String (military/politics/economy),
  author: String,
  timestamp: Date,
  isGlobal: Boolean,
  countries: [String] (country codes affected)
}
```

### Message Model (NEW FEATURE)
```javascript
{
  _id: ObjectId,
  from: ObjectId (ref: User),
  to: ObjectId (ref: User),
  subject: String,
  content: String,
  isRead: Boolean (default: false),
  timestamp: Date
}
```

### Market Model (NEW FEATURE)
```javascript
{
  _id: ObjectId,
  seller: ObjectId (ref: User),
  item: String,
  quantity: Number,
  price: Number,
  country: String (country code),
  isActive: Boolean (default: true),
  createdAt: Date
}
```

### League Model (NEW FEATURE)
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  countries: [String] (country codes),
  type: String (military/economic/political),
  leader: String (country code),
  createdAt: Date
}
```

## 2. API ENDPOINTS

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user profile

### User Endpoints
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `GET /api/users/:id` - Get user by ID
- `GET /api/users/rankings` - Get user rankings

### Country Endpoints
- `GET /api/countries` - Get all countries
- `GET /api/countries/:code` - Get country details
- `GET /api/countries/:code/users` - Get users by country
- `PUT /api/countries/:code` - Update country info (admin only)

### Battle Endpoints
- `GET /api/battles` - Get active battles
- `GET /api/battles/:id` - Get battle details
- `POST /api/battles/:id/fight` - Join battle
- `POST /api/battles` - Create battle (admin only)

### Company Endpoints
- `GET /api/companies` - Get all companies
- `GET /api/companies/:id` - Get company details
- `POST /api/companies` - Create company
- `PUT /api/companies/:id` - Update company
- `DELETE /api/companies/:id` - Delete company
- `POST /api/companies/:id/work` - Work in company

### Political Endpoints
- `GET /api/politics/parties` - Get political parties
- `GET /api/politics/parties/:id` - Get party details
- `POST /api/politics/parties` - Create party
- `POST /api/politics/parties/:id/join` - Join party
- `POST /api/politics/elections` - Start election (admin)

### News Endpoints
- `GET /api/news` - Get news feed
- `POST /api/news` - Create news (admin only)
- `GET /api/news/:id` - Get news details

### Message Endpoints (NEW)
- `GET /api/messages` - Get user messages
- `POST /api/messages` - Send message
- `PUT /api/messages/:id/read` - Mark as read
- `DELETE /api/messages/:id` - Delete message

### Market Endpoints (NEW)
- `GET /api/market` - Get market listings
- `POST /api/market` - Create listing
- `POST /api/market/:id/buy` - Buy item
- `DELETE /api/market/:id` - Remove listing

### League Endpoints (NEW)
- `GET /api/leagues` - Get all leagues
- `POST /api/leagues` - Create league
- `POST /api/leagues/:id/join` - Join league
- `DELETE /api/leagues/:id/leave` - Leave league

### Admin Endpoints (NEW)
- `GET /api/admin/users` - Get all users (admin only)
- `PUT /api/admin/users/:id/ban` - Ban user (admin only)
- `PUT /api/admin/users/:id/unban` - Unban user (admin only)
- `GET /api/admin/stats` - Get system statistics
- `POST /api/admin/news` - Create global news
- `PUT /api/admin/battles/:id` - Modify battle
- `DELETE /api/admin/battles/:id` - Delete battle

## 3. MOCK DATA TO REPLACE

### Frontend Mock Files to Replace:
- `mockUsers` → Real user authentication & profiles
- `mockCountries` → Database-driven country data
- `mockBattles` → Real-time battle system
- `mockCompanies` → User-owned companies with real economics
- `mockPoliticalParties` → Dynamic political system
- `mockNews` → Admin-generated news system

### New Features to Add:
1. **Message System** - Private messaging between users
2. **Marketplace** - Buy/sell items and resources
3. **Leagues** - Country alliances and coalitions
4. **Achievement System** - Unlockable achievements
5. **Admin Panel** - Complete game management system
6. **Real-time Notifications** - Battle updates, messages, etc.

## 4. FRONTEND INTEGRATION PLAN

### Authentication Integration:
- Replace mock auth with JWT-based authentication
- Add token storage and refresh logic
- Implement protected routes

### Dashboard Integration:
- Connect to real user stats from database
- Real-time battle participation
- Live company management
- Dynamic political party membership

### New Components to Add:
- `MessagingSystem.js` - Inbox, compose, message threads
- `Marketplace.js` - Buy/sell interface
- `LeagueManagement.js` - Alliance system
- `AdminPanel.js` - Complete admin dashboard
- `Achievements.js` - Achievement tracking
- `Notifications.js` - Real-time notifications

### Enhanced Features:
- **Battle System**: Real damage calculation, live updates
- **Economic System**: Supply/demand pricing, resource management
- **Political System**: Elections, voting, policy implementation
- **Social Features**: Friend lists, messaging, alliances

## 5. SECURITY & VALIDATION

### Authentication:
- JWT tokens with expiration
- Password hashing with bcrypt
- Rate limiting for API endpoints
- Input validation and sanitization

### Authorization:
- User role-based permissions
- Admin-only endpoints protection
- Country-specific data access control
- Company ownership validation

### Data Protection:
- MongoDB input sanitization
- XSS protection
- CORS configuration
- Environment variable security

This comprehensive backend will transform Europa from a mock application into a fully functional multiplayer strategy game with real user accounts, persistent data, and advanced features like messaging, marketplace, and admin management.