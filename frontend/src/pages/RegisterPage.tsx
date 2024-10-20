import { useState } from 'react';
import { toast } from 'sonner';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { signupFormSchema, SignupFormSchema } from '@/lib/schema';


function RegisterPage() {
  const [registrationSuccess, setRegistrationSuccess] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<SignupFormSchema>({
    resolver: zodResolver(signupFormSchema),
  });

  const onSubmit = async (data: SignupFormSchema) => {
    const registerPromise = fetch('/api/auth/register', {
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

    toast.promise(registerPromise, {
      loading: 'Registering...',
      success: () => {
        setRegistrationSuccess(true);
        return "Registration successful. Please check your email for verification.";
      },
      error: (error: any) => `Registration failed: ${error.message}`,
    });
  };

  return (
    <main className="container mx-auto p-4 max-w-md">
      <h1 className="text-3xl font-bold mb-6">Register to AI Venture</h1>
      {!registrationSuccess ? (
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-4">
            <Label htmlFor="name">Username</Label>
            <Input id="name" {...register('name')} />
            {errors.name && <p className="text-red-500">{errors.name.message}</p>}
          </div>
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
          <Button type="submit">Register</Button>
        </form>
      ) : (
        <p>Registration successful. You can now <a href="/login">login</a>.</p>
      )}
    </main>
  );
}

export default RegisterPage;

