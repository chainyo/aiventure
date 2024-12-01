<script lang="ts">
    import { getContext } from "svelte";

    import { type GameContext, GAME_CONTEXT_KEY } from "$lib/types/context";

    let gameContext = getContext<GameContext>(GAME_CONTEXT_KEY);
</script>
