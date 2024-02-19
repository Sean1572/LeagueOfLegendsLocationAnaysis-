<script>
    import { onMount } from 'svelte';
    import HeatMap from './HeatMap.svelte';
    import Hexbin from './Hexbin.svelte';
    import * as d3 from 'd3';

    let loaded = false
    let transition_div_class = "start_"
    let data = [];
    let data_to_display = [];
    let data_win_100 = [];
    let data_win_200 = [];
    let data_lost_100 = [];
    let data_lost_200 = [];
    let allData = []; // Temporary storage for the full dataset
    let filters = {
        
        "team_id": false,
        "win": false,
    };
    let currentFrame = 0; 
    let filter_categories = {};
    let label = {}
    let displayMode = 'heatmap';
    let isHeatmap = true;

    //DEBUG
    function sleep(milliseconds) {
        const date = Date.now();
        let currentDate = null;
        do {
            currentDate = Date.now();
        } while (currentDate - date < milliseconds);
    }
    //DEBUG




    onMount(async () => {
        allData = await d3.csv("https://raw.githubusercontent.com/Sean1572/league_data/main/2_09_2024_league_crawl_data_annon.csv");
        console.log("hello")
        
        Object.entries(filters).forEach(entry => {
            const [column, enabaled] = entry;
                //https://d3-graph-gallery.com/graph/basic_datamanipulation.html
                //Make a heap for the columns, g;et the keys in an array for the unique values:
                let categories = {};
                d3.map(allData, function(d){categories[d[column]] = 1});
                console.log(Object.keys(categories));
                
                //for each unqiue category create a filter for it
                filter_categories[column] = Object.keys(categories);
        });
        sleep(1000);
        updateData(currentFrame);
        loaded=true;
        transition_div_class="loaded_";
    });


    // The next 2 functions get pairwise categories
    //select potential filters
    function combinations(combinations) {
        let end_goal = 1
        Object.values(combinations).forEach(list => {
            end_goal *= list.length
        });
        let num_categories = Object.keys(combinations).length
        //https://stackoverflow.com/questions/1295584/most-efficient-way-to-create-a-zero-filled-javascript-array
        let index = new Array(num_categories).fill(0);
        let combinations_result = []
        return combinations_recursive(combinations_result, combinations, index, end_goal)
    }

    function combinations_recursive(combinations_result, combinations, index, end_goal) {
        let mini_result = []
        for (let i = 0; i<index.length; i++) {
            //get the ith column, with the unique category index[i]
            mini_result.push(combinations[Object.keys(combinations)[i]][index[i]]);
        }
        
        //console.log(index, mini_result)
        //increment index
        for (let i = index.length-1; i>= 0; i--) {
            index[i]++
            if (combinations[Object.keys(combinations)[i]].length <= index[i]) {
                index[i] = 0
            } else {
                break;
            }
        }
        

        combinations_result.push(mini_result);
        if (combinations_result.length < end_goal) {
            return combinations_recursive(combinations_result, combinations, index, end_goal);
        } else {
            return combinations_result;
        }
    }

    // Filter data
    function updateData(frame) {
        

        data = allData.filter(d => +d.frame === frame);

        data_to_display = [];

        //Get all pairwise categories we want to filter by only if user enables them
        console.log("start combatorics")
        let only_enabled_filters = {}
        Object.entries(filters).forEach(entry => {
            const [column, enabled] = entry;
            if (enabled) {
                only_enabled_filters[column] = filter_categories[column]
            }
        });
        //console.log("combinatorics", only_enabled_filters, filter_categories)
        let filters_selected = combinations(only_enabled_filters)
        
        console.log("end combatorics")


        //create the data splits to display
        if (filters_selected[0].length == 0) {
            data_to_display.push({
                    "data": data,
                    "label": "All Data"
                })
        } else {
            for (const a_filter_seleced of filters_selected) {
                console.log("make data", filters_selected)
                let mini_data = data.filter(d => {
                    let filter_data = true;
                    for (let i = 0; i < a_filter_seleced.length; i++) {
                        let column = Object.keys(only_enabled_filters)[i]
                        filter_data = filter_data && (d[column] === a_filter_seleced[i])
                    }
                    return filter_data
                })

                data_to_display.push({
                    "data": mini_data,
                    "label": a_filter_seleced.join(" ")
                })
                console.log("end data")
            }
        }

        // data_win_100 = data.filter(d => d.win === "True" && d.team_id =="100");
        

        // //filter the data down
        // data_win_100 = data.filter(d => d.win === "True" && d.team_id =="100");
        // data_win_200 = data.filter(d => d.win === "True" && d.team_id =="200");
        // data_lost_100 = data.filter(d => d.win === "False" && d.team_id =="100");
        // data_lost_200 = data.filter(d => d.win === "False" && d.team_id =="200");
        
    }

    function myFunction(event) {
        let option = event.target
        filters[option.id] = option.checked
        console.log("testing", filters, event)
    }
    

    // update the data
    $: filters, updateData(currentFrame);
    $: currentFrame, updateData(currentFrame);
    $: displayMode = isHeatmap ? 'heatmap' : 'hexbin';
    
</script>

<main>
    <div class={transition_div_class + !loaded}> 
        <h1>Please wait while the visualization loads in, thank you!</h1>
    </div>

    <div class={transition_div_class + loaded}> 
        <h1>Player Movement In League Of Legends Summoner's Rift</h1>
        <div class="slider-container">
            <input type="range" min="0" max="60" bind:value={currentFrame}>
        </div>
        <p>Current Frame: {currentFrame}</p>

        <form >
            
            <div class="checkbox">
                <input type="checkbox" id="team_id" name="team_id" value="team_id" on:change={(event) => myFunction(event)}>
                <label for="team_id"> Team</label><br>
            </div>
            <div class="checkbox">
                <input type="checkbox" id="win" name="win" value="win" on:change={(event) => myFunction(event)}>
                <label for="win"> Win</label><br>
            </div>
        </form>

        <div class='heathex_toggle'>
            <label class="switch">
                <input type="checkbox" bind:checked={isHeatmap}>
                <span class="slider round"></span>
                <span class="heatlabel">Heatmap</span>
                <span class="hexlabel">Hexbin</span>
            </label>
        </div>
        
        <div class='heatmap-container'>
            {#each data_to_display as details}
                <div class='heatmap-container-item'>
                    <p class='label'>{details["label"]}</p>
                    {#if displayMode === 'heatmap'}
                        <HeatMap bind:data={details["data"]}/>
                    {:else}
                        <Hexbin bind:data={details["data"]}/>
                    {/if}
                </div>
            {/each}
        </div>
    </div>
</main>

<style>
    /* Handling Loading Screen*/

    /* THE DIVS CONTAINING DATA */
    .start_false {
        opacity: 0;
        position: relative;
    }
    
    .loaded_true {
        position: relative;
        opacity: 1;
        transition:
            opacity 2s 2s;
    }

    /* THE DIVS CONTAINING PLEASE WAIT MESSAGE */
    .loaded_false {
        width: -moz-available;
        height: -moz-available;
        text-align: center; 
        position: absolute;
        opacity: 0;
        transition:
            opacity 2s;
    }

    .start_true {
        
        width: -moz-available;
        text-anchor: "middle";
        text-align: center;
        position: absolute;
        opacity: 1;
    }

    


    /* title */
    main h1 {
      font-size: 2.5em; 
      font-weight: bold; 
      color: #8400ff;
      text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.25); 
      font-family: 'Arial Black', Gadget, sans-serif; 
      text-align: center; 
      margin-top: 20px; 
      margin-bottom: 20px; 
    }
  

    /* label of the graph filter * /
    /* https://stackoverflow.com/questions/7720730/how-to-align-absolutely-positioned-element-to-center */
    /* used above but adapted for flex box */
    .label {
        position: absolute;
        margin-left: auto;
        margin-right: auto;
        display: flex;
        padding-left: 8%;
    }
  
    /* current frame */
    p {
      text-align: center; 
      font-size: 20px; 
      font-family: 'Arial', Gadget, sans-serif; 
    }

    /* heatmaps */
    .heatmap-container {
        width: 100%;
        display: flex;
        justify-content: center; 
        align-items: center; 
        flex-direction: row; 
    }
    

    /* slider */
    .slider-container {
        text-align: center;
        margin: 20px 0;
    }

    /*slider track */
    input[type='range'] {
        -webkit-appearance: none;
        appearance: none;
        width: 40%; 
        height: 8px; 
        background: #ddd; 
        opacity: 0.7; 
        transition: opacity 0.2s;
    }

    /* hover effect for the track */
    input[type='range']:hover {
        opacity: 1; 
    }

    /* draggable */
    input[type='range']::-webkit-slider-thumb {
        -webkit-appearance: none; 
        appearance: none;
        width: 20px; 
        height: 20px; 
        background: #8c2dcc; 
        cursor: pointer; 
        border-radius: 50%; 
    }

    input[type='range']::-moz-range-thumb {
        width: 20px; 
        height: 20px; 
        background: #8c2dcc; 
        cursor: pointer; 
        border-radius: 50%; 
    }

    /* checkbox form */
    form {
        text-align: center; 
        margin-bottom: 20px;
        display: block ruby; 
    }

    .checkbox input[type="checkbox"] {
        display: none;
    }

    /* checkbox labels */
    .checkbox label {
        position: relative;
        padding-left: 28px; 
        cursor: pointer;
        display: inline-block;
        line-height: 23px; 
    }

    .checkbox label {
        font-size: 23px; 
        color: #333; 
        cursor: pointer;
        font-family: georgia, sans-serif; 
        user-select: none; 
    }

    .checkbox {
        margin-bottom: 10px; 
        margin-left: 1%;
        margin-right: 1%;
    }

    /* checkbox boxes */
    .checkbox label::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 20px; 
        height: 20px;
        border: 2px solid #9B9B9B; 
        border-radius: 4px; 
        background-color: white; 
    }

    /* checkmarks */
    .checkbox input[type="checkbox"]:checked + label::after {
        content: '';
        position: absolute;
        left: 8px;
        top: 3px;
        width: 5px;
        height: 15px;
        border: solid #8c2dcc;
        border-width: 0 2px 2px 0;
        transform: rotate(45deg);
    }

    /* heathex toggle slider */
    .heathex_toggle{
        color: white; 
        border: none; 
        border-radius: 5px; 
        cursor: pointer;
        font-size: 16px; 
        transition: background-color 0.3s, transform 0.3s;
        display: flex;
        justify-content: center; 
        flex-wrap: wrap; 
        gap: 20px;
    }

    /* heathex switch */
    .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }

    .switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }


    /* right heatlabel */
    .heatlabel{
        position: absolute;
        color: #686868;
        top: 50%;
        transform: translateY(-50%);
        left: 75px;
        font-size: 24px;
    }

    /* left hexlabel */
    .hexlabel {
        position: absolute;
        color: #ff4b4b;
        top: 50%;
        transform: translateY(-50%);
        right: 75px; 
        font-size: 24px;
    }

    /* heathex slider */
    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ff0000; 
        transition: .4s;
        border-radius: 34px; 
        display: flex;
        justify-content: center;
        flex-wrap: wrap; 
    }

    .slider:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px; 
        left: 4px;
        bottom: 4px;
        background-color: white; 
        transition: .4s;
        border-radius: 50%;
    }

    /* color when the switch flipped */
    input:checked + .slider {
        background-color: #8c2dcc; 
    }

    /* Move knob when flipped */
        input:checked + .slider:before {
        transform: translateX(26px);
    }
</style>
