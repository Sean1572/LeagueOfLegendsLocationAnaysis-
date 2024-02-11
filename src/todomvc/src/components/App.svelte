<script>
    import { onMount } from 'svelte';
    import HeatMap from '../components/HeatMap.svelte';
    import * as d3 from 'd3';
    
    let data = [];

    // //Frame / Win / Loss
    // let data = {

    //     0: {
    //         window
    //     },
    //     1: []
    // };

    onMount(async () => {
        await d3.csv("test19.csv", function(row) {
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