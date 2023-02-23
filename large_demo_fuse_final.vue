<template>
    <!-- <div class="screen"></div>
    <div class="titles"></div> -->
    <Fusion3d ref="fusion3d1" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :snapshot_idx="49" :width="1800" :height="2160" :left="left(0)"></Fusion3d>
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
        zoom() {
            let time = this.time
            let middle_zoom = 0.1
            if (time < animation) {
                let ratio = time / animation
                return middle_zoom + (0.7 - middle_zoom) * Math.pow(ratio - 0.5, 2) * 4
            }
            return 0.7
        },
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
            const camera = this.$refs[`fusion3d1`].camera
            const orbit_control = this.$refs[`fusion3d1`].orbit_control
            camera.zoom = this.zoom
            let ratio = this.time_ratio()
            // -29.07083805498964, y: 999.2607827496196, z: 25.155008117675557
            camera.position.set(180 * (1-ratio) - 29 * ratio, 60 * (1-ratio) + 999 * ratio, 1000 * (1-ratio) + 25 * ratio)
            camera.updateProjectionMatrix()
            orbit_control.target.set(0, 0, 0 )
        },
        smooth_animate(ratio) {
            if (ratio < 0) ratio = 0
            if (ratio > 1) ratio = 1
            if (ratio < 0.5) {
                return 2 * ratio * ratio
            }
            return 1 - 2 * (1 - ratio) * (1 - ratio)
        },
        left(idx) {
            return (2.5 * 900 - 300)
        },
    },
    watch: {
        time() {
            this.update_cameras()
        },
    },
}
</script>
