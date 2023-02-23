<template>
    <div :style="{ transform: `scale(${scale})` }" class="canvas">
        <!-- tight edges --><div v-for="edge of tight_edges">
            <div class="tight-edge" :style="{ 'top': pos(edge.i1) - edge_width / 2 * scaling + 'px', 'left': pos(edge.j1) + 'px'
                , 'width': edge_length(edge) + 'px', 'transform': `rotate(${edge_rotation(edge)}deg)`
                , 'transform-origin': `0 ${edge_width / 2 * scaling}px`, 'opacity': edge_opacity(edge) }" v-if="edge_current_show"></div>
        </div>
    </div>
</template>

<style scoped>
.canvas {
    /* background-color: lightblue; */
    position: absolute;
    transform-origin: top left;
    top: v-bind(top + 'px');
    left: v-bind(left + 'px');
    width: 1000px;
    height: 1000px;
}
.tight-edge {
    position: absolute;
    height: 0;
    border: none;
    border-top: v-bind(edge_width * scaling + 'px') double blue;
}
</style>

<script>
export default {
    props: {
        "top": { type: Number, default: 0, },
        "left": { type: Number, default: 0, },
        "scale": { type: Number, default: 1, },
        "d": { type: Number, default: 3, },
        "time": Number,
        "tight_edges": { type: Array,
            default: [],
            // default: [ { i1: 3, j1: 0, i2: 3, j2: 2 } ],
        },
        "edge_width": { type: Number, default: 300, },
    },
    data() {
        return {

        }
    },
    mounted() {
        console.log("example both grow component mounted")
    },
    computed: {
        scaling() {
            return 1 / (2 * this.d + 2)
        },
    },
    methods: {
        pos(i) {
            return 1000 * (0.5 + (i - this.d) * this.scaling)
        },
        edge_length(edge) {
            const di = Math.abs(edge.i1 - edge.i2)
            const dj = Math.abs(edge.j1 - edge.j2)
            const length = Math.sqrt(di * di + dj * dj)
            return length * this.scaling * 1000
        },
        edge_rotation(edge) {
            const angle = Math.atan2(edge.i2 - edge.i1, edge.j2 - edge.j1)
            return angle / Math.PI * 180
        },
        edge_current_show(edge) {
            if (edge.start == null) return true
            return this.time >= edge.start && this.time <= edge.start + edge.last + edge.animate
        },
        edge_opacity(edge) {
            if (!this.edge_current_show(edge)) return 0
            let ratio = null
            if (this.time - edge.start <= edge.animate) {
                ratio = (this.time - edge.start) / edge.animate
            }
            if (this.time >= edge.start + edge.last) {
                ratio = 1 - (this.time - edge.start - edge.last) / edge.animate
            }
            if (ratio != null) {
                return ratio
            }
            return 1
        },
    },
    watch: {
        
    },
}
</script>
