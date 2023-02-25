<template>
    <Fusion3d ref="fusion3d" :fusion_data="decoding_graph_fusion_data" :camera_scale="3"></Fusion3d>
    <CompleteGraphBuilder ref="builder" :min_path_data="min_path_data" :time="interpolate" :show_edge_weight="interpolate <= 3" :show_region="interpolate <= 3 || interpolate >= 21" :scale="scale" :d="d"></CompleteGraphBuilder>
</template>

<style>

</style>

<script>
import fusion_3d from './common/fusion_3d.vue'
import complete_graph_builder from './common/complete_graph_builder.vue'

const duration = 50

function time_mapping(time) {
    const init_speed = 0.2
    const init_count = 3
    const init_time = init_count / init_speed
    if (time < init_time) {
        return time * init_speed
    }
    const middle_speed = 6
    const middle_count = 10
    const middle_time = 2 * middle_count / (middle_speed + init_speed)
    const a = (middle_speed - init_speed) / middle_time
    if (time < init_time + middle_time) {
        let bias = time - init_time
        return init_count + init_speed * bias + 0.5 * a * bias * bias
    }
    const end_count = 21 - init_count - middle_count
    const end_speed = middle_speed
    const end_time = end_count / end_speed
    if (time < init_time + middle_time + end_time) {
        let bias = time - init_time - middle_time
        return init_count + middle_count + bias * end_speed
    }
    if (time < 25) {
        return 21
    }
    if (time < 25 + 7) {
        return time - 25 + 21
    }
    return 21 + 7
}

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
            min_path_data: null,
        }
    },
    components: {
        Fusion3d: fusion_3d,
        CompleteGraphBuilder: complete_graph_builder,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // load fusion 3d
        let response = await fetch('./common/demo_aps2023_example_decoding_graph.json', { cache: 'no-cache', })
        this.decoding_graph_fusion_data = await response.json()
        // load min path data
        response = await fetch('./common/demo_aps2023_example_syndrome_graph_edges.json', { cache: 'no-cache', })
        const min_path_data = await response.json()
        console.log(min_path_data)
        this.min_path_data = min_path_data
        await Vue.nextTick()
        let builder = this.$refs.builder
        console.log(builder.count_edges)
        console.log("main component mounted")
    },
    computed: {
        interpolate() {
            return time_mapping(this.time)
        },
    },
    methods: {
        
    },
    watch: {
        
    },
}
</script>
