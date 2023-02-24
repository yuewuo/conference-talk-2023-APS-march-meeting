<template>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :snapshot_idx="snapshot_idx_interpolated" :camera_scale="3"></Fusion3d>
    <ExampleBothGrow :scale="scale" :d="d" ref="example1" :tight_edges="tight_edges_1" :time="time"></ExampleBothGrow>
    <Fusion3d :left="2500" ref="fusion3d" :fusion_data="syndrome_graph_fusion_data" :snapshot_idx="snapshot_idx_interpolated" :camera_scale="3" :show_dual_region="false"></Fusion3d>
    <ExampleBothGrow :scale="scale" :d="d" ref="example2" :tight_edges="tight_edges_2" :time="time" :left="2500"></ExampleBothGrow>
</template>

<style>

</style>

<script>
import fusion_3d from './common/fusion_3d.vue'
import example_both_grow from './common/example_both_grow.vue'

const padding = 0.5
const pause = 1
const single_animate = 2
const duration = padding * 2 + pause + single_animate * 2

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
            tight_edges_1: [
                { i1: 5, j1: 4, i2: 5, j2: 6, start: padding + single_animate, animate: 0.3, last: duration },
                { i1: 3, j1: 0, i2: 3, j2: 2, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
                { i1: 7, j1: 2, i2: 7, j2: 4, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
                { i1: 9, j1: 4, i2: 7, j2: 4, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
                { i1: 1, j1: 8, i2: 1, j2: 10, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
                { i1: 7, j1: 8, i2: 7, j2: 10, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
            ],
            tight_edges_2: [
                { i1: 5, j1: 4, i2: 5, j2: 6, start: padding + single_animate, animate: 0.3, last: duration },
                { i1: 3, j1: 0, i2: 3, j2: 2, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
                { i1: 7, j1: 2, i2: 9, j2: 4, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
                { i1: 1, j1: 8, i2: 1, j2: 10, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
                { i1: 7, j1: 8, i2: 7, j2: 10, start: padding + pause + 2 * single_animate, animate: 0.3, last: duration },
            ],
        }
    },
    components: {
        Fusion3d: fusion_3d,
        ExampleBothGrow: example_both_grow,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // get decoding graph data
        let response = await fetch('./common/demo_aps2023_example_decoding_graph.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        // get syndrome graph data
        response = await fetch('./common/demo_aps2023_example_syndrome_graph.json', { cache: 'no-cache', })
        this.syndrome_graph_fusion_data = await response.json()
        console.log("main component mounted")
    },
    computed: {
        snapshot_idx_interpolated() {
            let time = this.time
            if (time < padding) return 0
            if (time < padding + single_animate) {
                return this.smooth_animate((time - padding) / single_animate)
            }
            if (time < padding + pause + single_animate) {
                return 1
            }
            if (time < padding + pause + 2 * single_animate) {
                return this.smooth_animate((time - padding - pause - single_animate) / single_animate) + 2
            }
            return 3
        },
    },
    methods: {
        smooth_animate(ratio) {
            if (ratio < 0) ratio = 0
            if (ratio > 1) ratio = 1
            if (ratio < 0.5) {
                return 2 * ratio * ratio
            }
            return 1 - 2 * (1 - ratio) * (1 - ratio)
        }
    },
    watch: {
        
    },
}
</script>
