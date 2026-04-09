/* FILE: chisel.wgsl */
struct Voxel {
    pos: vec3<f32>,
    cov: vec4<f32>, // Packed covariance
    dna: vec4<f32>, // [n, rho, E, phantasmagoria]
    alpha: f32,
};

@group(0) @binding(0) var<storage, read> voxel_field: array<Voxel>;
@group(0) @binding(1) var<uniform> camera_plane: mat4x4<f32>;

struct VertexOutput {
    @builtin(position) pos: vec4<f32>,
    @location(0) color: vec4<f32>,
};

@vertex
fn vs_main(@builtin(vertex_index) in_vertex_index: u32) -> VertexOutput {
    let voxel = voxel_field[in_vertex_index];
    
    // Constant Projection: The voxel is already there. 
    // We just transform its Gaussian Mean to the camera plane.
    var out: VertexOutput;
    out.pos = camera_plane * vec4<f32>(voxel.pos, 1.0);
    
    // Branched Flow: Light state is sampled from the DNA
    let light_intensity = calculate_branched_flow(voxel);
    out.color = vec4<f32>(light_intensity, light_intensity, light_intensity, voxel.alpha);
    
    return out;
}

fn calculate_branched_flow(v: Voxel) -> f32 {
    // The "Magic Bullet": Light follows branched flow through the DNA-defined n
    // We use path randomization based on the refractive index 'n' (v.dna.x)
    let n = v.dna.x;
    let resistance = v.dna.y; // density
    
    let path_potential = sin(v.pos.x * n) * cos(v.pos.z * resistance);
    return smoothstep(0.3, 0.7, path_potential); // Resulting "Branch" intensity
}
/* END FILE: chisel.wgsl */
