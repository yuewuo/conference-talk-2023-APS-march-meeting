<template>
    <div :style="{ transform: `scale(${scale})` }" class="canvas">
        <!-- stabilizer operator --><div v-for="(_i, i) in (2*d+1)">
            <div v-for="(_j, j) in (2*d+1)">
                <div v-if="!qubit_is_virtual(i, j) && !qubit_is_data(i, j) && (qubit_is_x_stab(i, j) ? show_operator_x : show_operator_z)"
                        class="stabilizer-operator" :style="{ 'top': pos(i) - 1000 * scaling + 'px', 'left': pos(j) - 1000 * scaling + 'px', 'opacity': operator_opacity }">
                    <div class="stabilizer-left-top" v-if="qubit_show(i-1, j) && qubit_show(i, j-1)"
                        :style="{ 'border-bottom': `${950 * scaling}px solid ${qubit_is_x_stab(i, j) ? 'rgb(193, 217, 185)' : '#86bbd8'}` }"></div>
                    <div class="stabilizer-right-top" v-if="qubit_show(i-1, j) && qubit_show(i, j+1)"
                        :style="{ 'border-bottom': `${950 * scaling}px solid ${qubit_is_x_stab(i, j) ? 'rgb(193, 217, 185)' : '#86bbd8'}` }"></div>
                    <div class="stabilizer-left-bottom" v-if="qubit_show(i+1, j) && qubit_show(i, j-1)"
                        :style="{ 'border-top': `${950 * scaling}px solid ${qubit_is_x_stab(i, j) ? 'rgb(193, 217, 185)' : '#86bbd8'}` }"></div>
                    <div class="stabilizer-right-bottom" v-if="qubit_show(i+1, j) && qubit_show(i, j+1)"
                        :style="{ 'border-top': `${950 * scaling}px solid ${qubit_is_x_stab(i, j) ? 'rgb(193, 217, 185)' : '#86bbd8'}` }"></div>
                    <!-- text -->
                    <div class="stabilizer-text stabilizer-text-top" v-if="qubit_show(i-1, j)"
                        :style="{ 'color': qubit_is_x_stab(i, j) ? '#97a169' : '#33658a' }">{{ qubit_is_x_stab(i, j) ? 'X' : 'Z' }}</div>
                    <div class="stabilizer-text stabilizer-text-bottom" v-if="qubit_show(i+1, j)"
                        :style="{ 'color': qubit_is_x_stab(i, j) ? '#97a169' : '#33658a' }">{{ qubit_is_x_stab(i, j) ? 'X' : 'Z' }}</div>
                    <div class="stabilizer-text stabilizer-text-left" v-if="qubit_show(i, j-1)"
                        :style="{ 'color': qubit_is_x_stab(i, j) ? '#97a169' : '#33658a' }">{{ qubit_is_x_stab(i, j) ? 'X' : 'Z' }}</div>
                    <div class="stabilizer-text stabilizer-text-right" v-if="qubit_show(i, j+1)"
                        :style="{ 'color': qubit_is_x_stab(i, j) ? '#97a169' : '#33658a' }">{{ qubit_is_x_stab(i, j) ? 'X' : 'Z' }}</div>
                </div>
            </div>
        </div>
        <!-- error chains --><div v-for="error of animated_errors">
            <div v-if="show_error_chain && error_current_show(error)" class="error-chain" :style="{ 'opacity': error_opacity(error), 'top': pos(error.i) - 1000 * scaling + 'px', 'left': pos(error.j) - 1000 * scaling + 'px' }">
                <div v-if="error_chain_has_vertical(error)" class="vertical-error-chain"></div>
                <div v-if="error_chain_has_horizontal(error)" class="horizontal-error-chain"></div>
            </div>
        </div>
        <!-- qubits --><div v-for="(_i, i) in (2*d+1)">
            <div v-for="(_j, j) in (2*d+1)">
                <div v-if="qubit_show(i, j)" class="qubit" :style="{ 'background-color': qubit_color(i, j), 'opacity': qubit_opacity, 'top': pos(i) - qubit_radius + 'px', 'left': pos(j) - qubit_radius + 'px', }"></div>
            </div>
        </div>
        <!-- extra data qubits --><div v-for="qubit of extra_data_qubits">
            <div class="qubit" :style="{ 'background-color': qubit_color(1, 1), 'top': pos(qubit.i) - qubit_radius + 'px', 'left': pos(qubit.j) - qubit_radius + 'px', }"></div>
        </div>
        <!-- errors --><div v-for="error of animated_errors">
            <div v-if="error_current_show(error)" class="error" :style="{ 'top': pos(error.i) - error_radius + 'px', 'left': pos(error.j) - error_radius + 'px', 'opacity': error_opacity(error), }">
                {{ error.text }}
            </div>
            <div v-if="error_current_show(error)" class="error-circle" :style="{ 'border': `dotted 10px ${error_border_color(error)}`, 'top': pos(error.i) - error_radius - 5 + 'px', 'left': pos(error.j) - error_radius - 5 + 'px'
                , 'opacity': error_opacity(error), 'transform': `rotate(${parseInt(error_rotate_speed * (time - error.start))}deg)` }">
            </div>
        </div>
        <!-- syndrome --><div v-for="defect of animated_syndrome">
            <div v-if="error_current_show(defect)" class="defect" :style="{ 'opacity': error_opacity(defect), 'top': pos(defect.i) - qubit_radius + 'px', 'left': pos(defect.j) - qubit_radius + 'px', }">
                
            </div>
        </div>
    </div>
</template>

<style scoped>
.canvas {
    /* background-color: lightblue; */
    position: absolute;
    transform-origin: top left;
    top: 0;
    left: 0;
    width: 1000px;
    height: 1000px;
}
.qubit {
    position: absolute;
    width: v-bind(2 * qubit_radius + 'px');
    height: v-bind(2 * qubit_radius + 'px');
    border-radius: v-bind(2 * qubit_radius + 'px');
}
.error {
    /* background-color: red; */
    position: absolute;
    width: v-bind(2 * error_radius + 'px');
    height: v-bind(2 * error_radius + 'px');
    border-radius: v-bind(2 * error_radius + 'px');
    color: red;
    -webkit-text-stroke: 2px white;
    line-height: v-bind(2 * error_radius + 'px');
    font-size:  v-bind(1.5 * error_radius + 'px');
    font-family: Sans-Serif;
    text-align: center;
    font-weight: bold;
}
.error-circle {
    position: absolute;
    width: v-bind(2 * error_radius - 10 + 'px');
    height: v-bind(2 * error_radius - 10 + 'px');
    border-radius: v-bind(2 * error_radius + 'px');
}
.defect {
    position: absolute;
    width: v-bind(2 * qubit_radius + 'px');
    height: v-bind(2 * qubit_radius + 'px');
    border-radius: v-bind(2 * qubit_radius + 'px');
    background-color: red;
}
.error-chain {
    position: absolute;
    width: v-bind(2000 * scaling + 'px');
    height: v-bind(2000 * scaling + 'px');
    /* background-color: blue; */
}
.vertical-error-chain {
    position: relative;
    width: v-bind(200 * scaling + 'px');
    height: v-bind(2000 * scaling + 'px');
    left: v-bind(900 * scaling + 'px');
    border-radius: v-bind(200 * scaling + 'px');
    background-color: red;
    opacity: 0.2;
}
.horizontal-error-chain {
    position: relative;
    width: v-bind(2000 * scaling + 'px');
    top: v-bind(900 * scaling + 'px');
    height: v-bind(200 * scaling + 'px');
    border-radius: v-bind(200 * scaling + 'px');
    background-color: red;
    opacity: 0.2;
}
.stabilizer-operator {
    position: absolute;
    width: v-bind(2000 * scaling + 'px');
    height: v-bind(2000 * scaling + 'px');
}
.stabilizer-left-top {
    position: absolute;
    top: v-bind(50 * scaling + 'px');
    left: v-bind(50 * scaling + 'px');
    border-left: v-bind(950 * scaling + 'px') solid transparent;
    border-right: v-bind(0 * scaling + 'px') solid transparent;
    width: 0;
    height: 0;
}
.stabilizer-right-top {
    position: absolute;
    top: v-bind(50 * scaling + 'px');
    left: v-bind(990 * scaling + 'px');
    border-left: v-bind(0 * scaling + 'px') solid transparent;
    border-right: v-bind(950 * scaling + 'px') solid transparent;
    width: 0;
    height: 0;
}
.stabilizer-left-bottom {
    position: absolute;
    top: v-bind(990 * scaling + 'px');
    left: v-bind(50 * scaling + 'px');
    border-left: v-bind(950 * scaling + 'px') solid transparent;
    border-right: v-bind(0 * scaling + 'px') solid transparent;
    width: 0;
    height: 0;
}
.stabilizer-right-bottom {
    position: absolute;
    top: v-bind(990 * scaling + 'px');
    left: v-bind(990 * scaling + 'px');
    border-left: v-bind(0 * scaling + 'px') solid transparent;
    border-right: v-bind(950 * scaling + 'px') solid transparent;
    width: 0;
    height: 0;
}
.stabilizer-text {
    position: absolute;
    font-size: v-bind(300 * scaling + 'px');
    font-family: Sans-Serif;
}
.stabilizer-text-top {
    top: v-bind(250 * scaling + 'px');
    left: v-bind(900 * scaling + 'px');
}
.stabilizer-text-bottom {
    top: v-bind(1450 * scaling + 'px');
    left: v-bind(900 * scaling + 'px');
}
.stabilizer-text-left {
    top: v-bind(850 * scaling + 'px');
    left: v-bind(300 * scaling + 'px');
}
.stabilizer-text-right {
    top: v-bind(850 * scaling + 'px');
    left: v-bind(1500 * scaling + 'px');
}
</style>

<script>
export default {
    props: {
        "scale": { type: Number, default: 1, },
        "d": { type: Number, default: 3, },
        "time": Number,
        "animated_errors": { type: Array,
            default: [],
            // default: [ { start:0.5, last: 0.8, animate: 0.1, i: 2, j: 2, text: 'X' } ],
        },
        "extra_data_qubits":{ type: Array,
            default: [],
            // default: [ { i: 2, j: 2 } ],
        },
        "show_virtual": { type: Boolean, default: true, },
        "error_rotate_speed": { type: Number, default: 200, },
        "animated_syndrome": { type: Array,
            default: [],
            // default: [ { start:0.5, last: 0.8, animate: 0.1, i: 2, j: 3 } ],
        },
        "show_x_stabilizer": { type: Boolean, default: true, },
        "show_z_stabilizer": { type: Boolean, default: true, },
        "show_data_qubits": { type: Boolean, default: true, },
        "qubit_opacity": { type: Number, default: 1, },
        "show_error_chain": { type: Boolean, default: false, },
        "show_operator_x": { type: Boolean, default: false, },
        "show_operator_z": { type: Boolean, default: false, },
        "operator_opacity": { type: Number, default: 1, },
    },
    data() {
        return {

        }
    },
    mounted() {
        console.log("error model component mounted")
    },
    computed: {
        scaling() {
            return 1 / (2 * this.d + 2)
        },
        qubit_radius() {
            return 250 * this.scaling
        },
        error_radius() {
            return this.qubit_radius * 1.5
        },
    },
    methods: {
        qubit_color(i, j) {
            if (this.qubit_is_virtual(i, j)) {
                return 'yellow'
            }
            if (this.qubit_is_data(i, j)) {
                return 'black'
            }
            if (this.qubit_is_x_stab(i, j)) {
                return '#97a169'
            }
            if (this.qubit_is_z_stab(i, j)) {
                return '#33658a'
            }
            return 'orange'
        },
        pos(i) {
            return 1000 * (0.5 + (i - this.d) * this.scaling)
        },
        qubit_show(i, j) {
            if (i == 0 || i == 2 * this.d) {  // X virtual
                return this.show_x_stabilizer && this.show_virtual && j % 2 == 1
            }
            if (j == 0 || j == 2 * this.d) {  // Z virtual
                return this.show_z_stabilizer && this.show_virtual && i % 2 == 1
            }
            if (this.qubit_is_x_stab(i, j)) {
                return this.show_x_stabilizer
            }
            if (this.qubit_is_z_stab(i, j)) {
                return this.show_z_stabilizer
            }
            return this.show_data_qubits
        },
        qubit_is_virtual(i, j) {
            if (i == 0 || i == 2 * this.d) {
                return j % 2 == 1
            }
            if (j == 0 || j == 2 * this.d) {
                return i % 2 == 1
            }
            return false
        },
        qubit_is_data(i, j) {
            return (i + j) % 2 == 0
        },
        qubit_is_x_stab(i, j) {
            return !this.qubit_is_data(i, j) && i % 2 == 0
        },
        qubit_is_z_stab(i, j) {
            return !this.qubit_is_data(i, j) && i % 2 == 1
        },
        error_current_show(error) {
            return this.time >= error.start && this.time <= error.start + error.last + error.animate
        },
        error_opacity(error) {
            if (!this.error_current_show(error)) return 0
            let ratio = null
            if (this.time - error.start <= error.animate) {
                ratio = (this.time - error.start) / error.animate
            }
            if (this.time >= error.start + error.last) {
                ratio = 1 - (this.time - error.start - error.last) / error.animate
            }
            if (ratio != null) {
                return ratio
            }
            return 1
        },
        error_border_color(error) {
            if (error.text == "X") {
                return "#97a169"
            }
            if (error.text == "Z") {
                return "#33658a"
            }
            return "red"
        },
        error_chain_has_vertical(error) {
            if (this.qubit_is_x_stab(error.i + 1, error.j) && (error.text == "Z" || error.text == "Y")) {
                return true
            }
            if (this.qubit_is_z_stab(error.i + 1, error.j) && (error.text == "X" || error.text == "Y")) {
                return true
            }
            return false
        },
        error_chain_has_horizontal(error) {
            if (this.qubit_is_x_stab(error.i, error.j + 1) && (error.text == "Z" || error.text == "Y")) {
                return true
            }
            if (this.qubit_is_z_stab(error.i, error.j + 1) && (error.text == "X" || error.text == "Y")) {
                return true
            }
            return false
        },
    },
    watch: {
        animated_errors() {
            console.log(this.animated_errors)
        },
    },
}
</script>
