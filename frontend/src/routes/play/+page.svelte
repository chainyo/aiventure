<script lang="ts">
    import { getContext } from "svelte";

    import { type GameContext, GAME_CONTEXT_KEY } from "$lib/types/context";
    import { playerStore } from "$lib/stores/playerStore";

    let gameContext = getContext<GameContext>(GAME_CONTEXT_KEY);
</script>

<svelte:head>
    <title>AI Venture | Play</title>
    <meta name="description" content="Play AI Venture" />
</svelte:head>

<main class="container mx-auto p-4">
    {#if gameContext.activeLab}
        <h1 class="text-2xl font-bold">🧪 {gameContext.activeLab}</h1>
    {:else}
        <p>No lab selected. Please select a lab from the sidebar.</p>
    {/if}
</main>
