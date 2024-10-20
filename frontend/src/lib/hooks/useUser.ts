import { useState, useEffect } from 'react';

export interface UserData {
  name: string;
  pid: string;
  token: string;
  is_verified: boolean;
}

export function useUser() {
  const [user, setUser] = useState<UserData | null>(null);

  const setUserData = (userData: UserData) => {
    setUser(userData);
    localStorage.setItem('aiventureUser', JSON.stringify(userData));
  };

  const clearUser = () => {
    setUser(null);
    localStorage.removeItem('aiventureUser');
  };

  const initializeFromLocalStorage = () => {
    const storedUser = localStorage.getItem('aiventureUser');
    if (storedUser) {
      setUser(JSON.parse(storedUser) as UserData);
      return true;
    }
    return false;
  };

  const fetchUser = async () => {
    const storedUser: UserData | null = JSON.parse(localStorage.getItem('aiventureUser') || 'null');
    if (!storedUser) return false;

    try {
      const response = await fetch('/api/user/current', {
        headers: {
          'Authorization': `Bearer ${storedUser.token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data as UserData);
        return true;
      } else {
        throw new Error('Failed to fetch user data');
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
      return false;
    }
  };

  useEffect(() => {
    initializeFromLocalStorage();
  }, []);

  return {
    user,
    setUser: setUserData,
    clearUser,
    initializeFromLocalStorage,
    fetchUser,
  };
}
