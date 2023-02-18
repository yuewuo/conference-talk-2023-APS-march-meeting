<template>
    <ErrorModel :scale="scale" :time="time"></ErrorModel>
</template>

<style>

</style>

<script>
import error_model from './common/error_model.vue'

export default {
    props: {
        "scale": {
            type: Number,
            default: 1,
        },
        "time": Number,
    },
    data() {
        return {
            
        }
    },
    components: {
        ErrorModel: error_model,
    },
    mounted() {
        console.log("hello world")
    },
    computed: {
        
    },
    methods: {
        
    },
}
</script>
