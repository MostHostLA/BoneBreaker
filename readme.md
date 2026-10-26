# 🦴 Bone Breaker

> **An Epic MegaGrants recipient plugin for Blender that allows you to quickly and almost effortlessly edit, adjust, and export default Unreal Engine 4 animations.**

---

## ✨ Features

- 🔄 **Rigify Integration** – Automatically generates a metarig matching your incoming FBX armature and hooks it up to Rigify controls.
- 🏃 **Animation Baking** – Automatically tracks incoming FBX animation data, registers keyframes, and bakes them onto your animation rig.
- 📐 **Perfect Scale Alignment** – Instantly overrides your Blender scene metrics to match UE4 scale parameters seamlessly.
- 🧵 **Cloth Visualizer** – Specialized viewport tool for painting vertex colors while visualizing the distance values expected by ApexCloth/NVCloth inside Unreal.
- 📤 **Flawless FBX Pipeline** – Exports your animations back to UE4 with exact root orientations and proper bone hierarchies—no more guess work.

---

### 📋 Prerequisites

* Blender 3.0.0 (or version compatible with your release)
* Target FBX animation files exported from Unreal Engine 4

### 🔧 Installation

1. Download the latest `.zip` release of Bone Breaker.
2. In Blender, go to **Edit > Preferences > Add-ons**.
3. Click **Install...**, select your downloaded `.zip` file, and enable the add-on.

---

## 🕹️ Addon Usage

Follow this workflow to rapidly clean up or adjust your UE4 animations inside Blender:

1. **Click "Import FBX"** – This overrides your scene settings to Metric scale guidelines and brings in your targeted animation FBX.
2. **Click "DO IT ALL" in Char Rigging** – Generates a matching metarig and builds out your functional control rig layout.
3. **Click "DO IT ALL" in Rig Action** – Captures any incoming motion data and maps it clean to the control sliders and bones.
4. **Animate / Correct** – Make all your necessary tweaks to the animation path inside Blender.
5. **Click "Key All Frames"** – Automatically bakes down and registers keyframes across the timeline.
6. **Click "Export FBX"** – Saves your newly minted animation track, completely formatted for direct drag-and-drop import back into Unreal Engine onto the original skeleton asset.

---

## 📝 License

This software is provided "as is", with the following restriction.
You may NOT include this software into a PAID application or 
make a profit by directly selling portions of this code.
