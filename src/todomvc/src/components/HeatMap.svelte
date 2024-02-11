
<script>
	import * as d3 from 'd3';
    
    export let data = [];
    const width = 800;
    const height = width;
    const marginTop = 40;
    const marginRight = 40;
    const marginBottom = 40;
    const marginLeft = 40;
    const mapSize = 16000

    let gx;
    let gy;

    let geoPathGenerator = d3.geoPath()

    //going largely based on https://d3-graph-gallery.com/graph/density2d_shading.html
    // and https://github.com/dsc-courses/dsc106-wi24/blob/main/d3-lecture/src/components/Temperature03Axes.svelte
    $: console.log(data[0]);

    $: x = d3.scaleLinear()
        .domain([0, mapSize])
        .range([ marginRight, width - marginRight ]);

        // Add Y axis
    $: y = d3.scaleLinear()
        .domain([0, mapSize])
        .range([height - marginBottom, marginTop]);

    $: d3.select(gx).call(d3.axisBottom(x).ticks(width / 80))
    $: d3.select(gy).call(d3.axisLeft(y).ticks(height / 80))


    // Compute the rectbin
    var size = 100
    // $: rectbinData = d3.hexbin()
    //     .radius(9) // size of the bin in px
    //     .extent([ [0, 0], [width, height] ])
    // Prepare a color palette
    $: color = d3.scaleLinear()
      .domain([0, 1]) // Points per square pixel.
      .range(["white", "#69b3a2"])
    
 

    // Compute the hexbin data
    $:  densityData = d3.contourDensity()
            .x(function(d) { return x(d.x); })
            .y(function(d) { return y(d.y); })
            .size([width, height])
            .bandwidth(2)
            (data)

    $: console.log(densityData)

    
    
</script>

<div class="visualization">
    <svg 
    {width}
    {height}
    viewBox="0 0 {width} {height}"
    style="max-width: 100%; height: auto;">
        <g  transform="translate({0},{marginBottom})">\
            <!-- https://leagueoflegends.fandom.com/wiki/Summoner%27s_Rift_(League_of_Legends)?file=Summoner%27s_Rift_Minimap.png -->
            <image 
            href="summoners_rift.png" 
                height={height - marginBottom * 2}
                width={width}

             />
        </g>
        <g stroke="#000" stroke-opacity="0.2">
            {#each densityData as d}
                <path
                    d={geoPathGenerator(d)}
                    fill={color(d.value)}
                />
            {/each}
        </g>
        <!-- x-axis -->
        <g bind:this={gx} transform="translate(0,{height - marginBottom})" />
        <!-- y-axis -->
        <g bind:this={gy} transform="translate({marginLeft},0)">
        <!-- map -->
        
    </svg>
</div>