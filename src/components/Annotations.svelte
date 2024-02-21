
<script>
    export let time = 1;
    export let side = "All Data";
    // formmat is x,y, text
    let annotations = [[650/2, 650/2, "Mid Lane"]]

    function update_annotations() {
        if (time == 0) {
            annotations = [
                [650/2-50, 650/2+35, "Mid Lane"],
                [80, 180, "top Lane"],
                [450, 550, "Bottom Lane"]
            ]
        }


        else {
            annotations = []
        }
    }
    
    $: time, update_annotations();
  
</script>

<g class="annotations">
        <!-- https://developer.mozilla.org/en-US/docs/Web/SVG/Element/text -->
        {#each annotations as anno}
            <text x="{anno[0]}" y="{anno[1]}">{anno[2]}</text>
        {/each}
</g>

<style>


text {
    fill: #8400ff;
    font-family: 'Arial Black', Gadget, sans-serif; 
    text-align: center; 
  }
</style>