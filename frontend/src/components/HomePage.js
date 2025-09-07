import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Users, Trophy, Star, MapPin, Building, Sword, Crown } from 'lucide-react';
import { countriesByRegion } from '../mock/worldCountries';

const HomePage = ({ onLogin, onRegister }) => {
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ 
    username: '', 
    email: '', 
    password: '', 
    country: 'albania' 
  });
  const [isRegistering, setIsRegistering] = useState(false);

  const topCountries = [
    { name: 'Gjermania', players: 6543, flag: '🇩🇪', code: 'DE' },
    { name: 'Franca', players: 5987, flag: '🇫🇷', code: 'FR' },
    { name: 'Anglia', players: 5678, flag: '🇬🇧', code: 'GB' },
    { name: 'Italia', players: 5432, flag: '🇮🇹', code: 'IT' },
    { name: 'Spanja', players: 4876, flag: '🇪🇸', code: 'ES' },
    { name: 'Turqia', players: 5432, flag: '🇹🇷', code: 'TR' },
    { name: 'Polonia', players: 4321, flag: '🇵🇱', code: 'PL' },
    { name: 'Ukraina', players: 4987, flag: '🇺🇦', code: 'UA' },
    { name: 'Rumania', players: 3456, flag: '🇷🇴', code: 'RO' },
    { name: 'Greqia', players: 3245, flag: '🇬🇷', code: 'GR' },
    { name: 'Serbia', players: 2987, flag: '🇷🇸', code: 'RS' },
    { name: 'Bulgaria', players: 2876, flag: '🇧🇬', code: 'BG' },
    { name: 'Kroacia', players: 2543, flag: '🇭🇷', code: 'HR' },
    { name: 'Hungaria', players: 2987, flag: '🇭🇺', code: 'HU' },
    { name: 'Shqipëria', players: 2156, flag: '🇦🇱', code: 'AL' },
    { name: 'Bosnja dhe Hercegovina', players: 2134, flag: '🇧🇦', code: 'BA' },
    { name: 'Kosova', players: 1842, flag: '🇽🇰', code: 'XK' },
    { name: 'Sllovenia', players: 1876, flag: '🇸🇮', code: 'SI' },
    { name: 'Maqedonia e Veriut', players: 1654, flag: '🇲🇰', code: 'MK' }
  ];

  const features = [
    {
      icon: <Crown className="w-8 h-8 text-yellow-400" />,
      title: 'Political Power',
      description: 'Join political parties, run for office, and shape your nation\'s future through democratic processes.'
    },
    {
      icon: <Building className="w-8 h-8 text-green-400" />,
      title: 'Economic Empire',
      description: 'Build companies, manage resources, and dominate European markets through strategic business decisions.'
    },
    {
      icon: <Sword className="w-8 h-8 text-red-400" />,
      title: 'Military Strategy',
      description: 'Lead armies, conquer territories, and defend your homeland in epic continental battles.'
    }
  ];

  const testimonials = [
    { text: "Europa sjell politikën ballkanike në jetë në një mënyrë tërheqëse", author: "Koha Ditore" },
    { text: "Një kryevepër e lojës strategjike për rajonin", author: "Gazeta Express" },
    { text: "Europa ofron simulimin më realist politik të Ballkanit", author: "BIRN" },
    { text: "Një platformë e shkëlqyer për të kuptuar dinamikat rajonale", author: "Exit News" }
  ];

  const handleLogin = (e) => {
    e.preventDefault();
    onLogin(loginForm);
  };

  const handleRegister = (e) => {
    e.preventDefault();
    onRegister(registerForm);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-indigo-900 to-purple-900">
      {/* Hero Section */}
      <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background Image */}
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1551836022-deb4988cc6c0?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80')] bg-cover bg-center">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-900/80 via-indigo-900/70 to-purple-900/80"></div>
        </div>

        {/* Header */}
        <header className="absolute top-0 left-0 right-0 z-20 p-6">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center">
                <Crown className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white">EUROPA</h1>
            </div>
            
            {/* Login Form */}
            <div className="flex items-center space-x-4">
              <Input
                type="email"
                placeholder="Email"
                value={loginForm.email}
                onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                className="w-40 bg-white/10 border-white/20 text-white placeholder-white/70"
              />
              <Input
                type="password"
                placeholder="Password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                className="w-40 bg-white/10 border-white/20 text-white placeholder-white/70"
              />
              <Button 
                onClick={handleLogin}
                className="bg-yellow-500 hover:bg-yellow-600 text-black font-semibold"
              >
                Sign In
              </Button>
              <Button 
                variant="outline" 
                className="border-white/30 text-white hover:bg-white/10"
              >
                <Users className="w-4 h-4 mr-2" />
                Sign in with Facebook
              </Button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-6">
          <h2 className="text-6xl font-bold mb-6 bg-gradient-to-r from-yellow-300 to-yellow-500 bg-clip-text text-transparent">
            EUROPA
          </h2>
          <p className="text-2xl mb-8 text-gray-200">
            A new Europe is emerging. Your country needs YOU!
          </p>
          
          <div className="flex justify-center space-x-4 mb-12">
            <Button 
              size="lg"
              onClick={() => setIsRegistering(true)}
              className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold px-8 py-4 text-lg rounded-lg shadow-lg transform hover:scale-105 transition-all"
            >
              Sign up
            </Button>
            <Button 
              size="lg"
              variant="outline"
              className="border-2 border-blue-400 text-blue-400 hover:bg-blue-400 hover:text-white font-bold px-8 py-4 text-lg rounded-lg shadow-lg"
            >
              <Users className="w-5 h-5 mr-2" />
              Sign up with Facebook
            </Button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-black/50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-2xl font-bold text-white mb-8">Features</h3>
              <div className="space-y-6">
                {features.map((feature, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      {feature.icon}
                    </div>
                    <div>
                      <h4 className="font-semibold text-white mb-2">{feature.title}</h4>
                      <p className="text-gray-300 text-sm">{feature.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-bold text-white mb-8">Top Countries</h3>
              <div className="space-y-4">
                {topCountries.map((country, index) => (
                  <div key={index} className="flex items-center justify-between bg-white/10 rounded-lg p-3">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{country.flag}</span>
                      <span className="text-white font-medium">{country.name}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-yellow-400 font-bold">{country.players.toLocaleString()}</span>
                      <Users className="w-4 h-4 text-gray-400" />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-bold text-white mb-8">What others are saying</h3>
              <div className="space-y-6">
                {testimonials.map((testimonial, index) => (
                  <div key={index} className="bg-white/10 rounded-lg p-4">
                    <p className="text-gray-200 italic mb-3">"{testimonial.text}"</p>
                    <p className="text-yellow-400 font-semibold">{testimonial.author}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Registration Modal */}
      {isRegistering && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
          <Card className="w-full max-w-md mx-4">
            <CardHeader>
              <CardTitle className="text-center">Join Europa</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleRegister} className="space-y-4">
                <Input
                  placeholder="Username"
                  value={registerForm.username}
                  onChange={(e) => setRegisterForm({ ...registerForm, username: e.target.value })}
                  required
                />
                <Input
                  type="email"
                  placeholder="Email"
                  value={registerForm.email}
                  onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
                  required
                />
                <Input
                  type="password"
                  placeholder="Password"
                  value={registerForm.password}
                  onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
                  required
                />
                <select 
                  className="w-full p-2 border rounded-md"
                  value={registerForm.country}
                  onChange={(e) => setRegisterForm({ ...registerForm, country: e.target.value })}
                >
                  {/* Ballkani dhe Europa Juglindore */}
                  <optgroup label="Ballkani dhe Europa Juglindore">
                    <option value="albania">🇦🇱 Shqipëria</option>
                    <option value="kosovo">🇽🇰 Kosova</option>
                    <option value="north_macedonia">🇲🇰 Maqedonia e Veriut</option>
                    <option value="serbia">🇷🇸 Serbia</option>
                    <option value="greece">🇬🇷 Greqia</option>
                    <option value="montenegro">🇲🇪 Mali i Zi</option>
                    <option value="bosnia">🇧🇦 Bosnja dhe Hercegovina</option>
                    <option value="slovenia">🇸🇮 Sllovenia</option>
                    <option value="croatia">🇭🇷 Kroacia</option>
                    <option value="romania">🇷🇴 Rumania</option>
                    <option value="bulgaria">🇧🇬 Bulgaria</option>
                  </optgroup>
                  
                  {/* Europa Lindore */}
                  <optgroup label="Europa Lindore">
                    <option value="turkey">🇹🇷 Turqia</option>
                    <option value="moldova">🇲🇩 Moldavia</option>
                    <option value="ukraine">🇺🇦 Ukraina</option>
                    <option value="belarus">🇧🇾 Bjellorusia</option>
                    <option value="latvia">🇱🇻 Letonia</option>
                    <option value="estonia">🇪🇪 Estonia</option>
                    <option value="lithuania">🇱🇹 Lituania</option>
                    <option value="russia">🇷🇺 Rusia</option>
                  </optgroup>
                  
                  {/* Europa Qendrore */}
                  <optgroup label="Europa Qendrore">
                    <option value="hungary">🇭🇺 Hungaria</option>
                    <option value="poland">🇵🇱 Polonia</option>
                    <option value="slovakia">🇸🇰 Sllovakia</option>
                    <option value="czech">🇨🇿 Republika Çeke</option>
                  </optgroup>
                  
                  {/* Europa Perëndimore */}
                  <optgroup label="Europa Perëndimore">
                    <option value="germany">🇩🇪 Gjermania</option>
                    <option value="france">🇫🇷 Franca</option>
                    <option value="switzerland">🇨🇭 Zvicra</option>
                    <option value="austria">🇦🇹 Austria</option>
                    <option value="italy">🇮🇹 Italia</option>
                    <option value="uk">🇬🇧 Anglia</option>
                    <option value="ireland">🇮🇪 Irlanda</option>
                    <option value="netherlands">🇳🇱 Holanda</option>
                    <option value="belgium">🇧🇪 Belgjika</option>
                    <option value="spain">🇪🇸 Spanja</option>
                    <option value="portugal">🇵🇹 Portugalia</option>
                  </optgroup>
                  
                  {/* Ishujt */}
                  <optgroup label="Ishujt">
                    <option value="cyprus">🇨🇾 Qipro</option>
                    <option value="malta">🇲🇹 Malta</option>
                  </optgroup>
                  
                  {/* Azia */}
                  <optgroup label="Azia">
                    <option value="china">🇨🇳 Kina</option>
                    <option value="japan">🇯🇵 Japonia</option>
                    <option value="saudi_arabia">🇸🇦 Arabia Saudite</option>
                    <option value="israel">🇮🇱 Izraeli</option>
                    <option value="palestine">🇵🇸 Palestina</option>
                    <option value="syria">🇸🇾 Siria</option>
                    <option value="iran">🇮🇷 Irani</option>
                    <option value="iraq">🇮🇶 Iraku</option>
                  </optgroup>
                  
                  {/* Afrika */}
                  <optgroup label="Afrika">
                    <option value="egypt">🇪🇬 Egjipti</option>
                  </optgroup>
                  
                  {/* Amerika */}
                  <optgroup label="Amerika">
                    <option value="usa">🇺🇸 SHBA</option>
                    <option value="canada">🇨🇦 Kanadaja</option>
                    <option value="mexico">🇲🇽 Meksika</option>
                  </optgroup>
                </select>
                <div className="flex space-x-2">
                  <Button type="submit" className="flex-1">Register</Button>
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={() => setIsRegistering(false)}
                    className="flex-1"
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default HomePage;