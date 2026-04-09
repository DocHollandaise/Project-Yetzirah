📋 The Steel (src/lib.rs)
Rust
/* Project: Yoga Fire (Project Yetzirah) 
   Author: Doc Hollandaise
   Description: Core Kiln logic for subtractive voxel saturation.
*/

pub struct YogaFireKiln {
    pub influence_horizon: f32,
    pub current_scale: f32,
}

impl YogaFireKiln {
    pub fn new() -> Self {
        Self {
            influence_horizon: 1.5,
            current_scale: 1.0,
        }
    }

    /// Constant Acoustics: v_s = sqrt(E / rho)
    pub fn calculate_phonon_velocity(&self, youngs_modulus: f32, density: f32) -> f32 {
        (youngs_modulus / density).sqrt()
    }

    /// Placeholder for the Subtractive Chisel logic
    pub fn chisel_voxel(&mut self, occupancy: f32, strength: f32) -> f32 {
        (occupancy - strength).max(0.0)
    }
}
