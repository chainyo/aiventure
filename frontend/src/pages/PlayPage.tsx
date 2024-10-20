import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { initializeSocket, closeSocket, getPlayerData } from "@/lib/websocket";
import { useUser } from "@/lib/hooks/useUser";

function PlayPage() {
  const [playerData] = useState(null);
  const navigate = useNavigate();
  const { user, clearUser, fetchUser } = useUser();

  useEffect(() => {
    const initUser = async () => {
      if (!user) {
        const fetchedUser = await fetchUser();
        if (!fetchedUser) {
          navigate('/login');
          return;
        }
      }

      if (!user?.is_verified) {
        navigate('/verify');
        return;
      }

      initializeSocket();
      getPlayerData();
    };

    initUser();

    return () => {
      closeSocket();
    };
  }, [navigate, fetchUser, user]);

  function handleLogout() {
    clearUser();
    navigate('/');
  }

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <main className="container mx-auto p-4 max-w-md">
      <h1 className="text-3xl font-bold mb-6">Welcome to AI Venture</h1>
      <p>Logged in as {user.name}</p>
      <p>Your PID is {user.pid}</p>
      <p>Your token is {user.token}</p>
      <p>Your is_verified is {user.is_verified.toString()}</p>
      <Button onClick={handleLogout}>Log out</Button>

      {playerData && (
        <div>
          <h2>Player Data:</h2>
          <p>{JSON.stringify(playerData)}</p>
        </div>
      )}
    </main>
  );
}

export default PlayPage;
