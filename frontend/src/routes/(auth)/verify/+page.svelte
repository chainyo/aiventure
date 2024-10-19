<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { toast } from 'svelte-sonner';
    import { Button } from '$lib/components/ui/button';

    let token: string | null = null;
    let verificationStatus = 'pending';

    onMount(() => {
        token = window.location.hash.slice(1);
        if (token) {
            verifyEmail();
        } else {
            verificationStatus = 'error';
            toast.error('Email verification failed. Please try again or contact support.');
        }
    });

    async function verifyEmail() {
        try {
            const response = await fetch('/api/auth/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token }),
            });

            if (response.ok) {
                verificationStatus = 'success';
                toast.success('Email verified successfully');
            } else {
                verificationStatus = 'error';
                toast.error('Email verification failed');
            }
        } catch (error) {
            verificationStatus = 'error';
            toast.error('An error occurred during verification');
        }
    }

    function goToLogin() {
        goto('/login');
    }
</script>

<svelte:head>
    <title>Email Verification</title>
</svelte:head>

<div class="container mx-auto p-4 max-w-md">
    <h1 class="text-2xl font-bold mb-4">Email Verification</h1>

    {#if verificationStatus === 'pending'}
        <p>Verifying your email...</p>
    {:else if verificationStatus === 'success'}
        <p class="text-green-600 mb-4">Your email has been successfully verified!</p>
        <Button on:click={goToLogin}>Go to Login</Button>
    {:else}
        <p class="text-red-600 mb-4">Email verification failed. Please try again or contact support.</p>
        <Button on:click={goToLogin}>Go to Login</Button>
    {/if}
</div>