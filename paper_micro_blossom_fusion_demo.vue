<template>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :snapshot_idx="snapshot_idx_interpolated"
        :camera_scale="5"></Fusion3d>
</template>

<style></style>

<script>
import error_model from './common/error_model.vue'
import fusion_3d from './common/fusion_3d.vue'

const showing_indices = [7, 9, 11, 15, 17, 19, 22, 24, 26, 29, 30]
const duration = showing_indices.length

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
        }
    },
    components: {
        ErrorModel: error_model,
        Fusion3d: fusion_3d,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // load fusion 3d
        let response = await fetch('./common/micro_fusion_demo.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        const camera = this.$refs[`fusion3d`].camera
        // const orbit_control = this.$refs[`fusion3d${i}`].orbit_control
        camera.position.set(-838.819, 117.835, -531.505)
        camera.updateProjectionMatrix()
        console.log("main component mounted")
    },
    computed: {
        snapshot_idx_interpolated() {
            return showing_indices[Math.floor(this.time)]
        }
    },
    methods: {

    },
    watch: {

    },
}
</script>
