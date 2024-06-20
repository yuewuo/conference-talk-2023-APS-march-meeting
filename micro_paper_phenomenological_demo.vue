<template>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :camera_scale="5"></Fusion3d>
</template>

<style></style>

<script>
import fusion_3d from './common/fusion_3d.vue'

const duration = 20

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
        Fusion3d: fusion_3d,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // load fusion 3d
        let response = await fetch('./common/micro_paper_phenomenological_demo.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        const camera = this.$refs[`fusion3d`].camera
        camera.position.set(-838.819, 117.835, -531.505)
        camera.updateProjectionMatrix()
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
