<script>
	import { ModeWatcher } from "mode-watcher";
	import { Toaster } from "$lib/components/ui/sonner";
	import '../app.css';
</script>

<ModeWatcher />
<Toaster richColors expand={true} />
<slot></slot>
