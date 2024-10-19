<script>
	import { ModeWatcher } from "mode-watcher";
	import { Toaster } from "$lib/components/ui/sonner";
	import '../app.css';
</script>

<ModeWatcher />
<Toaster richColors expand={true} />

<div class="relative flex min-h-screen flex-col bg-background" id="page">
	<!-- <SiteHeader /> -->
	<div class="flex-1">
		<slot />
	</div>
	<!-- <SiteFooter /> -->
</div>
