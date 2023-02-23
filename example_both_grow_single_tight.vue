<template>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :snapshot_idx="1" :camera_scale="3"></Fusion3d>
    <ExampleBothGrow :scale="scale" :d="d" ref="example1" :tight_edges="[ { i1: 3, j1: 0, i2: 3, j2: 2 } ]"></ExampleBothGrow>
    <Fusion3d :left="2500" ref="fusion3d2" :fusion_data="syndrome_graph_fusion_data" :snapshot_idx="1" :camera_scale="3" :show_dual_region="false"></Fusion3d>
    <ExampleBothGrow :left="2500" :scale="scale" :d="d" ref="example2" :tight_edges="[ { i1: 3, j1: 0, i2: 3, j2: 2 } ]"></ExampleBothGrow>
</template>

<style>

</style>

<script>
import fusion_3d from './common/fusion_3d.vue'
import example_both_grow from './common/example_both_grow.vue'

const duration = 1

export default {
    props: {
        "scale": { type: Number, default: 1, },
        "time": Number,
        "d": { type: Number, default: 5, },
    },
    emits: ["duration-is"],
    data() {
        return {
            decoding_graph_fusion_data: null,
            syndrome_graph_fusion_data: null,
        }
    },
    components: {
        Fusion3d: fusion_3d,
        ExampleBothGrow: example_both_grow,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // get decoding graph data
        let response = await fetch('./common/demo_aps2023_example_decoding_graph_grow_single.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        // get syndrome graph data
        response = await fetch('./common/demo_aps2023_example_syndrome_graph_grow_single.json', { cache: 'no-cache', })
        this.syndrome_graph_fusion_data = await response.json()
        console.log("main component mounted")
    },
    computed: {
        
    },
    methods: {
        
    },
    watch: {
        
    },
}
</script>
