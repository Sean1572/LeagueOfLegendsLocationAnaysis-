<script>
    import { onMount } from 'svelte';
    import HeatMap from './HeatMap.svelte';
    import * as d3 from 'd3';
    let data = [];
    let data_win_100 = [];
    let data_win_200 = [];
    let data_lost_100 = [];
    let data_lost_200 = [];
    let allData = []; // Temporary storage for the full dataset
    let currentFrame = 0; 

    onMount(async () => {
        allData = await d3.csv("https://raw.githubusercontent.com/Sean1572/league_data/main/2_09_2024_league_crawl_data_annon.csv");
        console.log("hello")
        updateData(currentFrame);
    });

    //team_id == 100, 200 ,win == True/Fa;lse
    // Filter data
    function updateData(frame) {
        data = allData.filter(d => +d.frame === frame);
        data_win_100 = data.filter(d => d.win === "True" && d.team_id =="100");
        data_win_200 = data.filter(d => d.win === "True" && d.team_id =="200");
        data_lost_100 = data.filter(d => d.win === "False" && d.team_id =="100");
        data_lost_200 = data.filter(d => d.win === "False" && d.team_id =="200");
        
    }
    

    // update the data
    $: currentFrame, updateData(currentFrame);
    $: data_lost_200, console.log("update dataset", data_lost_200)
</script>

<main>
    <h1>Dynamic Heatmap Visualization</h1>
    <input type="range" min="1" max="60" bind:value={currentFrame} />
    <p>Current Frame: {currentFrame}</p>
    <HeatMap bind:data={data_win_100} />
    <HeatMap bind:data={data_win_200} />
    <HeatMap bind:data={data_lost_100} />
    <HeatMap bind:data={data_lost_200} />
</main>
