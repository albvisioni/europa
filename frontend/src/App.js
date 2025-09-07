import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import Dashboard from "./components/Dashboard";
import { mockAuth } from "./mock/mockData";
import { useToast } from "./hooks/use-toast";
import { Toaster } from "./components/ui/toaster";

function App() {
  const [user, setUser] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const { toast } = useToast();

  const handleLogin = (credentials) => {
    const result = mockAuth.login(credentials);
    if (result.success) {
      setUser(result.user);
      setIsLoggedIn(true);
      toast({
        title: "Welcome back!",
        description: `Logged in as ${result.user.username}`,
      });
    } else {
      toast({
        title: "Login Failed",
        description: result.error,
        variant: "destructive",
      });
    }
  };

  const handleRegister = (userData) => {
    const result = mockAuth.register(userData);
    if (result.success) {
      setUser(result.user);
      setIsLoggedIn(true);
      toast({
        title: "Welcome to Europa!",
        description: `Account created for ${result.user.username}`,
      });
    } else {
      toast({
        title: "Registration Failed", 
        description: result.error,
        variant: "destructive",
      });
    }
  };

  const handleLogout = () => {
    setUser(null);
    setIsLoggedIn(false);
    toast({
      title: "Logged out",
      description: "See you next time!",
    });
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route 
            path="/" 
            element={
              isLoggedIn ? (
                <Dashboard user={user} onLogout={handleLogout} />
              ) : (
                <HomePage onLogin={handleLogin} onRegister={handleRegister} />
              )
            } 
          />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </div>
  );
}

export default App;