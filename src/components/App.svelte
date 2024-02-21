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
                    "label": a_filter_seleced.join(" ").replace("False", "Lost").replace("True", "Won")
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

    let frame_num = ""
    let frame_message = ""
    function update_message() {
        if (currentFrame == 0) {
            frame_num = "Minutes in Game: 0"
            frame_message = "Here we are at the start of the game, all the players are at spawn. Note there are 3 lanes (top, middle, and bottom) with two rivers. The circles next to the rivers are boss spawns. The goal is to break the opposing side's nexus."
        } else if (currentFrame == 1) {
            frame_num = "Minutes in Game: 1"
            frame_message = "Players are moving into the top and middle lanes. Players who are going to the bottom lane are helping the player in the jungle at their buffs."
        }
        else if (currentFrame == 2) {
            frame_num = "Minutes in Game: 2" 
            frame_message = "Bottom lane players have left the jungle, junglers moving to second camps."
        }
        else if (currentFrame == 3) {
            frame_num = "Minutes in Game: 3"
            frame_message = "We are starting to see more variance in player movement: junglers moving to next camp, players spread out in lane, handful of players at spawn who had an early loss."
        }
        else if (currentFrame == 4) {
            frame_num = "Minutes in Game: 4" 
            frame_message = "We are starting see more variance in player movement, jungle moving to next camp, players spread out in lane, handful of players at spawn who had an early loss."
        }
        else if (currentFrame == 5) {
            frame_num = "Minutes in Game: 5" 
            frame_message = "We see the first 'ganks' where the player in jungle uses the river to help the laning players."
        }
        else if (currentFrame >= 6 && currentFrame < 9) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "Watch the river! Some of the first bosses (dragon and baron nashor) have spawned so more players are there."
        }
        else if (currentFrame >= 9 && currentFrame < 10) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "We start seeing much more variance in games, we typically see much more activity in bottom lane."
        }
        else if (currentFrame >= 10 && currentFrame < 13) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "We start seeing much more presence in the top river. Players begin fighting for the big objective on the top side of the map at this stage of the game."
        }
        else if (currentFrame >= 13 && currentFrame < 17) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "We start seeing more activity further up and down the lanes as towers start to fall allowing players to push forward."
        }
        else if (currentFrame >= 17 && currentFrame < 20) {
            frame_num = "Minutes in Game: " + currentFrame 
            frame_message = "At this point the laning phase is mostly done, watch as bottom and top lane become a much less popular place."
        }
        else if (currentFrame >= 20 && currentFrame < 22) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "Mid lane becomes a key target, players are roaming jungle much more chaotically now (We recommend turning on some of the filters, around now you can see how the winning and lossing us on midlane and the river)."
        }
        else if (currentFrame >= 22 && currentFrame < 25) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "If you haven't already, start turning on those filters, around now you can start seeing how much map control the diffrent sides and winning teams have."
        }
        else if (currentFrame >= 25 && currentFrame < 30) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "Players are spread out more, at this late stage of the game, players start adapting more to individual games, and follow much less set patterns."
        }
        else if (currentFrame >= 30 && currentFrame < 40) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "Most games are ending around now, players are now spending more time at nexuses of the losing team, players are mostly grouping mid."
        }
        else if (currentFrame >= 40 && currentFrame < 60) {
            frame_num = "Minutes in Game: " + currentFrame
            frame_message = "As games start to end, we have fewer and fewer datapoints for these really long games, so the data becomes more scarce over time."
        }
        else if (currentFrame == 60) {
            frame_num = "Minutes in Game: " + currentFrame 
            frame_message = "The longest game lasted for about 60 minutes, you can see just 10 players at this point since there is only 1 game in our data now. Looks like red side is losing."
        }
        // currentframe 5 we see frist "ganks" where jungle uses the river to help the lanes
        // currentframe 6,7,8 the frist bosses spawn in river "barron" and "dragon" close to top and bottom lane,
        // current frame 9,10, 11, 12 We start seeeing much more variance in games, we typically see much more activity in bottom lane
        // current frame 13 - 17 we start seeing more activity further up and down the lanes as towers start to fall allowing players to push forward
        // current frame 18 - 20 at this point the lane phase is mostly done, watch as bottom and top lane becomes a much less popular place
        // current frame 20 - mid lane becomes a key target, people are roaming jungle much more chaotically now as people focWe recommend turning on some of the filters, around now you can see how the winning and lossing us on midlane and the river
        // current frame 22 - sides have much more map control
        // current frame 25 - Players are spread out more, you will notice that also the data becomes less as time goes on, an adverage match will end soon
        // current frame 30 - at this point players are just going back and forth just trying to push close enough to the opposing nexus for victory, winning teams spend a lot of time on the opposite side
        // current frame 40 - Most games do not last this long, many of the data points you will see now represent indivual players, at this stage, games no long follow a set script
        // current frame 60 - The longest game last for about 60 minutes, you can see just 10 players at this point since there is only 1 game in our data now 



        else {
            frame_message = "Current Frame: " + currentFrame;
        }
    }
    

    // update the data
    $: filters, updateData(currentFrame);
    $: currentFrame, updateData(currentFrame), update_message();
    $: displayMode = isHeatmap ? 'heatmap' : 'hexbin';
    
</script>

<main>
    <div class={transition_div_class + !loaded}> 
        <h1>Please wait while the visualization loads in, thank you!</h1>
    </div>

    <div class={transition_div_class + loaded}> 
        <h1>League of Legends: Player Movement Patterns on Summoner's Rift</h1>
        <div class="slider-container">
            <input type="range" min="0" max="60" bind:value={currentFrame}>
        </div>

        <div class="frame_message_div">
            <p style="margin-block-start: 0;
            margin-block-end: 0;">{frame_num}</p>
            <p style="margin-block-start: 0;
            margin-block-end: 0;">{frame_message}</p>
        </div>

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
        <div class='disclaimer_text'>
            <p>
                Hello! This visualization uses data from league games from across rank and causal play to see player movement over time. 
                To move through time: use the slider
                If you want to filter the data by if that team won, and the side the players are on, use the checkboxes above.

                
                Writeup for the visualization can be found at <a href="https://docs.google.com/document/d/1J5RdQfsPoy5ICeKG5RTZqPyxcE6aeAQPJTv0Q-zu9yU/edit?usp=sharing">this google docs</a>
            </p>
            <p>
                Map for Summoners Rift as well as background images all belong to Riot Games
            </p>
        </div>
    </div>
</main>

<style>

    /* above was a key bit of googling for centering the elements */
    /* https://stackoverflow.com/questions/7720730/how-to-align-absolutely-positioned-element-to-center */


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
        margin-left: auto;
        margin-right: auto;
        text-align: center; 
        left: 0;
        right: 0;
        position: absolute;
        opacity: 0;
        transition:
            opacity 2s;
    }

    .start_true {
        align-content: center;
        margin-left: auto;
        margin-right: auto;
        left: 0;
        right: 0;
        text-anchor: "middle";
        text-align: center;
        position: absolute;
        opacity: 1;
    }

    


    /* title */
    main h1 {
      font-size: xx-large; 
      font-weight: bold; 
      color: #8400ff;
      text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.25); 
      font-family: 'Arial Black', Gadget, sans-serif; 
      text-align: center; 
      margin-top: 20px; 
      margin-bottom: 20px; 
    }
  

    /* label of the graph filter * /
    /* used above but adapted for flex box */
    .label {
        position: absolute;
        margin-left: auto;
        margin-right: auto;
        display: flex;
        padding-left: 8%;
    }
  
    a {
        color: #ffffff;
    }
    /* current frame */
    p {
      
      text-align: center; 
      font-size: 20px; 
      font-family: 'Roboto', Gadget, sans-serif; 
      margin-left: auto;
      margin-right: auto;
      
      line-clamp: 2;
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
        display: flex;
        justify-content: center;

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
        line-height: 22px; 
    }

    .checkbox label {
        font-size: 20px; 
        color: #333; 
        cursor: pointer;
        font-family: "roboto", sans-serif; 
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
        bottom: 0;
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
        top: 1px;
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
        font-family: "roboto", sans-serif; 
    }

    /* left hexlabel */
    .hexlabel {
        position: absolute;
        color: #ff4b4b;
        top: 50%;
        transform: translateY(-50%);
        right: 75px; 
        font-size: 24px;
        font-family: "roboto", sans-serif; 
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

    /* move knob when flipped */
        input:checked + .slider:before {
        transform: translateX(26px);
    }

    .disclaimer_text{
        color:#ffffff;
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        display: inline-block;
        font-family: "roboto", sans-serif; 
    }

    .frame_message_div {
        font-family: "roboto", sans-serif;
        padding-left: 10%;
        padding-right:  10%;
        margin-bottom: 20px;
        font-size: 15px;
        overflow-y: scroll;
        height: 100px;
    }
</style>
