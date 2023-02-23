<template>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="0" :top="top1"></Fusion3d>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="3" :top="top2"></Fusion3d>
</template>

<style>

</style>

<script>
import error_model from './common/error_model.vue'
import fusion_3d from './common/fusion_3d.vue'

const animation = 1
const duration = 1.2
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
        }
    },
    components: {
        ErrorModel: error_model,
        Fusion3d: fusion_3d,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // load fusion 3d
        let response = await fetch('./common/demo_aps2023_example_partition.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        console.log("main component mounted")
    },
    computed: {
        top1() {
            let time = this.time
            if (time < animation) {
                return - separation * this.smooth_animate(time / animation)
            }
            return - separation
        },
        top2() {
            let time = this.time
            if (time < animation) {
                return separation * this.smooth_animate(time / animation)
            }
            return separation
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
