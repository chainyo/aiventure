<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from "$app/navigation";
    import { userStore } from "$lib/stores/userStore";

    let isLoading = true;

    onMount(async () => {
        const initialized = userStore.initializeFromLocalStorage();
        if (!initialized) {
            // User is not logged in, redirect to login page
            goto('/login');
        } else {
            // Optionally, you can fetch additional user data here if needed
            await userStore.fetchUser();
        }
        isLoading = false;
    });
</script>

{#if isLoading}
    <p>Loading...</p>
{:else if $userStore}
    <slot />
{/if}