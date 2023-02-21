<template>
    <Fusion3d :time="time" ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :snapshot_idx="snapshot_idx_interpolated"></Fusion3d>
    <Fusion3d :left="2500" :time="time" ref="fusion3d" :fusion_data="syndrome_graph_fusion_data" :snapshot_idx="snapshot_idx_interpolated"></Fusion3d>
</template>

<style>

</style>

<script>
import fusion_3d from './common/fusion_3d.vue'

const padding = 1
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
            animated_errors: [],
            animated_syndrome: [],
            decoding_graph_fusion_data: null,
            syndrome_graph_fusion_data: null,
        }
    },
    components: {
        Fusion3d: fusion_3d,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // get decoding graph data
        let response = await fetch('./common/demo_aps2023_decoding_graph_growing.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        // get syndrome graph data
        response = await fetch('./common/demo_aps2023_syndrome_graph_growing.json', { cache: 'no-cache', })
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
                return this.smooth_animate((time - padding - pause - single_animate) / single_animate) + 1
            }
            return 2
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
