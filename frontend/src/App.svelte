<script lang="ts">
	import UserList from './components/UserList.svelte';
	// move to users list component
	async function getUsers() {
		const res = await fetch(`users`);
		const json = await res.json();

		if (res.ok) {
			return json;
		} else {
			throw new Error(json);
		}
	}

	let usersPromise = getUsers();

	let openTab: number = 1;

	function toggleTabs(tabNumber: number){
		openTab = tabNumber
	}
</script>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>

<main>
		<!--{#await users}-->
		<!--	<p>Loading...</p>-->
		<!--{:then user}-->
		<!--	{#each user as user}-->
		<!--		<User {...user}/>-->
		<!--	{/each}-->
		<!--{:catch error}-->
		<!--	<p style="color: red">{error.message}</p>-->
		<!--{/await}-->
	<div class="relative bg-white">
		<div class="max-w-7xl mx-auto px-4 sm:px-6">
			<div class="flex justify-between items-center border-b-2 border-gray-100 py-6 md:justify-start md:space-x-10">
				<div class="flex justify-start lg:w-0 lg:flex-1">
					<a href="#">
						<img class="h-8 w-auto sm:h-10" src="https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg" alt="">
					</a>
				</div>
				<nav class="hidden md:flex space-x-10">
					<a href="#" class="{openTab === 1 ? 'whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700':'text-base font-medium px-4 py-2 border border-transparent rounded-md shadow-sm text-gray-500 hover:text-gray-900'}" on:click={() => toggleTabs(1)}>
						Users
					</a>
					<a href="#" class="{openTab === 2 ? 'whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700':'text-base font-medium px-4 py-2 border border-transparent rounded-md shadow-sm text-gray-500 hover:text-gray-900'}" on:click={() => toggleTabs(2)}>
						Metadata
					</a>
					<a href="#" class="{openTab === 3 ? 'whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700':'text-base font-medium px-4 py-2 border border-transparent rounded-md shadow-sm text-gray-500 hover:text-gray-900'}" on:click={() => toggleTabs(3)}>
						Settings
					</a>
				</nav>
				<div class="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
					<a href="https://github.com/doshmajhan/idpy" class="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900">
						Documentation
					</a>
				</div>
			</div>
			<div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
				<div class="px-4 py-5 flex-auto">
					<div class="tab-content tab-space">
						<div class="{openTab === 1 ? 'block':'hidden'}">
							{#await usersPromise}
								<p>Loading...</p>
							{:then users}
									<UserList users={users}/>
							{:catch error}
								<p style="color: red">{error.message}</p>
							{/await}
						</div>
						<div class="{openTab === 2 ? 'block':'hidden'}">
							<p>
								Completely synergize resource taxing relationships via
								premier niche markets. Professionally cultivate one-to-one
								customer service with robust ideas.
								<br />
								<br />
								Dynamically innovate resource-leveling customer service for
								state of the art customer service.
							</p>
						</div>
						<div class="{openTab === 3 ? 'block':'hidden'}">
							<p>
								Efficiently unleash cross-media information without
								cross-media value. Quickly maximize timely deliverables for
								real-time schemas.
								<br />
								<br />
								Dramatically maintain clicks-and-mortar solutions
								without functional solutions.
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</main>