<script lang="ts">
    import { getContext } from "svelte";

    import { type GameContext, GAME_CONTEXT_KEY } from "$lib/types/context";
    import { playerStore } from "$lib/stores/playerStore";

    const { client, messages, sidebarOpen, toggleSidebar } = getContext<GameContext>(GAME_CONTEXT_KEY);
</script>

<svelte:head>
    <title>AI Venture | Play</title>
    <meta name="description" content="Play AI Venture" />
</svelte:head>

<main class="container mx-auto p-4">
    <pre class="whitespace-pre-wrap bg-secondary p-4 rounded-lg">
        {JSON.stringify($playerStore, null, 2)}
    </pre>
</main>
