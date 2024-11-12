<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from "$app/navigation";
    import { ChevronDown, LoaderCircle } from "lucide-svelte";

    import { userStore } from "$lib/stores/userStore";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";


    let { children } = $props();
    let isLoading = $state(true);
    let sidebarOpen = $state(false);
    let needsVerification = $state(false);

    onMount(async () => {
        const initialized = userStore.initializeFromLocalStorage();

        if (!initialized) {
            // User is not logged in, redirect to login page
            goto('/login');
        // } else if ($userStore && !$userStore.is_verified) {
        //     // NOTE: We don't need to verify email for now
        //     // needsVerification = true;
        } else {
            // Optionally, you can fetch additional user data here if needed
            await userStore.fetchUser();
        }
        isLoading = false;
        sidebarOpen = true;
    });
</script>

<Sidebar.Provider open={sidebarOpen}>
    <Sidebar.Root>
        <Sidebar.Header>
            <Sidebar.Menu>
                <Sidebar.MenuItem>
                    <DropdownMenu.Root>
                        <DropdownMenu.Trigger>
                            {#snippet child({ props })}
                                <Sidebar.MenuButton {...props}>
                                    Select active Lab
                                    <ChevronDown class="ml-auto" />
                                </Sidebar.MenuButton>
                            {/snippet}
                        </DropdownMenu.Trigger>
                        <DropdownMenu.Content class="w-[--bits-dropdown-menu-anchor-width]">
                            {#each [1, 2, 3] as lab}
                            <DropdownMenu.Item>
                                <span>Lab {lab}</span>
                            </DropdownMenu.Item>
                            {/each}
                        </DropdownMenu.Content>
                    </DropdownMenu.Root>
                </Sidebar.MenuItem>
            </Sidebar.Menu>
        </Sidebar.Header>
        <Sidebar.Content>
            <Sidebar.Group />
            <Sidebar.Group />
        </Sidebar.Content>
        <Sidebar.Footer class="pb-8">
            <Sidebar.Menu class="flex flex-row items-center mx-auto justify-center gap-4">
                <Sidebar.MenuItem>
                    <Avatar.Root class="relative">
                        <Avatar.Image src="https://github.com/shadcn.png" alt="@shadcn" />
                        <Avatar.Fallback>CN</Avatar.Fallback>
                    </Avatar.Root>
                </Sidebar.MenuItem>
                <Sidebar.MenuItem>
                    {#if $userStore}
                    <Badge variant="outline">{$userStore.email}</Badge>
                    {:else}
                    <Badge variant="outline">ID: 12345</Badge>
                    {/if}
                </Sidebar.MenuItem>
            </Sidebar.Menu>
        </Sidebar.Footer>
    </Sidebar.Root>
    <main class="container mx-auto p-4 max-w-md">
        <Sidebar.Trigger class="absolute top-0 right-0"/>
        {#if isLoading}
        <div class="flex items-center justify-center h-screen mx-auto">
            <LoaderCircle class="mr-2 size-4 animate-spin" />
            <p>Loading the game state...</p>
        </div>
        {:else if needsVerification}
        <p>Please verify your email to continue. Check your inbox for a verification link.</p>
        {:else}
            {@render children?.()}
        {/if}
    </main>
</Sidebar.Provider>
