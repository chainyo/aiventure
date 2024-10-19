<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from "$app/navigation";
    import { userStore } from "$lib/stores/userStore";

    let isLoading = true;
    let needsVerification = false;

    onMount(async () => {
        const initialized = userStore.initializeFromLocalStorage();
        if (!initialized) {
            // User is not logged in, redirect to login page
            goto('/login');
        } else if ($userStore && !$userStore.is_verified) {
            needsVerification = true;
        } else {
            // Optionally, you can fetch additional user data here if needed
        }
        isLoading = false;
    });
</script>

{#if isLoading}
    <p>Loading...</p>
{:else if needsVerification}
    <p>Please verify your email to continue. Check your inbox for a verification link.</p>
{:else if $userStore}
    <slot />
{/if}