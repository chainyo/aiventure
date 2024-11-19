<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from "$app/navigation";
    import { ChevronDown, LoaderCircle } from "lucide-svelte";
    
    import { playerStore, type PlayerData } from "$lib/stores/playerStore";
    import { userStore } from "$lib/stores/userStore";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import { Skeleton } from "$lib/components/ui/skeleton/index.js";


    let { children } = $props();
    let isLoading = $state(true);
    let sidebarOpen = $state(false);
    let needsVerification = $state(false);

    onMount(async () => {
    try {
        const initialized = await userStore.initializeFromLocalStorage();

        if (!initialized) {
            await goto('/login');
            return;
        }

        // Fetch user data first
        await userStore.fetchUser();
        
        // Initialize player data if needed
        // if (!$playerStore) {
        //     await playerStore.initialize();
        // }

        sidebarOpen = true;
    } catch (error) {
        console.error('Failed to initialize:', error);
        await goto('/login');
    } finally {
        isLoading = false;
        }
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
                            {#if $playerStore?.labs}
                                {#each $playerStore.labs as lab}
                                    <DropdownMenu.Item>
                                        <span>Lab {lab.name}</span>
                                    </DropdownMenu.Item>
                                {/each}
                            {:else}
                                <DropdownMenu.Item disabled>
                                    <span>No labs found</span>
                                </DropdownMenu.Item>
                            {/if}
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
                {#if $playerStore}
                    <Sidebar.MenuItem>
                        <Avatar.Root class="relative w-12 h-12">
                            <Avatar.Image src="https://avatar.iran.liara.run/public" alt="avatar" />
                            <Avatar.Fallback>{$playerStore.name.slice(0, 2)}</Avatar.Fallback>
                        </Avatar.Root>
                    </Sidebar.MenuItem>
                    <div class="flex flex-col gap-2">
                        <Sidebar.MenuItem>
                            <Badge class="max-w-full" variant="outline">{$playerStore.name}</Badge>
                        </Sidebar.MenuItem>
                        <Sidebar.MenuItem>
                            <Badge class="max-w-full">$ {$playerStore.funds}</Badge>
                        </Sidebar.MenuItem>
                    </div>
                {:else}
                    <Sidebar.MenuItem>
                        <Skeleton class="size-8 rounded-full" />
                    </Sidebar.MenuItem>
                    <div class="flex flex-col">
                        <Sidebar.MenuItem>
                            <Skeleton class="h-4 w-[125px]" />
                        </Sidebar.MenuItem>
                        <Sidebar.MenuItem>
                            <Skeleton class="h-4 w-[125px]" />
                        </Sidebar.MenuItem>
                    </div>
                {/if}
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
