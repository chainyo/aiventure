import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { Button } from "@/components/ui/button";

function VerifyPage() {
  const [verificationStatus, setVerificationStatus] = useState('pending');
  const navigate = useNavigate();

  useEffect(() => {
    const token = window.location.hash.slice(1);
    if (token) {
      verifyEmail(token);
    } else {
      setVerificationStatus('error');
      toast.error('Email verification failed. Please try again or contact support.');
    }
  }, []);

  async function verifyEmail(token: string) {
    try {
      const response = await fetch('/api/auth/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
      });

      if (response.ok) {
        setVerificationStatus('success');
        toast.success('Email verified successfully');
      } else {
        setVerificationStatus('error');
        toast.error('Email verification failed');
      }
    } catch (error) {
      setVerificationStatus('error');
      toast.error('An error occurred during verification');
    }
  }

  function goToLogin() {
    navigate('/login');
  }

  return (
    <div className="container mx-auto p-4 max-w-md">
      <h1 className="text-2xl font-bold mb-4">Email Verification</h1>

      {verificationStatus === 'pending' && <p>Verifying your email...</p>}
      {verificationStatus === 'success' && (
        <>
          <p className="text-green-600 mb-4">Your email has been successfully verified!</p>
          <Button onClick={goToLogin}>Go to Login</Button>
        </>
      )}
      {verificationStatus === 'error' && (
        <>
          <p className="text-red-600 mb-4">Email verification failed. Please try again or contact support.</p>
          <Button onClick={goToLogin}>Go to Login</Button>
        </>
      )}
    </div>
  );
}

export default VerifyPage;
