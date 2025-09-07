import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Progress } from './ui/progress';
import { 
  Crown, 
  Building, 
  Sword, 
  Users, 
  TrendingUp, 
  MapPin, 
  Star,
  Coins,
  Shield,
  Target,
  Award,
  Globe,
  Briefcase,
  Vote,
  Newspaper
} from 'lucide-react';

const Dashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('overview');

  const mockUserStats = {
    level: 12,
    experience: 2847,
    nextLevelExp: 3000,
    gold: 1250,
    strength: 845,
    rank: 'Lieutenant',
    country: 'Germany',
    region: 'Bavaria',
    party: 'European Unity Party',
    company: 'Bavarian Industries',
    battles: 23,
    victories: 18
  };

  const mockNews = [
    { title: 'France declares war on Spain over territory dispute', time: '2 hours ago', type: 'military' },
    { title: 'New economic policies announced in Germany', time: '4 hours ago', type: 'politics' },
    { title: 'Italy elects new president in close election', time: '6 hours ago', type: 'politics' },
    { title: 'Battle for Alsace region intensifies', time: '8 hours ago', type: 'military' }
  ];

  const mockBattles = [
    { region: 'Alsace', attacker: 'France', defender: 'Germany', status: 'ongoing', timeLeft: '2h 45m' },
    { region: 'Catalonia', attacker: 'Spain', defender: 'France', status: 'victory', result: 'Victory' },
    { region: 'Silesia', attacker: 'Poland', defender: 'Germany', status: 'defeat', result: 'Defeat' }
  ];

  const mockCompanies = [
    { name: 'Munich Steel Works', type: 'Raw Materials', employees: 45, profit: '+€2,450', quality: 5 },
    { name: 'Berlin Tech Hub', type: 'Moving Tickets', employees: 32, profit: '+€1,890', quality: 4 },
    { name: 'Hamburg Logistics', type: 'Food', employees: 28, profit: '+€1,234', quality: 3 }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      {/* Header */}
      <header className="bg-black/50 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center">
                <Crown className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-white">EUROPA</h1>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-4 text-white">
                <div className="flex items-center space-x-2">
                  <Coins className="w-5 h-5 text-yellow-400" />
                  <span className="font-semibold">{mockUserStats.gold.toLocaleString()}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Star className="w-5 h-5 text-blue-400" />
                  <span className="font-semibold">Level {mockUserStats.level}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Shield className="w-5 h-5 text-green-400" />
                  <span className="font-semibold">{mockUserStats.strength}</span>
                </div>
              </div>
              <Button 
                variant="outline" 
                onClick={onLogout}
                className="border-white/30 text-white hover:bg-white/10"
              >
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left Sidebar - User Profile */}
          <div className="lg:col-span-1">
            <Card className="bg-white/10 border-white/20 text-white">
              <CardHeader className="text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <Users className="w-10 h-10 text-white" />
                </div>
                <CardTitle className="text-xl">{user?.username || 'Player'}</CardTitle>
                <Badge className="bg-yellow-500 text-black">{mockUserStats.rank}</Badge>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Experience</span>
                    <span>{mockUserStats.experience}/{mockUserStats.nextLevelExp}</span>
                  </div>
                  <Progress 
                    value={(mockUserStats.experience / mockUserStats.nextLevelExp) * 100} 
                    className="h-2"
                  />
                </div>
                
                <div className="space-y-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span>{mockUserStats.country}, {mockUserStats.region}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Vote className="w-4 h-4 text-gray-400" />
                    <span>{mockUserStats.party}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Briefcase className="w-4 h-4 text-gray-400" />
                    <span>{mockUserStats.company}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-green-400">{mockUserStats.victories}</div>
                    <div className="text-xs text-gray-400">Victories</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-red-400">{mockUserStats.battles - mockUserStats.victories}</div>
                    <div className="text-xs text-gray-400">Defeats</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid grid-cols-4 w-full mb-6">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="military">Military</TabsTrigger>
                <TabsTrigger value="economy">Economy</TabsTrigger>
                <TabsTrigger value="politics">Politics</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                {/* Quick Stats */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 border-blue-400/30">
                    <CardContent className="p-6 text-center">
                      <Crown className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">Rank #47</div>
                      <div className="text-blue-200">Global Ranking</div>
                    </CardContent>
                  </Card>
                  <Card className="bg-gradient-to-br from-green-500/20 to-green-600/20 border-green-400/30">
                    <CardContent className="p-6 text-center">
                      <Building className="w-8 h-8 text-green-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">3</div>
                      <div className="text-green-200">Companies Owned</div>
                    </CardContent>
                  </Card>
                  <Card className="bg-gradient-to-br from-red-500/20 to-red-600/20 border-red-400/30">
                    <CardContent className="p-6 text-center">
                      <Sword className="w-8 h-8 text-red-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">78%</div>
                      <div className="text-red-200">Win Rate</div>
                    </CardContent>
                  </Card>
                </div>

                {/* Recent News */}
                <Card className="bg-white/10 border-white/20">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <Newspaper className="w-5 h-5 mr-2" />
                      Latest News
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {mockNews.map((news, index) => (
                        <div key={index} className="flex items-start space-x-3 p-3 bg-white/5 rounded-lg">
                          <div className={`w-2 h-2 rounded-full mt-2 ${
                            news.type === 'military' ? 'bg-red-400' : 'bg-blue-400'
                          }`}></div>
                          <div className="flex-1">
                            <div className="text-white font-medium">{news.title}</div>
                            <div className="text-gray-400 text-sm">{news.time}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="military" className="space-y-6">
                <Card className="bg-white/10 border-white/20">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <Sword className="w-5 h-5 mr-2" />
                      Active Battles
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {mockBattles.map((battle, index) => (
                        <div key={index} className="bg-white/5 rounded-lg p-4">
                          <div className="flex justify-between items-start mb-2">
                            <h4 className="text-white font-semibold">{battle.region}</h4>
                            <Badge className={`${
                              battle.status === 'ongoing' ? 'bg-yellow-500' :
                              battle.status === 'victory' ? 'bg-green-500' : 'bg-red-500'
                            } text-black`}>
                              {battle.status === 'ongoing' ? battle.timeLeft : battle.result}
                            </Badge>
                          </div>
                          <div className="text-gray-300 text-sm">
                            {battle.attacker} vs {battle.defender}
                          </div>
                          {battle.status === 'ongoing' && (
                            <Button className="mt-3 bg-red-600 hover:bg-red-700">
                              Join Battle
                            </Button>
                          )}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="economy" className="space-y-6">
                <Card className="bg-white/10 border-white/20">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <Building className="w-5 h-5 mr-2" />
                      My Companies
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {mockCompanies.map((company, index) => (
                        <div key={index} className="bg-white/5 rounded-lg p-4">
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <h4 className="text-white font-semibold">{company.name}</h4>
                              <p className="text-gray-400 text-sm">{company.type}</p>
                            </div>
                            <div className="text-right">
                              <div className="text-green-400 font-semibold">{company.profit}</div>
                              <div className="text-gray-400 text-sm">Daily Profit</div>
                            </div>
                          </div>
                          <div className="flex justify-between items-center">
                            <div className="flex items-center space-x-2">
                              <Users className="w-4 h-4 text-gray-400" />
                              <span className="text-gray-300 text-sm">{company.employees} employees</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              {[...Array(5)].map((_, i) => (
                                <Star
                                  key={i}
                                  className={`w-4 h-4 ${
                                    i < company.quality ? 'text-yellow-400 fill-current' : 'text-gray-600'
                                  }`}
                                />
                              ))}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <Button className="w-full mt-4 bg-green-600 hover:bg-green-700">
                      Create New Company
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="politics" className="space-y-6">
                <Card className="bg-white/10 border-white/20">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <Vote className="w-5 h-5 mr-2" />
                      Political Status
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="bg-white/5 rounded-lg p-4">
                        <h4 className="text-white font-semibold mb-2">Current Party</h4>
                        <p className="text-gray-300">{mockUserStats.party}</p>
                        <p className="text-gray-400 text-sm">Member since January 2024</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-4">
                        <h4 className="text-white font-semibold mb-2">Next Elections</h4>
                        <p className="text-gray-300">Presidential Election - Germany</p>
                        <p className="text-gray-400 text-sm">In 3 days, 14 hours</p>
                        <Button className="mt-2 bg-blue-600 hover:bg-blue-700">
                          View Candidates
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;