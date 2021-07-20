<script lang="ts">
	import {fetchApi} from "./utils";
	import UserList from './components/UserList.svelte';
	import MetadataList from './components/MetadataList.svelte'
	import IdpSettings from './components/IdpSettings.svelte'

	// TODO define type interfaces for returned JSON
	let usersPromise: Promise<string> = fetchApi('users');
	let metadataPromise: Promise<string> = fetchApi('metadata/sp')

	let openTab: number = 1;

	function toggleTabs(tabNumber: number): void{
		openTab = tabNumber
	}
</script>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>

<main>
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
						SP Metadata
					</a>
					<a href="#" class="{openTab === 3 ? 'whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700':'text-base font-medium px-4 py-2 border border-transparent rounded-md shadow-sm text-gray-500 hover:text-gray-900'}" on:click={() => toggleTabs(3)}>
						IDP Settings
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
							{#await metadataPromise}
								<p>Loading...</p>
							{:then metadatas}
								<MetadataList metadatas={metadatas}/>
							{:catch error}
								<p style="color: red">{error.message}</p>
							{/await}
						</div>
						<div class="{openTab === 3 ? 'block':'hidden'}">
							<IdpSettings />
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</main>