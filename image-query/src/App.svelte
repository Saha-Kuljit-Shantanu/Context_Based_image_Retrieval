<script>
    import Router from "svelte-spa-router";
    import b from "./1.svelte" 
    import home from "./home.svelte"
</script>

<!-- <nav>
    <a href="/">Home</a>
    <a href="/#/1">1</a>
</nav> -->

<Router routes={{
    '/1' : b,
    '/' : home
}}/>