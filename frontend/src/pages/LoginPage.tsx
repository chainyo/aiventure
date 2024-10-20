import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginFormSchema, LoginFormSchema } from '@/lib/schema';


function LoginPage() {
  const navigate = useNavigate();
  const [isInitialized, setIsInitialized] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormSchema>({
    resolver: zodResolver(loginFormSchema),
  });

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (user) {
      redirectToPlay();
    }
    setIsInitialized(true);
  }, []);

  function redirectToPlay() {
    setTimeout(() => {
      navigate('/play');
    }, 3000);
  }

  const onSubmit = async (data: LoginFormSchema) => {
    const loginPromise = fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    }).then(async (response) => {
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      return await response.json();
    });

    toast.promise(loginPromise, {
      loading: 'Logging in...',
      success: (data) => {
        localStorage.setItem('user', JSON.stringify(data));
        redirectToPlay();
        return "Logged in successfully.";
      },
      error: (error: any) => `Login failed: ${error.message}`,
    });
  };

  if (!isInitialized) {
    return <p>Loading...</p>;
  }

  const user = JSON.parse(localStorage.getItem('user') || 'null');

  return (
    <main className="container mx-auto p-4 max-w-md">
      <h1 className="text-3xl font-bold mb-6">Login to AI Venture</h1>
      {!user ? (
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-4">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" {...register('email')} />
            {errors.email && <p className="text-red-500">{errors.email.message}</p>}
          </div>
          <div className="mb-4">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" {...register('password')} />
            {errors.password && <p className="text-red-500">{errors.password.message}</p>}
          </div>
          <Button type="submit">Log in</Button>
        </form>
      ) : (
        <>
          <p className="text-2xl">Welcome back <span className="font-bold text-blue-500">{user.name}</span></p>
          <p className="text-gray-500">Redirecting you to the game...</p>
        </>
      )}
    </main>
  );
}

export default LoginPage;

