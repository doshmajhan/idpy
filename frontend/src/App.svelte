<script lang="ts">
	import {fetchApi} from "./utils";
	import Dashboard from "./components/Dashboard.svelte";

	// TODO define type interfaces for returned JSON
	let usersPromise: Promise<string> = fetchApi('users');
	let metadataPromise: Promise<string> = fetchApi('metadata/sp')
</script>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>


<Dashboard usersPromise={usersPromise} metadataPromise={metadataPromise}/>
