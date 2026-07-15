<script lang="ts">
	import StudyLanding from '$lib/components/study-landing.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
</script>

{#snippet headerAction()}
	<Button href="/login" class="bg-white text-base text-slate-900 shadow-sm hover:bg-slate-100">
		Log in
	</Button>
{/snippet}

{#snippet primaryAction()}
	<Button
		href="/login"
		class="bg-pingpong-blue p-4 text-base text-white select-none hover:bg-pingpong-blue/90 dark:bg-white dark:text-slate-900 dark:hover:bg-slate-200"
	>
		Instructor login
	</Button>
{/snippet}

<StudyLanding {headerAction} {primaryAction} />
