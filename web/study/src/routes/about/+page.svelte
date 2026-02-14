<script lang="ts">
	import { page } from '$app/state';
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Accordion from '$lib/components/ui/accordion/index.js';
	import * as Carousel from '$lib/components/ui/carousel/index.js';
	import Separator from '$lib/components/ui/separator/separator.svelte';

	const hasApplicationSource = $derived(page.url.searchParams.get('source') === 'application');
	let showApplicationReferralDialog = $state(false);

	$effect(() => {
		if (hasApplicationSource) {
			showApplicationReferralDialog = true;
		}
	});

	const slides = [
		{
			title: 'Homework Problems',
			description:
				'PingPong will help students solve homework problems without giving away answers.',
			src: '/eduaccess/homework_problems.webp',
			alt: 'Screenshot of the Algebra 101 group on the PingPong platform, showing an active thread with the "AI Tutor" assistant discussing a homework problem.'
		},
		{
			title: 'Explain Concepts',
			description: 'PingPong can explain concepts specific to your course content.',
			src: '/eduaccess/explain_concepts.webp',
			alt: 'Screenshot of the Pre-Calculus group on the PingPong platform, showing an active thread with the "Calculus I" assistant discussing the Pythagorean identity.'
		},
		{
			title: 'Practice Problems',
			description:
				'Students can use PingPong to generate practice problems based on your course syllabus.',
			src: '/eduaccess/practice_problems.webp',
			alt: 'Screenshot of the Statistics 201 group on the PingPong platform displaying a conversation thread with an assistant providing a series of options for practice problem topics.'
		}
	];

	const quickFacts = [
		{
			title: 'Benefits for instructors',
			items: [
				'Access to a highly customizable, multilingual tool that instructors can easily tailor to their syllabus and assignments.',
				'Financial honorarium for engagement ($1,000 USD upon completing the study).',
				'The possibility of improved student learning outcomes.',
				'Optional short trainings to learn how to effectively use PingPong and similar AI tools.'
			]
		},
		{
			title: 'Benefits for students',
			items: [
				'Free access to PingPong, a multilingual AI chatbot designed specifically for educational settings.',
				'The possibility of improved learning outcomes due to access to the tool.'
			]
		},
		{
			title: 'Who can participate?',
			items: [
				'Instructors at two- and four-year colleges, especially those teaching math, economics, statistics, and/or computer science.'
			]
		},
		{
			title: 'Why should you participate?',
			items: [
				'Help shape the future of education.',
				'Get access to cutting-edge learning tools.',
				'Gain insights on student learning via access to de-identified student interactions with the tool.'
			]
		},
		{
			title: 'What does participation entail?',
			items: [
				'Agree that you and your students will not use other generative AI teaching tools, like ChatGPT, for the duration of the study.',
				"Administer a short (15 minute) online assessment for students at the beginning of the semester, as part of your course's required assignments.",
				'Integrate PingPong into your courses if you are randomly selected to be in the treatment group.',
				"Administer a short (15 minute) online assessment for students at the end of the semester, as part of your course's required assignments."
			]
		}
	];

	const faqs = [
		{
			value: 'irb',
			question: 'Has this study received Institutional Review Board (IRB) approval?',
			answer:
				'Yes, the study has been reviewed and received an exempt determination from the Harvard University-Area IRB. If you need a copy of the approval letter or additional documentation, please contact us directly at support@pingpong-hks.atlassian.net.'
		},
		{
			value: 'requirements',
			question: 'What does the study require from instructors and students?',
			answerItems: [
				'Instructors will integrate a brief baseline and end-of-semester assessment into their courses. Our team will provide instructors with initial versions of these assessments, which will assess general subject-matter knowledge. These activities can be completed in or outside class at the instructor discretion.',
				'When completing the assessment, students will participate in an informed consent process to decide whether their de-identified data can be used in the study. Data will be anonymized and securely stored to protect student privacy. Students who do not consent to study participation will still receive access to PingPong (see below for access timing details).',
				'If admitted to the study, you agree that you and your students will not use other generative AI teaching tools, like ChatGPT, for the duration of the study.'
			]
		},
		{
			value: 'privacy',
			question: 'How is student data used and protected?',
			answer:
				'Only de-identified data will be accessed by the research team. Instructors may choose to use identifiable assessment data for course purposes, but student consent decisions are confidential and will not affect their course participation or grades.'
		},
		{
			value: 'post-study',
			question: 'Will instructors and students receive free access to PingPong after the study?',
			answer:
				'Yes, after the study concludes, all instructors and students —both those in the treatment group and the control group— will receive free access for the following semester. (During the study, instructors and students in the treatment group will have free access to PingPong.)'
		},
		{
			value: 'formats',
			question: 'Does the study accommodate both in-person and online courses?',
			answer:
				'Yes, both in-person and online courses are eligible for participation. If you teach a mix of formats, you can still participate.'
		},
		{
			value: 'dual-credit',
			question: 'Are dual credit courses offered with high schools eligible?',
			answer:
				'Yes, dual credit courses may be eligible, but all student participants must be over 18 years old and provide consent to participate in the study.'
		}
	];
</script>

<svelte:head>
	<title>Educational Access | PingPong Study</title>
</svelte:head>

<div class="min-h-svh bg-[#1f1c3f]">
	<div class="mx-auto flex w-full max-w-6xl flex-col gap-10 px-6 py-10 lg:px-10">
		<header class="flex items-center justify-between text-white">
			<div class="flex items-center">
				<img src="/pingpong_logo_2x.png" alt="PingPong logo" class="h-14 w-auto" />
			</div>
			<Button href="/login" class="bg-white text-base text-slate-900 shadow-sm hover:bg-slate-100">
				Log in
			</Button>
		</header>

		{#if hasApplicationSource}
			<AlertDialog.Root bind:open={showApplicationReferralDialog}>
				<AlertDialog.Content>
					<AlertDialog.Header>
						<AlertDialog.Title>Applications are now closed for Spring 2026</AlertDialog.Title>
						<AlertDialog.Description class="text-base font-light text-foreground">
							Thank you for your interest in the PingPong College Study. To inquire about future
							participation, please contact
							<a
								href="mailto:support@pingpong-hks.atlassian.net"
								rel="noopener noreferrer"
								class="font-medium text-foreground underline underline-offset-4"
								target="_blank"
							>
								support@pingpong-hks.atlassian.net
							</a>.
						</AlertDialog.Description>
					</AlertDialog.Header>
					<AlertDialog.Footer>
						<AlertDialog.Cancel>Close</AlertDialog.Cancel>
					</AlertDialog.Footer>
				</AlertDialog.Content>
			</AlertDialog.Root>
		{/if}

		<Card.Root class="border-white/10 bg-white/95 px-4 py-0 shadow-xl">
			<Card.Content class="space-y-10 p-6 md:p-10">
				<section class="space-y-6">
					<div class="space-y-4">
						<h1
							class="bg-gradient-to-t from-[#201E45] to-[#545193] bg-clip-text text-4xl leading-tight font-bold text-balance text-transparent md:text-5xl lg:text-6xl"
						>
							Educational Access
						</h1>
						<p class="text-lg text-gray-700 md:text-xl lg:w-4/5 lg:text-2xl">
							Participate in a study evaluating the impact of AI on student learning at two- and
							four-year colleges.
						</p>
					</div>
					<div class="space-y-4 text-base text-gray-900">
						<p>
							<strong>PingPong</strong> is an AI-powered virtual teaching assistant based on ChatGPT,
							developed by students and teachers at Harvard. PingPong is designed to help students with
							homework without giving them the answers, much like a human tutor. Our study aims to assess
							how PingPong and similar AI tools can improve education.
						</p>
						<p>
							We are seeking instructors at <strong>two- and four-year colleges</strong>, especially
							those teaching math, economics, statistics and/or computer science, to participate in
							a randomized large-scale study. Initial access to PingPong will be provided to half of
							the participating instructors, with access provided to all instructors in the
							following semester. An
							<strong>honorarium of $1,000</strong> will be available to all eligible participating instructors,
							along with the opportunity to earn bonuses for referring other eligible instructors.
						</p>
						<p>
							<strong> Applications are now closed for Spring 2026 courses. </strong>
							To inquire about future participation, please contact
							<a
								href="mailto:support@pingpong-hks.atlassian.net"
								rel="noopener noreferrer"
								class="font-medium text-foreground underline underline-offset-4"
								target="_blank"
							>
								support@pingpong-hks.atlassian.net
							</a>.
						</p>
					</div>
					<div class="flex flex-wrap items-center gap-3">
						<Button
							href="/login"
							class="bg-[oklch(0.2607_0.071_282.61)] p-4 text-base text-white select-none hover:bg-[oklch(0.225_0.08_282.61)]"
						>
							Instructor login
						</Button>
					</div>
				</section>

				<Separator />

				<section class="space-y-6">
					<div class="space-y-2">
						<h2 class="text-2xl font-semibold">See PingPong in action</h2>
						<p class="text-secondary-foreground">
							A few examples of how students use PingPong throughout the semester.
						</p>
					</div>
					<Carousel.Root class="relative">
						<Carousel.Content>
							{#each slides as slide (slide.title)}
								<Carousel.Item class="md:basis-1/1">
									<Card.Root class="border-muted/60 p-0">
										<Card.Content class="p-0">
											<img
												src={slide.src}
												alt={slide.alt}
												class="w-full rounded-md bg-slate-50 object-contain"
												loading="lazy"
											/>
											<div class="space-y-2 p-6">
												<h3 class="text-lg font-semibold">{slide.title}</h3>
												<p class="text-sm text-secondary-foreground">{slide.description}</p>
											</div>
										</Card.Content>
									</Card.Root>
								</Carousel.Item>
							{/each}
						</Carousel.Content>
						<Carousel.Previous class="start-4 size-12" />
						<Carousel.Next class="end-4 size-12" />
					</Carousel.Root>
				</section>

				<Separator />

				<section class="space-y-6">
					<h2 class="text-2xl font-semibold">Quick facts about PingPong Educational Access</h2>
					<div class="grid gap-4 md:grid-cols-2">
						{#each quickFacts as fact (fact.title)}
							<Card.Root class="gap-2 border-muted/60">
								<Card.Header>
									<Card.Title class="text-lg">{fact.title}</Card.Title>
								</Card.Header>
								<Card.Content>
									<ul
										class="list-disc space-y-2 pl-5 text-base font-light text-secondary-foreground"
									>
										{#each fact.items as item (item)}
											<li>{item}</li>
										{/each}
									</ul>
								</Card.Content>
							</Card.Root>
						{/each}

						<Card.Root class="gap-2 border-muted/60">
							<Card.Header>
								<Card.Title class="text-lg">Who is developing PingPong?</Card.Title>
							</Card.Header>
							<Card.Content class="text-base font-light text-secondary-foreground">
								PingPong was developed by the
								<a
									href="https://policylab.hks.harvard.edu/"
									rel="noopener noreferrer"
									class="font-medium text-foreground underline underline-offset-4"
									target="_blank"
								>
									Computational Policy Lab at Harvard University
								</a>. The lab uses technology to tackle pressing societal issues, including in
								education. We believe that this technology can be particularly powerful at levelling
								educational inequalities. With this study, we aim to understand how artificial
								intelligence can help improve teaching and learning.
							</Card.Content>
						</Card.Root>

						<Card.Root class="gap-2 border-muted/60 md:col-span-2">
							<Card.Header>
								<Card.Title class="text-lg">How can I participate?</Card.Title>
							</Card.Header>
							<Card.Content class="text-base font-light text-secondary-foreground">
								Applications are now closed for Spring 2026 courses. To inquire about future
								participation, please contact
								<a
									href="mailto:support@pingpong-hks.atlassian.net"
									rel="noopener noreferrer"
									class="font-medium text-foreground underline underline-offset-4"
									target="_blank"
								>
									support@pingpong-hks.atlassian.net
								</a>.
							</Card.Content>
						</Card.Root>
					</div>
				</section>

				<Separator />

				<section class="space-y-4">
					<div class="space-y-2">
						<h2 class="text-2xl font-semibold">FAQ for instructors</h2>
						<p class="text-secondary-foreground">Answers to common questions about the study.</p>
					</div>
					<Card.Root class="border-muted/60 py-2">
						<Card.Content>
							<Accordion.Root type="single" class="w-full">
								{#each faqs as faq (faq.value)}
									<Accordion.Item value={faq.value}>
										<Accordion.Trigger class="text-base">{faq.question}</Accordion.Trigger>
										<Accordion.Content class="text-base">
											{#if faq.answerItems}
												<ul
													class="list-disc space-y-2 pl-5 leading-relaxed text-secondary-foreground"
												>
													{#each faq.answerItems as item (item)}
														<li>{item}</li>
													{/each}
												</ul>
											{:else}
												<p class="leading-relaxed text-secondary-foreground">
													{faq.answer}
												</p>
											{/if}
										</Accordion.Content>
									</Accordion.Item>
								{/each}
							</Accordion.Root>
						</Card.Content>
					</Card.Root>
				</section>
			</Card.Content>
		</Card.Root>

		<footer class="flex w-full flex-col gap-8 py-8">
			<div class="flex flex-row items-center justify-evenly gap-2 px-12">
				<div class="w-48">
					<a href="https://shorensteincenter.org/" rel="noopener noreferrer" target="_blank">
						<img
							src="/HKSlogo_shorenstein_transparent-1.png"
							alt="Harvard Kennedy School - Shorenstein Center logo"
						/>
					</a>
				</div>
				<div>
					<a
						href="https://policylab.hks.harvard.edu"
						class="flex flex-row items-center gap-3"
						rel="noopener noreferrer"
						target="_blank"
					>
						<img
							src="/cpl_logo_white.svg"
							style="height: 1.2rem"
							alt="Computational Policy Lab logo"
						/>
						<span class="font-mono text-base text-gray-100">COMPUTATIONAL POLICY LAB</span>
					</a>
				</div>
			</div>
			<p class="mt-4 w-full text-center text-sm text-gray-100">
				All content © 2026 Computational Policy Lab. All rights reserved.
			</p>
		</footer>
	</div>
</div>
