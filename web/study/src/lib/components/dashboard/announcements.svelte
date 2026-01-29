<script lang="ts">
	import * as Alert from '$lib/components/ui/alert/index.js';
	import { courses as coursesStore } from '$lib/stores/courses';
	import Info from '@lucide/svelte/icons/info';
	const hasAnyAcceptedCourses = $derived(
		$coursesStore.some((course) => course.status === 'accepted')
	);
</script>

<div class="rounded-md border p-4">
	<h2 class="mb-3 text-lg font-semibold">Announcements</h2>

	{#if hasAnyAcceptedCourses}
		<div class="flex flex-col gap-3">
			<Alert.Root class="self-start">
				<Info />
				<Alert.Title class="line-clamp-none tracking-normal"
					>Need to change your enrollment count?</Alert.Title
				>
				<Alert.Description>
					<p>
						We use your enrollment count to calculate completion rates. Click <i>View course</i> to
						navigate to the course details page and use the <i>Adjust Enrollment</i> button to update
						your enrollment count.
					</p>
				</Alert.Description>
			</Alert.Root>
		</div>
	{/if}
</div>
