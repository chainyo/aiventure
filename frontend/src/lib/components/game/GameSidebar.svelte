<script lang="ts">
    import { goto } from "$app/navigation";
    import { BadgeCent, FlaskConical, Moon, Store, Sun, Trophy } from "lucide-svelte";
    import { toggleMode } from "mode-watcher";

    import NumberTransition from "./NumberTransition.svelte";
    import { playerStore } from "$lib/stores/gameStore";
    import { userStore } from "$lib/stores/userStore";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import { Skeleton } from "$lib/components/ui/skeleton/index.js";

    const gameTabs = [
        { id: "home", name: "Home", icon: FlaskConical },
        { id: "leaderboard", name: "Leaderboard", icon: Trophy },
        { id: "market", name: "Market", icon: Store },
        { id: "investments", name: "Investments", icon: BadgeCent },
    ];

    let { children, activeTab = $bindable(), activeLab = $bindable(), gameContext } = $props();

    const triggerActiveLab = $derived(
        $playerStore?.labs?.find((l) => l.name === activeLab)?.name ?? "No lab selected"
    );
</script>

<Sidebar.Provider open={gameContext.sidebarOpen}>
    <Sidebar.Root>
        <Sidebar.Header>
            <Sidebar.Menu>
                <Sidebar.MenuItem class="flex items-center">
                    <Sidebar.MenuButton>
                        <Badge variant="destructive">AI Venture</Badge>
                    </Sidebar.MenuButton>
                </Sidebar.MenuItem>
                <Sidebar.MenuItem class="w-full flex justify-center">
                    <Select.Root type="single" name="activeLab" bind:value={activeLab}>
                        <Select.Trigger class="w-full max-w-[calc(100%-1rem)]">{triggerActiveLab}</Select.Trigger>
                        <Select.Content>
                          <Select.Group>
                            <Select.GroupHeading>🧪 Your Labs</Select.GroupHeading>
                            {#each $playerStore?.labs ?? [] as lab}
                              <Select.Item value={lab.name} label={lab.name}
                                >{lab.name}</Select.Item
                              >
                            {/each}
                          </Select.Group>
                        </Select.Content>
                    </Select.Root>
                </Sidebar.MenuItem>
            </Sidebar.Menu>
        </Sidebar.Header>
        <Sidebar.Content>
            <Sidebar.Group>
                <Sidebar.GroupLabel>Game Controls</Sidebar.GroupLabel>
                <Sidebar.GroupContent>
                    <Sidebar.Menu>
                        {#each gameTabs as tab}
                            <Sidebar.MenuItem>
                                <Sidebar.MenuButton class="flex items-center gap-2 w-full {activeTab === tab.id ? 'bg-foreground text-primary-foreground' : ''}"
                                    onclick={() => activeTab = tab.id}
                                >
                                    <tab.icon />
                                    <span>{tab.name}</span>
                                </Sidebar.MenuButton>
                            </Sidebar.MenuItem>
                        {/each}
                    </Sidebar.Menu>
                </Sidebar.GroupContent>
            </Sidebar.Group>
        </Sidebar.Content>
        <Sidebar.Footer class="pb-8">
            <Sidebar.Menu class="flex flex-row items-center mx-auto justify-center gap-4">
                {#if $playerStore}
                    <Sidebar.MenuItem>
                        <Avatar.Root class="relative w-12 h-12 ">
                            <Avatar.Image src={$playerStore.avatar} alt="avatar" />
                            <Avatar.Fallback>{$playerStore.name.slice(0, 2)}</Avatar.Fallback>
                        </Avatar.Root>
                    </Sidebar.MenuItem>
                    <div class="flex flex-col gap-2">
                        <Sidebar.MenuItem>
                            <Badge class="max-w-full" variant="outline">{$playerStore.name}</Badge>
                        </Sidebar.MenuItem>
                        <Sidebar.MenuItem>
                            <NumberTransition value={$playerStore?.funds ?? 0} />
                        </Sidebar.MenuItem>
                    </div>
                {:else}
                    <Sidebar.MenuItem>
                        <Skeleton class="size-8 rounded-full" />
                    </Sidebar.MenuItem>
                    <div class="flex flex-col gap-2">
                        <Sidebar.MenuItem>
                            <Skeleton class="h-4 w-[125px]" />
                        </Sidebar.MenuItem>
                        <Sidebar.MenuItem>
                            <Skeleton class="h-4 w-[125px]" />
                        </Sidebar.MenuItem>
                    </div>
                {/if}
            </Sidebar.Menu>
            <Sidebar.Menu class="flex flex-row justify-center gap-2 mt-8">
                <Button onclick={toggleMode} variant="outline" size="icon">
                    <Sun
                    class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
                    />
                    <Moon
                    class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
                    />
                    <span class="sr-only">Toggle theme</span>
                </Button>
                <Button onclick={() => { window.open('https://github.com/chainyo/aiventure', '_blank'); }} variant="outline" size="icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-github"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
                </Button>
                <Button onclick={() => { userStore.clearUser(); goto('/login'); }} variant="outline" size="icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-log-out"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>
                </Button>
            </Sidebar.Menu>
        </Sidebar.Footer>
    </Sidebar.Root>
    <main class="container mx-auto p-4 w-full">
        <Sidebar.Trigger class="absolute top-0 right-0"/>
        {@render children()}
    </main>
</Sidebar.Provider>
