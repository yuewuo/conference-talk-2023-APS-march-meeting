<template>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :camera_scale="3" :edge_opacity="0.5"></Fusion3d>
    <ErrorModel :scale="scale" :time="time" :d="d" ref="error_model" :animated_errors="animated_errors" :animated_syndrome="animated_syndrome" :qubit_opacity="0.2" :show_error_chain="true" :show_x_stabilizer="false" :show_operator_z="true" :operator_opacity="0.2"></ErrorModel>
</template>

<style>

</style>

<script>
import error_model from './common/error_model.vue'
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
        ErrorModel: error_model,
        Fusion3d: fusion_3d,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // load fusion 3d
        let response = await fetch('./common/demo_aps2023_decoding_graph_static.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()

        // generate random errors
        const rng = new Math.seedrandom(666)
        const error_rounds = 10
        const p = 0.1
        for (let round=0; round < error_rounds; ++round) {
            let syndrome = {}
            for (let i=0; i<2*this.d; ++i) {
                for (let j=0; j<2*this.d; ++j) {
                    if (!(this.$refs.error_model.qubit_show(i, j) && this.$refs.error_model.qubit_is_data(i, j))) {
                        continue
                    }
                    if (rng() < p) {
                        // let err = ['X', 'Y', 'Z'][parseInt(rng() * 3) % 3]
                        let err = ['X', 'Z'][parseInt(rng() * 2) % 2]
                        if (err == 'X') {
                            this.animated_errors.push({
                                start: (round + 0.1) / error_rounds * duration,
                                last: 0.8 / error_rounds * duration,
                                animate: 0.3,
                                i, j, text: err,
                            })
                        }
                        if (err == "X" || err == "Y") {
                            for (let [di, dj] of [[1,0],[-1,0],[0,1],[0,-1]]) {
                                if (this.$refs.error_model.qubit_is_z_stab(i + di, j + dj) && !this.$refs.error_model.qubit_is_virtual(i + di, j + dj)) {
                                    const pos = `${i+di},${j+dj}`
                                    if (syndrome[pos] == null) { syndrome[pos] = 0 }
                                    syndrome[pos] += 1
                                }
                            }
                        }
                    }
                }
            }
            for (let pos in syndrome) {
                if (syndrome[pos] % 2 == 1) {
                    let [i, j] = pos.split(',')
                    this.animated_syndrome.push({
                        start: (round + 0.1) / error_rounds * duration,
                        last: 0.8 / error_rounds * duration,
                        animate: 0.3,
                        i: parseInt(i), j: parseInt(j),
                    })
                }
            }
        }
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
