<template>
    <!-- <div class="screen"></div>
    <div class="titles"></div> -->
    <Fusion3d ref="fusion3d1" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="snapshot_idx(0)" :width="1800" :height="2160" :left="left(0)"></Fusion3d>
    <Fusion3d ref="fusion3d2" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="snapshot_idx(1)" :width="1800" :height="2160" :left="left(1)"></Fusion3d>
    <Fusion3d ref="fusion3d3" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="snapshot_idx(2)" :width="1800" :height="2160" :left="left(2)"></Fusion3d>
    <Fusion3d ref="fusion3d4" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="snapshot_idx(3)" :width="1800" :height="2160" :left="left(3)"></Fusion3d>
    <div class="mask" :style="{ 'opacity': 0.8 * time_ratio(fast_first_animation) }"></div>
</template>

<style scoped>
.screen {
    position: absolute;
    top: 0;
    left: 0;
    height: 2160px;
    width: 3840px;
    background-color: rgba(255, 0, 0, 0.227);
}
.titles {
    position: absolute;
    top: 170px;
    left: 190px;
    width: 1680px;
    height: 500px;
    background-color: lightblue;
}
.mask {
    position: absolute;
    top: 700px;
    left: 190px;
    width: 1680px;
    height: 1400px;
    background-color: white;
}
</style>

<script>
import error_model from './common/error_model.vue'
import fusion_3d from './common/fusion_3d.vue'

const animation = 2
const duration = 2.2

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
        let response = await fetch('./common/demo_aps2023_large_demo.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        // updates cameras
        for (let i=0; i<100; ++i) await Vue.nextTick()
        this.update_cameras()
        console.log("main component mounted")
    },
    computed: {

    },
    methods: {
        time_ratio(smooth_func=null) {
            let ratio = 0
            let time = this.time
            if (time < animation) {
                if (smooth_func == null) {
                    ratio = this.smooth_animate(time / animation)
                } else {
                    ratio = smooth_func(time / animation)
                }
            } else {
                ratio = 1
            }
            return ratio
        },
        update_cameras() {
            for (let i=1; i<=4; ++i) {
                const camera = this.$refs[`fusion3d${i}`].camera
                const orbit_control = this.$refs[`fusion3d${i}`].orbit_control
                let bias = [-12,-2,8,18][i-1]
                if (i <= 2) {
                    camera.zoom = 0.3
                    camera.position.set(180, 60 + bias, 1000)
                    camera.updateProjectionMatrix()
                    orbit_control.target.set(0, bias, 0 )
                } else {
                    let ratio = this.time_ratio(this.slow_first_animation)
                    let fast_ratio = this.time_ratio(this.fast_first_animation)
                    camera.zoom = 0.3 * (1-ratio) + 0.7 * ratio
                    let delta = bias * (1-fast_ratio) + 10 * fast_ratio
                    camera.position.set(180, 60 + delta, 1000)
                    camera.updateProjectionMatrix()
                    orbit_control.target.set(0, delta, 0 )
                }
            }
        },
        snapshot_idx(idx) {
            const moves = [
                [0, 2],
                [5, 8],
                [11, 13],
                [16, 18]
            ][idx]
            return moves[1] + 1
        },
        smooth_animate(ratio) {
            if (ratio < 0) ratio = 0
            if (ratio > 1) ratio = 1
            if (ratio < 0.5) {
                return 2 * ratio * ratio
            }
            return 1 - 2 * (1 - ratio) * (1 - ratio)
        },
        fast_first_animation(ratio) {
            return 1 - Math.pow((1 - ratio), 6)
        },
        slow_first_animation(ratio) {
            return Math.pow(ratio, 6)
        },
        left(idx) {
            let ratio = this.time_ratio()
            if (idx < 2) {
                return (idx * 900 - 330)
            }
            return (idx * 900 - 330) * (1-ratio) + (2.5 * 900 - 300) * ratio
        },
    },
    watch: {
        time() {
            this.update_cameras()
        },
    },
}
</script>
