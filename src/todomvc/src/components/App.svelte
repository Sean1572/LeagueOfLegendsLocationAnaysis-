<script>
    import { onMount } from 'svelte';
    import HeatMap from '../components/HeatMap.svelte';
    import * as d3 from 'd3';
    
    data = [];

    onMount(async () => {
        d3.csv("test.csv", function(row) {
            data.push({
                "match_ids": row["match_ids]
            })
        });
    })

    $: console.log(data);
</script>

<main>

    <h1>testing</h1>
    <HeatMap />

</main>