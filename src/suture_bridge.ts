/* FILE: suture_bridge.ts */
import init, { SutureOven } from "./wasm/suture_core.js";

async function runOven() {
    // 1. Initialize the Wasm context
    await init();
    const oven = new SutureOven();

    // 2. Load the Quartz Seed (The Lumber)
    const quartzResponse = await fetch("/seeds/quartz_alpha.suture");
    const quartzSeed = await quartzResponse.json();
    
    // 3. Germinate the Saturated Field
    oven.load_seed(quartzSeed);

    // 4. The Time Slider Hook
    const timeSlider = document.getElementById("geologic-time");
    timeSlider.oninput = (e) => {
        const delta = parseFloat(e.target.value);
        oven.apply_erosion(delta); // Subtractive Chisel in action
    };

    // 5. The Loupe Hook
    window.addEventListener("wheel", (e) => {
        const zoom = e.deltaY;
        oven.update_fracture_depth(zoom); // Scale-Coherence trigger
    });
}

runOven();
/* END FILE: suture_bridge.ts */
