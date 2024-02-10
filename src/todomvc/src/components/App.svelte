<script>
    import { onMount } from 'svelte';
    import HeatMap from '../components/HeatMap.svelte';
    import * as d3 from 'd3';
    
    let data = [];

    onMount(async () => {
        await d3.csv("test1.csv", function(row) {
            data.push({
                "x": row['x'],
                "y": row['y']
            })
        });
        data=data; //???????
    })

    
</script>

<main>

    <h1>testing</h1>
    <HeatMap bind:data={data} />
    <HeatMap bind:data={data} />

</main>