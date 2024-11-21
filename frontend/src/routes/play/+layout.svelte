<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { goto } from "$app/navigation";
    import { ChevronDown, LoaderCircle } from "lucide-svelte";

    import { GameWebSocketClient } from "$lib/websocket";
    import { GameActions, type GameMessageResponse } from "$lib/types/websocket";
    import { playerStore, type Player } from "$lib/stores/playerStore";
    import { userStore } from "$lib/stores/userStore";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import { Skeleton } from "$lib/components/ui/skeleton/index.js";


    let client: GameWebSocketClient;
    let { children } = $props();
    let isLoading = $state(true);
    let sidebarOpen = $state(false);
    let needsVerification = $state(false);
    let messages: string[] = [];
    let playerName: string = $state("");
    let labName: string = $state("");


    function handleCreatePlayer(event: SubmitEvent) {
        event.preventDefault();
        if (!playerName.trim()) return;

        client.sendCommand(GameActions.CREATE_PLAYER, { name: playerName.trim() });
    }

    function handleCreateLab(event: SubmitEvent) {
        event.preventDefault();
        if (!labName.trim()) return;

        client.sendCommand(GameActions.CREATE_LAB, { name: labName.trim() });
    }

    async function initializeWebSocket() {
        if (!$userStore?.access_token) {
            return;
        }

        try {
            client = new GameWebSocketClient();
            client.token = $userStore.access_token;

            await client.connectWebSocket();

            client.onMessage((data: GameMessageResponse) => {
                messages = [...messages, JSON.stringify(data)];

                switch (data.action) {
                    case GameActions.CREATE_PLAYER:
                    case GameActions.RETRIEVE_PLAYER_DATA:
                        const player = data.payload as Player;
                        if (player && Object.keys(player).length > 0) {
                            playerStore.set(player);
                        }
                        break;
                }
            });

            client.sendCommand(GameActions.RETRIEVE_PLAYER_DATA);

        } catch (error) {
            throw new Error("WebSocket connection failed");
        }
    }

    onDestroy(() => {
        if (client) {
            client.close();
        }
    });

    onMount(async () => {
        try {
            const initialized = await userStore.initializeFromLocalStorage();

            if (!initialized) {
                throw new Error("User not initialized");
            }

            // Fetch user data first
            await userStore.fetchUser();
            
            if ($userStore?.access_token) {
                await initializeWebSocket();
            } else {
                throw new Error("User not authenticated");
            }

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
            {#if $userStore !== null}
                {#if $playerStore === null}
                    <form class="flex w-full max-w-sm flex-col gap-1.5" onsubmit={handleCreatePlayer}>
                        <Label for="player-name">Player name</Label>
                        <Input type="text" id="player-name" placeholder="Jane Doe" bind:value={playerName} />
                        <p class="text-muted-foreground text-sm">Enter your player name.</p>
                        <Button type="submit">Submit</Button>
                    </form>
                {/if}
                {#if $playerStore && ($playerStore.labs?.length === 0 || !$playerStore.labs)}
                    <form class="flex w-full max-w-sm flex-col gap-1.5" onsubmit={handleCreateLab}>
                        <Label for="lab-name">Lab name</Label>
                        <Input type="text" id="lab-name" placeholder="ClosedAI" bind:value={labName} />
                        <p class="text-muted-foreground text-sm">Enter your lab name.</p>
                        <Button type="submit">Submit</Button>
                    </form>
                {:else}
                    {@render children?.()}
                {/if}
            {/if}
        {/if}
    </main>
</Sidebar.Provider>
