<template>
    <ErrorModel :scale="scale" :time="time" :d="d" ref="error_model" :animated_errors="animated_errors" :show_virtual="false"
        :show_operator_x="show_operator_x" :show_operator_z="show_operator_z" :show_x_stabilizer="show_operator_x" :show_z_stabilizer="show_operator_z"></ErrorModel>
</template>

<style>

</style>

<script>
import error_model from './common/error_model.vue'

const duration = 1


const urlParams = new URLSearchParams(window.location.search)
const hide_x = urlParams.get("hide_x") != null
const hide_z = urlParams.get("hide_z") != null

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
            show_operator_x: !hide_x,
            show_operator_z: !hide_z,
        }
    },
    components: {
        ErrorModel: error_model,
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
