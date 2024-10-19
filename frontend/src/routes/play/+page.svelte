<script lang="ts">
	import { goto } from "$app/navigation";
	import { userStore } from "$lib/stores/userStore";
	import { Button } from "$lib/components/ui/button";

  function handleLogout() {
    userStore.clearUser();
    goto('/');
  }
</script>

<svelte:head>
  <title>AI Venture | Play</title>
  <meta name="description" content="Play AI Venture" />
</svelte:head>

<main class="container mx-auto p-4 max-w-md">
    <h1 class="text-3xl font-bold mb-6">Welcome to AI Venture</h1>
    {#if $userStore}
        <p>Logged in as {$userStore.name}</p>
        <p>Your PID is {$userStore.pid}</p>
        <p>Your token is {$userStore.token}</p>
        <p>Your is_verified is {$userStore.is_verified}</p>
        <Button on:click={handleLogout}>Log out</Button>
    {:else}
        <p>You are not logged in</p>
    {/if}
</main>
