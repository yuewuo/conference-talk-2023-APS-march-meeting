<template>
    <div class="canvas" ref="canvas_div">
        
    </div>
</template>

<style>
.canvas {
    /* background-color: lightblue; */
    position: absolute;
    transform-origin: top left;
    top: 0;
    left: v-bind(left + 'px');
    width: v-bind(width + 'px');
    height: v-bind(height + 'px');
}
</style>

<script async>

// commonly used vectors
const zero_vector = new THREE.Vector3( 0, 0, 0 )
const unit_up_vector = new THREE.Vector3( 0, 1, 0 )

// create common geometries
const segment = 128
const vertex_radius = 0.15
const vertex_geometry = new THREE.SphereGeometry( vertex_radius, segment, segment )
const edge_radius = 0.03
const edge_geometry = new THREE.CylinderGeometry( edge_radius, edge_radius, 1, segment, 1, true )
edge_geometry.translate(0, 0.5, 0)

// create common materials
export const defect_vertex_material = new THREE.MeshStandardMaterial({
    color: 0xff0000,
    opacity: 1,
    transparent: true,
    side: THREE.FrontSide,
})
export const disabled_mirror_vertex_material = new THREE.MeshStandardMaterial({
    color: 0x1e81b0,
    opacity: 1,
    transparent: true,
    side: THREE.FrontSide,
})
export const real_vertex_material = new THREE.MeshStandardMaterial({
    color: 0xffffff,
    opacity: 0.1,
    transparent: true,
    side: THREE.FrontSide,
})
export const virtual_vertex_material = new THREE.MeshStandardMaterial({
    color: 0xffff00,
    opacity: 0.5,
    transparent: true,
    side: THREE.FrontSide,
})
export const defect_vertex_outline_material = new THREE.MeshStandardMaterial({
    color: 0x000000,
    opacity: 1,
    transparent: true,
    side: THREE.BackSide,
})
export const real_vertex_outline_material = new THREE.MeshStandardMaterial({
    color: 0x000000,
    opacity: 1,
    transparent: true,
    side: THREE.BackSide,
})
export const virtual_vertex_outline_material = new THREE.MeshStandardMaterial({
    color: 0x000000,
    opacity: 1,
    transparent: true,
    side: THREE.BackSide,
})
export const edge_material = new THREE.MeshStandardMaterial({
    color: 0x000000,
    opacity: 0.1,
    transparent: true,
    side: THREE.FrontSide,
})
export const grown_edge_material = new THREE.MeshStandardMaterial({
    color: 0xff0000,
    opacity: 1,
    transparent: true,
    side: THREE.FrontSide,
})
export const subgraph_edge_material = new THREE.MeshStandardMaterial({
    color: 0x0000ff,
    opacity: 1,
    transparent: true,
    side: THREE.FrontSide,
})
export const hover_material = new THREE.MeshStandardMaterial({  // when mouse is on this object (vertex or edge)
    color: 0x6FDFDF,
    side: THREE.DoubleSide,
})
export const selected_material = new THREE.MeshStandardMaterial({  // when mouse is on this object (vertex or edge)
    color: 0x4B7BE5,
    side: THREE.DoubleSide,
})
export const blossom_convex_material = new THREE.MeshStandardMaterial({
    color: 0x82A284,
    opacity: 0.7,
    transparent: true,
    side: THREE.BackSide,
})
export const blossom_convex_material_2d = blossom_convex_material.clone()
blossom_convex_material_2d.side = THREE.DoubleSide

const outline_ratio = 1.2
const vertex_outline_radius = vertex_radius * outline_ratio

// helper functions
export function compute_vector3(data_position) {
    let vector = new THREE.Vector3( 0, 0, 0 )
    load_position(vector, data_position)
    return vector
}
export function load_position(mesh_position, data_position) {
    mesh_position.z = data_position.i
    mesh_position.x = data_position.j
    mesh_position.y = data_position.t
}

/// translate to a format that is easy to plot (gracefully handle the overgrown edges)
export function translate_edge(left_grown, right_grown, weight) {
    console.assert(left_grown >= 0 && right_grown >= 0, "grown should be non-negative")
    if (left_grown + right_grown <= weight) {
        return [left_grown, right_grown]
    } else {
        const middle = (left_grown + weight - right_grown) / 2
        if (middle < 0) {
            return [0, weight]
        }
        if (middle > weight) {
            return [weight, 0]
        }
        return [middle, weight - middle]
    }
}


export default {
    props: {
        "left": { type: Number, default: 0, },
        "width": { type: Number, default: 2000, },
        "height": { type: Number, default: 2000, },
        "camera_scale": { type: Number, default: 6, },
        "fusion_data": { type: Object,
            default: fusion_data_example,
        },
        "snapshot_idx": { type: Number, default: 0, },  // can be any fractional number, if so, the data is interpolated
        "edge_opacity": { type: Number, default: edge_material.opacity },
    },
    data() {
        return {

        }
    },
    async mounted() {
        // update properties
        edge_material.opacity = this.edge_opacity
        // create scene
        const scene = new THREE.Scene()
        scene.background = new THREE.Color( 0xffffff )  // for better image output
        scene.add( new THREE.AmbientLight( 0xffffff ) )
        const aspect_ratio = this.width / this.height
        const camera_scale = this.camera_scale
        const camera = new THREE.OrthographicCamera( - aspect_ratio * camera_scale, aspect_ratio * camera_scale, camera_scale, -camera_scale, 0.1, 100000 )
        camera.left = - aspect_ratio * camera_scale
        camera.right = aspect_ratio * camera_scale
        camera.position.x = 0
        camera.position.y = 1000
        camera.position.z = 0
        camera.lookAt(0, 0, 0)
        camera.updateProjectionMatrix()
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
        renderer.setSize( this.width, this.height, false )
        this.$refs.canvas_div.appendChild( renderer.domElement )
        const canvas = renderer.domElement
        canvas.width = this.width
        canvas.height = this.height
        canvas.style.width = `${this.width}px`
        canvas.style.height = `${this.height}px`
        // orbit control
        const orbit_control = new OrbitControls( camera, renderer.domElement )
        orbit_control.enable = true
        // start animation
        function animate() {
            requestAnimationFrame( animate )
            orbit_control.update()
            renderer.render( scene, camera )
        }
        animate()
        // meshes that can be reused across different snapshots
        this.variables = {
            scene, orbit_control,
            vertex_meshes: [],
            vertex_outline_meshes: [],
            vertex_caches: [],  // store some information that can be useful
            left_edge_meshes: [],
            right_edge_meshes: [],
            middle_edge_meshes: [],
            edge_caches: [],  // store some information that can be useful
            blossom_convex_meshes: [],
        }
        this.is_vertices_2d_plane = false
        // refresh data
        this.refresh_snapshot_data()
        console.log("fusion 3d component mounted")
    },
    computed: {
        
    },
    methods: {
        async refresh_snapshot_data() {
            if (this.fusion_data == null) {
                return
            }
            const fusion_data = this.fusion_data
            const snapshot_idx_1 = Math.floor(this.snapshot_idx)
            const snapshot_idx_2 = snapshot_idx_1 == this.snapshot_idx ? snapshot_idx_1 : snapshot_idx_1 + 1
            const snapshot_1 = fusion_data.snapshots[snapshot_idx_1][1]
            const snapshot_2 = fusion_data.snapshots[snapshot_idx_2][1]
            let s1r = snapshot_idx_1 == this.snapshot_idx ? 1 : (snapshot_idx_2 - this.snapshot_idx)
            let s2r = snapshot_idx_1 == this.snapshot_idx ? 0 : (this.snapshot_idx - snapshot_idx_1)
            const { scene, vertex_meshes, vertex_outline_meshes, vertex_caches, left_edge_meshes, right_edge_meshes, middle_edge_meshes,
                edge_caches, blossom_convex_meshes } = this.variables
            // update vertex cache
            vertex_caches.length = 0
            this.is_vertices_2d_plane = true
            for (let position of fusion_data.positions) {
                if (position.t != 0) {
                    this.is_vertices_2d_plane = false
                }
                vertex_caches.push({
                    position: {
                        center: compute_vector3(position),
                    }
                })
            }
            // draw vertices
            for (let [i, vertex] of snapshot_1.vertices.entries()) {
                if (vertex == null) {
                    if (i < vertex_meshes.length) {  // hide
                        vertex_meshes[i].visible = false
                    }
                    continue
                }
                let position = fusion_data.positions[i]
                while (vertex_meshes.length <= i) {
                    const vertex_mesh = new THREE.Mesh( vertex_geometry, real_vertex_material )
                    vertex_mesh.visible = false
                    vertex_mesh.userData = {
                        type: "vertex",
                        vertex_index: vertex_meshes.length,
                    }
                    scene.add( vertex_mesh )
                    vertex_meshes.push(vertex_mesh)
                }
                const vertex_mesh = vertex_meshes[i]
                load_position(vertex_mesh.position, position)
                if (vertex.mi != null && vertex.me == 0) {
                    vertex_mesh.material = disabled_mirror_vertex_material
                } else if (vertex.s) {
                    vertex_mesh.material = defect_vertex_material
                } else if (vertex.v) {
                    vertex_mesh.material = virtual_vertex_material
                } else {
                    vertex_mesh.material = real_vertex_material
                }
                vertex_mesh.visible = true
            }
            for (let i = snapshot_1.vertices.length; i < vertex_meshes.length; ++i) {
                vertex_meshes[i].visible = false
            }
            // draw edges
            let subgraph_set = {}
            if (snapshot_1.subgraph != null) {
                for (let edge_index of snapshot_1.subgraph) {
                    subgraph_set[edge_index] = true
                }
            }
            let edge_offset = 0
            if (edge_radius < vertex_outline_radius) {
                edge_offset = Math.sqrt(Math.pow(vertex_outline_radius, 2) - Math.pow(edge_radius, 2))
            }
            edge_caches.length = 0  // clear cache
            for (let [i, edge_1] of snapshot_1.edges.entries()) {
                if (edge_1 == null) {
                    if (i < left_edge_meshes.length) {  // hide
                        for (let j of [0, 1]) {
                            left_edge_meshes[i][j].visible = false
                            right_edge_meshes[i][j].visible = false
                            middle_edge_meshes[i][j].visible = false
                        }
                    }
                    continue
                }
                const edge_2 = snapshot_2.edges[i]
                const left_position = fusion_data.positions[edge_1.l]
                const right_position = fusion_data.positions[edge_1.r]
                const relative = compute_vector3(right_position).add(compute_vector3(left_position).multiplyScalar(-1))
                const direction = relative.clone().normalize()
                const quaternion = new THREE.Quaternion()
                quaternion.setFromUnitVectors(unit_up_vector, direction)
                const reverse_quaternion = new THREE.Quaternion()
                reverse_quaternion.setFromUnitVectors(unit_up_vector, direction.clone().multiplyScalar(-1))
                let local_edge_offset = edge_offset
                const distance = relative.length()
                let edge_length = distance - 2 * edge_offset
                if (edge_length < 0) {  // edge length should be non-negative
                    local_edge_offset = distance / 2
                    edge_length = 0
                }
                const left_start = local_edge_offset
                let lg = edge_1.lg * s1r + edge_2.lg * s2r
                let rg = edge_1.rg * s1r + edge_2.rg * s2r
                const [left_grown, right_grown] = translate_edge(lg, rg, edge_1.w)
                let left_end = local_edge_offset + edge_length * (edge_1.w == 0 ? 0.5 : (left_grown / edge_1.w))  // always show 0-weight edge as fully-grown
                let right_end = local_edge_offset + edge_length * (edge_1.w == 0 ? 0.5 : (edge_1.w - right_grown) / edge_1.w)  // always show 0-weight edge as fully-grown
                const right_start = local_edge_offset + edge_length
                edge_caches.push({
                    position: {
                        left_start: compute_vector3(left_position).add(relative.clone().multiplyScalar(left_start / distance)),
                        left_end: compute_vector3(left_position).add(relative.clone().multiplyScalar(left_end / distance)),
                        right_end: compute_vector3(left_position).add(relative.clone().multiplyScalar(right_end / distance)),
                        right_start: compute_vector3(left_position).add(relative.clone().multiplyScalar(right_start / distance)),
                    }
                })
                for (let [start, end, edge_meshes, is_grown_part] of [[left_start, left_end, left_edge_meshes, true], [left_end, right_end, middle_edge_meshes, false]
                        , [right_end, right_start, right_edge_meshes, true]]) {
                    while (edge_meshes.length <= i) {
                        let two_edges = [null, null]
                        for (let j of [0, 1]) {
                            const edge_mesh = new THREE.Mesh( edge_geometry, edge_material )
                            edge_mesh.userData = {
                                type: "edge",
                                edge_index: edge_meshes.length,
                            }
                            edge_mesh.visible = false
                            scene.add( edge_mesh )
                            two_edges[j] = edge_mesh
                        }
                        edge_meshes.push(two_edges)
                    }
                    const start_position = compute_vector3(left_position).add(relative.clone().multiplyScalar(start / distance))
                    const end_position = compute_vector3(left_position).add(relative.clone().multiplyScalar(end / distance))
                    for (let j of [0, 1]) {
                        const edge_mesh = edge_meshes[i][j]
                        edge_mesh.position.copy(j == 0 ? start_position : end_position)
                        edge_mesh.scale.set(1, (end - start) / 2, 1)
                        edge_mesh.setRotationFromQuaternion(j == 0 ? quaternion : reverse_quaternion)
                        edge_mesh.visible = true
                        if (start >= end) {
                            edge_mesh.visible = false
                        }
                        edge_mesh.material = is_grown_part ? grown_edge_material : edge_material
                        if (snapshot_1.subgraph != null) {
                            edge_mesh.material = edge_material  // do not display grown edges
                        }
                        if (subgraph_set[i]) {
                            edge_mesh.material = subgraph_edge_material
                        }
                    }
                }
            }
            for (let i = snapshot_1.edges.length; i < left_edge_meshes.length; ++i) {
                for (let j of [0, 1]) {
                    left_edge_meshes[i][j].visible = false
                    right_edge_meshes[i][j].visible = false
                    middle_edge_meshes[i][j].visible = false
                }
            }
            // draw vertex outlines
            for (let [i, vertex] of snapshot_1.vertices.entries()) {
                if (vertex == null) {
                    if (i < vertex_outline_meshes.length) {  // hide
                        vertex_outline_meshes[i].visible = false
                    }
                    continue
                }
                let position = fusion_data.positions[i]
                while (vertex_outline_meshes.length <= i) {
                    const vertex_outline_mesh = new THREE.Mesh( vertex_geometry, real_vertex_outline_material )
                    vertex_outline_mesh.visible = false
                    vertex_outline_mesh.scale.x = outline_ratio
                    vertex_outline_mesh.scale.y = outline_ratio
                    vertex_outline_mesh.scale.z = outline_ratio
                    scene.add( vertex_outline_mesh )
                    vertex_outline_meshes.push(vertex_outline_mesh)
                }
                const vertex_outline_mesh = vertex_outline_meshes[i]
                load_position(vertex_outline_mesh.position, position)
                if (vertex.s) {
                    vertex_outline_mesh.material = defect_vertex_outline_material
                } else if (vertex.v) {
                    vertex_outline_mesh.material = virtual_vertex_outline_material
                } else {
                    vertex_outline_mesh.material = real_vertex_outline_material
                }
                vertex_outline_mesh.visible = true
            }
            for (let i = snapshot_1.vertices.length; i < vertex_meshes.length; ++i) {
                vertex_outline_meshes[i].visible = false
            }
            // draw convex
            if (snapshot_1.dual_nodes != null) {
                for (let blossom_convex_mesh of blossom_convex_meshes) {
                    scene.remove( blossom_convex_mesh )
                    blossom_convex_mesh.geometry.dispose()
                }
                for (let [i, dual_node_1] of snapshot_1.dual_nodes.entries()) {
                    let dual_node_2 = null
                    if (snapshot_2.dual_nodes != null && i < snapshot_2.dual_nodes.length) dual_node_2 = snapshot_2.dual_nodes[i]
                    if (dual_node_1 == null && dual_node_2 == null) { continue }
                    if (snapshot_1.subgraph != null) { continue }  // do not display convex if subgraph is displayed
                    // for child node in a blossom, this will not display properly; we should avoid plotting child nodes
                    let composed_dual_node = {
                        d: dual_node_1 == null ? dual_node_2.d : (dual_node_2 == null ? dual_node_1.d : dual_node_1.d * s1r + dual_node_2.d * s2r),
                    }
                    let display_node = dual_node_1.p == null && (composed_dual_node.d > 0 || dual_node_1.o != null)
                    if (display_node) {  // no parent and (positive dual variable or it's a blossom)
                        let points = []
                        if (dual_node_2.b != null) {
                            for (let [is_left, edge_index] of dual_node_2.b) {
                                let cached_position = edge_caches[edge_index].position
                                const edge_1 = snapshot_1.edges[edge_index]
                                const edge_2 = snapshot_2.edges[edge_index]
                                const lg = edge_1.lg * s1r + edge_2.lg * s2r
                                const rg = edge_1.rg * s1r + edge_2.rg * s2r
                                if (edge_1.ld == edge_1.rd && lg + rg >= edge_1.w) {
                                    continue  // do not draw this edge, this is an internal edge
                                }
                                if (is_left) {
                                    if (lg == edge_1.w) {
                                        points.push(vertex_caches[edge_1.r].position.center.clone())
                                    } else if (lg == 0) {
                                        points.push(vertex_caches[edge_1.l].position.center.clone())
                                    } else {
                                        points.push(cached_position.left_end.clone())
                                    }
                                } else {
                                    if (rg == edge_1.w) {
                                        points.push(vertex_caches[edge_1.l].position.center.clone())
                                    } else if (rg == 0) {
                                        points.push(vertex_caches[edge_1.r].position.center.clone())
                                    } else {
                                        points.push(cached_position.right_end.clone())
                                    }
                                }
                            }
                        }
                        if (points.length >= 3) {  // only display if points is more than 3
                            if (this.is_vertices_2d_plane) {
                                // special optimization for 2D points, because ConvexGeometry doesn't work well on them
                                const points_2d = []
                                for (let point of points) {
                                    points_2d.push([ point.x, point.z ])
                                }
                                const hull_points = hull(points_2d, 1)
                                const shape_points = []
                                for (let hull_point of hull_points) {
                                    shape_points.push( new THREE.Vector2( hull_point[0], hull_point[1] ) );
                                }
                                const shape = new THREE.Shape( shape_points )
                                const geometry = new THREE.ShapeGeometry( shape )
                                const blossom_convex_mesh = new THREE.Mesh( geometry, blossom_convex_material_2d )
                                blossom_convex_mesh.position.set( 0, -0.2, 0 )  // place the plane to slightly below the vertices for better viz
                                blossom_convex_mesh.rotation.set( Math.PI / 2, 0, 0 );
                                scene.add( blossom_convex_mesh )
                                blossom_convex_meshes.push(blossom_convex_mesh)
                            } else {
                                const geometry = new ConvexGeometry( points )
                                const blossom_convex_mesh = new THREE.Mesh( geometry, blossom_convex_material )
                                scene.add( blossom_convex_mesh )
                                blossom_convex_meshes.push(blossom_convex_mesh)
                            }
                        }
                    }
                }
            }
        },
    },
    watch: {
        snapshot_idx() {
            this.refresh_snapshot_data()
        },
        snapshot_idx_interpolated() {

        },
        fusion_data() {
            this.refresh_snapshot_data()
        },
    },
}
</script>
