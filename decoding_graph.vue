<template>
    <Fusion3d :scale="scale" :time="time" ref="fusion3d"></Fusion3d>
</template>

<style>

</style>

<script>
import fusion_3d from './common/fusion_3d.vue'

const duration = 10

export default {
    props: {
        "scale": { type: Number, default: 1, },
        "time": Number,
        "d": { type: Number, default: 5, },
    },
    data() {
        return {
            animated_errors: [],
            animated_syndrome: [],
        }
    },
    components: {
        Fusion3d: fusion_3d,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        
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
