<template>
    <div :style="{ transform: `scale(${scale})` }" class="canvas">
        <h1>Hello at {{ time }}</h1>
    </div>
</template>

<style>
.canvas {
    background-color: red;
    position: absolute;
    transform-origin: top left;
    top: 0;
    left: 0;
    width: 1000px;
    height: 1000px;
}
</style>

<script>
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
    mounted() {
        console.log("hello")
    },
    computed: {
        
    },
    methods: {
        
    },
}
</script>
