<script>
    import { onMount } from 'svelte';
    import HeatMap from './HeatMap.svelte';
    import * as d3 from 'd3';
    let data = [];
    let allData = []; // Temporary storage for the full dataset
    let currentFrame = 0; 

    onMount(async () => {
        allData = await d3.csv("https://raw.githubusercontent.com/Sean1572/league_data/main/2_09_2024_league_crawl_data_annon.csv");
        console.log("hello", allData)
        updateData(currentFrame);
    });

    // Filter data
    function updateData(frame) {
        data = allData.filter(d => +d.frame === frame);
    }
    

    // update the data
    $: currentFrame, updateData(currentFrame);
</script>

<main>
    <h1>Dynamic Heatmap Visualization</h1>
    <input type="range" min="1" max="60" bind:value={currentFrame} />
    <p>Current Frame: {currentFrame}</p>
    <HeatMap {data} />
</main>
