<script lang="ts">
    import { playerStore } from "$lib/stores/playerStore";
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
