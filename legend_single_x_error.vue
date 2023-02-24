<template>
    <ErrorModel :scale="scale" :time="time" :d="d" ref="error_model" :animated_errors="animated_errors" :show_x_stabilizer="false" :show_z_stabilizer="false" :show_data_qubits="false"
    :extra_data_qubits="animated_errors"></ErrorModel>
</template>

<style>

</style>

<script>
import error_model from './common/error_model.vue'

const duration = 5

export default {
    props: {
        "scale": { type: Number, default: 1, },
        "time": Number,
        "d": { type: Number, default: 5, },
    },
    emits: ["duration-is"],
    data() {
        return {
            animated_errors: [
                { start: 0, last: duration, animate: 0, i: -0.5, j: -0.5, text: 'X' }
            ],
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
