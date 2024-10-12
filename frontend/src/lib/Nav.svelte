<script lang="ts">
	import { page } from '$app/stores'

	export let navs = [
		{ label: 'Home', href: '/' },
		{ label: 'Chat', href: '/chat' },
		{ label: 'DSL Chat', href: '/dsl_chat' },
		{ label: 'Smart Vendors', href: '/smart_vendors' },
		{ label: 'Vendors', href: '/vendors' }
	]

	import { Header, HeaderNav, HeaderNavMenu, HeaderNavItem } from 'carbon-components-svelte'
</script>

<Header
	company="appRAD"
	platformName=""
	expandedByDefault={false}
	style="background-color: white; color:gray"
>
	<HeaderNav>
		{#each navs as nav}
			<HeaderNavItem href={nav.href} class="navbar-item" text="nav.label">
				<span class:active={$page.url.pathname === nav.href}>{nav.label}</span>
			</HeaderNavItem>
		{/each}
		<HeaderNavMenu text="WIPs: Dropdowns">
			<HeaderNavItem href="/blog" text="Blog" />
			<HeaderNavItem href="/posts" text="Posts" />
			<HeaderNavItem href="/setup" text="Setup" />
			<HeaderNavItem href="/timeline" text="Timeline" />
		</HeaderNavMenu>
	</HeaderNav>
</Header>

<style>
	:global(.active) {
		font-weight: bold;
		text-decoration: underline;
	}
</style>
