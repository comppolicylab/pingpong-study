<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { cn } from '$lib/utils.js';
	import type { HTMLAttributes } from 'svelte/elements';
	import { loginAsWithMagicLink } from '$lib/api/client';
	import { fail } from '@sveltejs/kit';
	import SpinnerIcon from '$lib/components/spinner.svelte';
	let { class: className, ...restProps }: HTMLAttributes<HTMLDivElement> = $props();
	import { page } from '$app/state';
	import { toast } from 'svelte-sonner';
	import { resolve } from '$app/paths';

	const forward = page.url.searchParams.get('forward') || '/';

	const id = $props.id();
	let linkSent = $state(false);
	let isLoading = $state(false);

	async function handleSubmit(event: Event) {
		event.preventDefault();
		isLoading = true;
		const formData = new FormData(event.target as HTMLFormElement);
		const instructorEmail = formData.get('instructor_email') as string;
		const adminEmail = formData.get('admin_email') as string;

		if (!instructorEmail || !adminEmail) {
			isLoading = false;
			return fail(400, {
				instructorEmail,
				adminEmail,
				success: false,
				error: 'Missing email(s)'
			});
		}

		try {
			const result = await loginAsWithMagicLink(fetch, instructorEmail, adminEmail, forward);
			if (result.$status < 300) {
				linkSent = true;
			} else {
				toast.error(
					result.detail?.toString() ||
						'We faced an unexpected error. Please try again or contact the study administrator.',
					{
						duration: 10000
					}
				);
			}
		} catch (error) {
			const message =
				error instanceof Error
					? error.message
					: 'We faced a network error. Please try again or contact the study administrator.';
			toast.error(message, { duration: 10000 });
		} finally {
			isLoading = false;
		}
	}
</script>

<div class={cn('flex flex-col gap-6', className)} {...restProps}>
	<Card.Root>
		{#if !linkSent}
			<Card.Header class="text-center">
				<Card.Title class="text-xl">Admin Login</Card.Title>
				<Card.Description>Send a login link to your admin email.</Card.Description>
			</Card.Header>
		{/if}
		<Card.Content>
			{#if !linkSent}
				<form onsubmit={handleSubmit}>
					<div class="grid gap-6">
						<div class="grid gap-6">
							<div class="grid gap-3">
								<Label for="admin-email-{id}">Admin email</Label>
								<Input
									id="admin-email-{id}"
									type="email"
									name="admin_email"
									placeholder="admin@example.edu"
									required
									disabled={isLoading}
								/>
							</div>
							<div class="grid gap-3">
								<Label for="instructor-email-{id}">Instructor email</Label>
								<Input
									id="instructor-email-{id}"
									type="email"
									name="instructor_email"
									placeholder="instructor@example.edu"
									required
									disabled={isLoading}
								/>
							</div>
							<Button type="submit" class="w-full" disabled={isLoading}>
								{#if isLoading}
									<SpinnerIcon class="animate-spin" />
								{:else}
									Send login link
								{/if}
							</Button>
							<div class="text-center text-sm">
								Are you an instructor?
								<a href={resolve('/login')} class="underline underline-offset-4"> Log in here</a>
							</div>
						</div>
					</div>
				</form>
			{:else}
				<div class="flex flex-col gap-1">
					<div class="text-center text-lg font-semibold">Success!</div>
					<div class="text-center text-sm text-muted-foreground">
						A login link has been sent to the admin email.
					</div>
					<Button onclick={() => (linkSent = false)} class="mt-4">Send another link</Button>
				</div>
			{/if}
		</Card.Content>
	</Card.Root>
</div>
