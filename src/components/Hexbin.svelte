<script>
    import * as d3 from 'd3';
    import { hexbin } from 'd3-hexbin';
    import { onMount } from 'svelte';

    export let data = [];
    let svg;
    const width = 650, height = 650;
    const marginBottom = 40, marginLeft = 10, marginTop = 30, marginRight = 40;

    var color = d3.scaleLinear()
        .domain([30, 300])
        .range(["white","red"]);

    let hexbinGenerator = hexbin().radius(20).extent([[0, 0], [width, height]]);

    $: x = d3.scaleLinear().domain([0, 16000]).range([marginRight + marginLeft, width - marginRight]);
    $: y = d3.scaleLinear().domain([0, 16000]).range([height - marginBottom, marginTop]);


</script>

<div class="visualization">
    <svg {width} {height} viewBox="0 0 {width} {height}" style="max-width: 100%; height: auto;">
        <g transform={`translate(0,${marginBottom})`}>
            <image href="summoners_rift.png" height={height - marginBottom * 2} width={width} />
        </g>
        <g fill-opacity="0.5">
            {#each hexbinGenerator(data.map(d => [x(d.x), y(d.y)])) as hex}
                <path
                    d={hexbinGenerator.hexagon()}
                    transform={`translate(${hex.x},${hex.y})`}
                    fill={color(hex.length)}
                />
            {/each}
        </g>
    </svg>
</div>
