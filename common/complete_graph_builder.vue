<template>
    <div class="grow-div" :style="{ top: bias_top + 'px', left: bias_left + 'px', width: 2000 - 2 * bias_left + 'px', height: 2000 - 2 * bias_top + 'px' }" v-if="min_path_data != null">
        <div class="grow-region" v-if="radius > 0 && show_region" :style="{ width: `${2000 * radius * scaling * Math.sqrt(2)}px`, height: `${2000 * radius * scaling * Math.sqrt(2)}px`, left: `${pos(rj) - 1000 * radius * scaling * Math.sqrt(2) - bias_left}px`, top: `${pos(ri) - 1000 * radius * scaling * Math.sqrt(2) - bias_top}px`, opacity: region_opacity }"></div>
    </div>
    <div class="canvas">
        <div class="vertex" :style="{ opacity: vertex_opacity, top: `${pos(si) - vertex_radius - 20}px`, left: `${pos(sj) - vertex_radius - 20}px`, 'transform': `rotate(${parseInt(200 * time)}deg)` }"></div>
        <div class="vertex" :style="{ opacity: vertex_opacity, top: `${pos(ei) - vertex_radius - 20}px`, left: `${pos(ej) - vertex_radius - 20}px`, 'transform': `rotate(${parseInt(200 * time)}deg)` }"></div>
    </div>
    <canvas ref="canvas" class="canvas" width="2000" height="2000"></canvas>
    <div v-if="show_edge_weight" class="edge-weight" :style="{ opacity: weight_opacity }"><i>w<sub>e</sub></i> = {{ edge_weight }}</div>
</template>

<style scoped>
.canvas {
    /* background-color: lightblue; */
    position: absolute;
    transform-origin: top left;
    top: 0;
    left: 0;
    width: 2000px;
    height: 2000px;
}
.grow-div {
    position: absolute;
    transform-origin: top left;
    top: 0;
    left: 0;
    overflow: hidden;
}
.grow-region {
    z-index: -1000;
    background-color: #82A284;
    position: relative;
    transform-origin: center;
    transform: rotate(45deg);
}
.edge-weight {
    height: 200px;
    width: 2000px;
    position: absolute;
    left: 0;
    top: 50px;
    line-height: 200px;
    font-size: 120px;
    text-align: center;
    font-weight: bold;
}
.vertex {
    position: absolute;
    width: v-bind(2 * vertex_radius + 'px');
    height: v-bind(2 * vertex_radius + 'px');
    border: 20px dotted red;
    border-radius: v-bind(2 * vertex_radius + 'px');
}
</style>

<script>
export default {
    props: {
        "scale": { type: Number, default: 1, },
        "d": { type: Number, default: 3, },
        "time": Number,
        "min_path_data": { type: Object },
        // styles
        "line_width": { type: Number, default: 30, },
        "line_min_path_style": { type: String, default: "rgb(255, 0, 255)", },
        "line_exist_path_style": { type: String, default: "rgb(200, 200, 200)", },
        "line_border": { type: Number, default: 10, },
        "line_border_style": { type: String, default: "rgb(0, 0, 0)", },
        "show_edge_weight": { type: Boolean, default: true, },
        "show_region": { type: Boolean, default: true, },
        "vertex_radius": { type: Number, default: 70, },
    },
    data() {
        return {
            sequence: [],
            // region
            ri: 0,
            rj: 0,
            radius: 0,
            region_opacity: 0.1,
            edge_weight: 0,
            weight_opacity: 0,
            vertex_opacity: 0,
            si: 0,
            sj: 0,
            ei: 0,
            ej: 0,
        }
    },
    mounted() {
        console.log("complete graph builder component mounted")
    },
    computed: {
        scaling() {
            return 1 / (2 * this.d + 2)
        },
        defect_vertex_num() {
            return this.min_path_data.defect_vertices.length
        },
        count_edges() {
            return this.defect_vertex_num * (this.defect_vertex_num - 1) / 2
        },
        bias_top() {
            return this.pos(1)
        },
        bias_left() {
            return this.pos(0)
        },
    },
    methods: {
        pos(i) {
            return 2000 * (0.5 + (i - this.d) * this.scaling)
        },
        color_rgb(color) {
            const seq = color.split('(')
            if (seq.length == 2) {
                const colors = seq[1].split(')')[0].split(',')
                console.assert(colors.length == 3)
                return [parseInt(colors[0]), parseInt(colors[1]), parseInt(colors[2])]
            }
        },
        interpolate_color(color1, color2, ratio) {
            if (ratio < 0) ratio = 0
            if (ratio > 1) ratio = 1
            const c1 = this.color_rgb(color1)
            const c2 = this.color_rgb(color2)
            return "rgb(" + 
                `${parseInt(c1[0] * (1-ratio) + c2[0] * ratio)}, ` + 
                `${parseInt(c1[1] * (1-ratio) + c2[1] * ratio)}, ` + 
                `${parseInt(c1[2] * (1-ratio) + c2[2] * ratio)})`
        },
        draw_line(ctx, path, line_style=null) {  // e.g. path = [[1,0], [3,2], [1,4]]
            ctx.save()
            let line_width = this.line_width
            let line_border = this.line_border
            ctx.lineJoin = "round"
            ctx.lineCap = "round"
            if (line_border != 0) {
                ctx.lineWidth = line_width + line_border * 2
                ctx.strokeStyle = this.line_border_style
                ctx.beginPath()
                ctx.moveTo(this.pos(path[0][1]), this.pos(path[0][0]))
                for (let i=1; i<path.length; ++i) {
                    ctx.lineTo(this.pos(path[i][1]), this.pos(path[i][0]))
                }
                ctx.stroke()
            }
            ctx.lineWidth = line_width
            if (line_style == null) line_style = this.line_exist_path_style
            ctx.strokeStyle = line_style
            ctx.beginPath()
            ctx.moveTo(this.pos(path[0][1]), this.pos(path[0][0]))
            for (let i=1; i<path.length; ++i) {
                ctx.lineTo(this.pos(path[i][1]), this.pos(path[i][0]))
            }
            ctx.stroke()
            ctx.restore()
        },
        draw_min_path_interpolated(ctx, min_path, interpolate=0) {  // interpolate: [0, 1]
            if (interpolate < 0) interpolate = 0
            if (interpolate > 1) interpolate = 1
            if (interpolate == 1) {
                let [si, sj] = this.min_path_data.indices[min_path[0]]
                let [ei, ej] = this.min_path_data.indices[min_path[min_path.length-1]]
                this.draw_line(ctx, [[si,sj], [ei,ej]])
                return
            }
            let points_per_segment = 20
            let origin_points = []
            for (let i=0; i<min_path.length; ++i) {
                let [si, sj] = this.min_path_data.indices[min_path[i]]
                origin_points.push([si, sj])
                if (i+1 < min_path.length) {
                    let [ei, ej] = this.min_path_data.indices[min_path[i+1]]
                    for (let j=1; j<points_per_segment; ++j) {
                        let ratio = j / points_per_segment
                        origin_points.push([
                            si * (1-ratio) + ei * ratio,
                            sj * (1-ratio) + ej * ratio,
                        ])
                    }
                }
            }
            // calculate intersect point
            let [si, sj] = this.min_path_data.indices[min_path[0]]
            let [ei, ej] = this.min_path_data.indices[min_path[min_path.length-1]]
            let interpolated_points = []
            for (let [i, j] of origin_points) {
                const ca = ei - si
                const db = ej - sj
                let xi = (
                    ca * db * j + ca * ca * i + si * db * db - sj * ca * db
                ) / ( ca * ca + db * db )
                let xj = (
                    db * db * j + db * ca * i - si * ca * db - sj * db * db
                ) / ( ca * ca + db * db ) + sj
                const dis = Math.pow(Math.pow(xi - i, 2) + Math.pow(xj - j, 2), 0.5)
                let ratio = 1 - Math.pow(1 - interpolate, 1 + 0.5 * dis)
                interpolated_points.push([
                    i * (1-ratio) + xi * ratio,
                    j * (1-ratio) + xj * ratio,
                ])
            }
            let line_style = this.interpolate_color(this.line_min_path_style, this.line_exist_path_style, interpolate)
            this.draw_line(ctx, interpolated_points, line_style=line_style)
        },
        draw() {
            if (this.min_path_data == null) return
            const canvas = this.$refs.canvas
            const ctx = canvas.getContext("2d")
            // ctx.globalCompositeOperation = 'destination-atop'
            ctx.clearRect(0, 0, canvas.width, canvas.height)
            let static_seq_length = this.sequence.length
            let active_seq_idx = null
            let interpolate = this.time - Math.floor(this.time)
            if (this.time < this.sequence.length) {
                active_seq_idx = Math.floor(this.time)
                static_seq_length = active_seq_idx
            }
            // first draw existing edges
            for (let i=0; i<static_seq_length; ++i) {
                const [sv, ev] = this.sequence[i]
                const path = this.min_path_data.map[sv].paths[ev]
                this.draw_min_path_interpolated(ctx, path, 1)
            }
            // next draw new edge
            this.radius = 0
            this.region_opacity = 0.7
            this.weight_opacity = 0
            this.vertex_opacity = 0
            // configuration
            const explore_ratio = 0.5
            const show_ratio = 0.3
            const transform_ratio = 1 - explore_ratio - show_ratio
            const animate = 0.1
            if (active_seq_idx != null) {
                const [sv, ev] = this.sequence[active_seq_idx]
                const [si, sj] = this.min_path_data.indices[sv]
                const [ei, ej] = this.min_path_data.indices[ev]
                this.si = si
                this.sj = sj
                this.ei = ei
                this.ej = ej
                const distance = Math.abs(si - ei) + Math.abs(sj - ej)
                this.ri = si
                this.rj = sj
                const path = this.min_path_data.map[sv].paths[ev]
                this.edge_weight = path.length - 1
                if (interpolate < animate) {
                    this.vertex_opacity = interpolate / animate
                } else if (interpolate < 1 - animate) {
                    this.vertex_opacity = 1
                } else {
                    this.vertex_opacity = (1 - interpolate) / animate
                }
                if (interpolate < explore_ratio) {
                    this.radius = this.smooth_animate(interpolate / explore_ratio) * distance
                } else if (interpolate < explore_ratio + animate) {
                    this.radius = distance
                    this.region_opacity = 0.7 * (1 - this.smooth_animate((interpolate - explore_ratio) / animate))
                }
                if (interpolate >= explore_ratio && interpolate < explore_ratio + show_ratio) {
                    this.draw_min_path_interpolated(ctx, path, 0)
                    if (interpolate < explore_ratio + animate) {
                        this.weight_opacity = (interpolate - explore_ratio) / animate
                    } else {
                        this.weight_opacity = 1
                    }
                }
                if (interpolate >= explore_ratio + show_ratio) {
                    let ratio = (interpolate - explore_ratio - show_ratio) / transform_ratio
                    this.draw_min_path_interpolated(ctx, path, ratio)
                    if (interpolate < 1 - animate) {
                        this.weight_opacity = 1
                    } else {
                        this.weight_opacity = (1 - interpolate) / animate
                    }
                }
            }
            if (this.time >= this.sequence.length) {
                let existing_vertex_index = Math.floor(this.time - this.sequence.length)
                if (existing_vertex_index > 7) existing_vertex_index = 7
                for (let i=0; i<existing_vertex_index; ++i) {
                    const defect_vertex = this.min_path_data.defect_vertices[i]
                    const path = this.min_path_data.map[defect_vertex].boundary
                    this.draw_min_path_interpolated(ctx, path, 1)
                }
            }
            if (this.time >= this.sequence.length && this.time < this.sequence.length + this.min_path_data.defect_vertices.length) {
                const defect_vertex_index = Math.floor(this.time - this.sequence.length)
                const defect_vertex = this.min_path_data.defect_vertices[defect_vertex_index]
                const path = this.min_path_data.map[defect_vertex].boundary
                const [si, sj] = this.min_path_data.indices[path[0]]
                const [ei, ej] = this.min_path_data.indices[path[path.length-1]]
                const distance = Math.abs(si - ei) + Math.abs(sj - ej)
                this.si = si
                this.sj = sj
                this.ei = -2
                this.ej = -2
                this.ri = si
                this.rj = sj
                if (interpolate < animate) {
                    this.vertex_opacity = interpolate / animate
                } else if (interpolate < 1 - animate) {
                    this.vertex_opacity = 1
                } else {
                    this.vertex_opacity = (1 - interpolate) / animate
                }
                if (interpolate < explore_ratio) {
                    this.radius = this.smooth_animate(interpolate / explore_ratio) * distance
                } else if (interpolate < explore_ratio + animate) {
                    this.radius = distance
                    this.region_opacity = 0.7 * (1 - this.smooth_animate((interpolate - explore_ratio) / animate))
                }
                if (interpolate >= explore_ratio && interpolate < explore_ratio + show_ratio) {
                    this.draw_min_path_interpolated(ctx, path, 0)
                }
                if (interpolate >= explore_ratio + show_ratio) {
                    let ratio = (interpolate - explore_ratio - show_ratio) / transform_ratio
                    this.draw_min_path_interpolated(ctx, path, ratio)
                }
            }
            // this.draw_line(ctx, [[1,0], [3,2], [1,4]])
            // this.draw_min_path_interpolated(ctx, [14, 8, 9, 3], this.smooth_animate(this.time * 2))
        },
        smooth_animate(ratio) {
            if (ratio < 0) ratio = 0
            if (ratio > 1) ratio = 1
            if (ratio < 0.5) {
                return 2 * ratio * ratio
            }
            return 1 - 2 * (1 - ratio) * (1 - ratio)
        },
        build_sequence() {
            let sequence = []
            for (let i=0; i<this.min_path_data.defect_vertices.length; ++i) {
                for (let j=i+1; j<this.min_path_data.defect_vertices.length; ++j) {
                    sequence.push([
                        this.min_path_data.defect_vertices[i],
                        this.min_path_data.defect_vertices[j],
                    ])
                }
            }
            this.sequence = sequence
        },
    },
    watch: {
        min_path_data() {
            if (this.min_path_data != null) {
                this.build_sequence()
                this.draw()
            }
        },
        time() {
            this.draw()
        },
    },
}
</script>
