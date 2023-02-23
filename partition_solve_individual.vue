<template>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="snapshot_idx_interpolated" :top="-separation"></Fusion3d>
    <ExampleBothGrow :scale="scale" :d="d" ref="example1" :tight_edges="tight_edges_1" :time="time" :top="-separation"></ExampleBothGrow>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="3 + snapshot_idx_interpolated" :top="separation"></Fusion3d>
    <ExampleBothGrow :scale="scale" :d="d" ref="example2" :tight_edges="tight_edges_2" :time="time" :top="separation"></ExampleBothGrow>
</template>

<style>

</style>

<script>
import fusion_3d from './common/fusion_3d.vue'
import example_both_grow from './common/example_both_grow.vue'

const showing = 2
const duration = showing + 0.5

const separation = 150

export default {
    props: {
        "scale": { type: Number, default: 1, },
        "time": Number,
        "d": { type: Number, default: 5, },
    },
    emits: ["duration-is"],
    data() {
        return {
            animated_errors: [],
            animated_syndrome: [],
            decoding_graph_fusion_data: null,
            separation: separation,
            tight_edges_1: [
                { i1: 3, j1: 0, i2: 3, j2: 2, start: showing, animate: 0.3, last: duration },
                { i1: 1, j1: 8, i2: 1, j2: 10, start: showing, animate: 0.3, last: duration },
            ],
            tight_edges_2: [
                { i1: 7, j1: 2, i2: 7, j2: 4, start: showing, animate: 0.3, last: duration },
                { i1: 9, j1: 4, i2: 7, j2: 4, start: showing, animate: 0.3, last: duration },
                { i1: 7, j1: 8, i2: 7, j2: 10, start: showing, animate: 0.3, last: duration },
            ],
        }
    },
    components: {
        Fusion3d: fusion_3d,
        ExampleBothGrow: example_both_grow,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // load fusion 3d
        let response = await fetch('./common/demo_aps2023_example_partition.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        console.log("main component mounted")
    },
    computed: {
        snapshot_idx_interpolated() {
            let time = this.time
            if (time < showing) {
                return this.smooth_animate(time / showing)
            }
            return 1
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
