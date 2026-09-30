"""MasteryFlow 3D Cybernetic Knowledge Universe (universe_3d.py).

High-Performance 3D WebGL / Three.js Interactive Curriculum Visualizer.
Renders the 10 canonical concepts in full 3D spatial orbital coordinates with:
- 3D concept spheres with low-saturation status palette and orbital rings
- Animated prerequisite energy pulses traveling along 3D connection arcs
- 360-degree OrbitControls (pan, zoom, rotate, inspect)
- Interactive raycasting: click any 3D node to inspect its pedagogical state
- Floating clean light HUD with concept metadata, effective mastery, and prerequisites
- Dynamic camera positioning and preset view angles
"""

from __future__ import annotations
import json
from typing import Any, Dict, Optional
import streamlit.components.v1 as components


# Spatial 3D coordinates for the 10 Canonical Concepts (Tiered pedagogical layout)
NODE_3D_COORDINATES = {
    "C1": {"x": 0, "y": -140, "z": 0, "tier": 1},
    "C2": {"x": 0, "y": -70, "z": 0, "tier": 2},
    "C3": {"x": -90, "y": 0, "z": -30, "tier": 3},
    "C4": {"x": -30, "y": 0, "z": 40, "tier": 3},
    "C5": {"x": 30, "y": 0, "z": 40, "tier": 3},
    "C6": {"x": 90, "y": 0, "z": -30, "tier": 3},
    "C7": {"x": -50, "y": 70, "z": 10, "tier": 4},
    "C9": {"x": 50, "y": 70, "z": -10, "tier": 4},
    "C8": {"x": -30, "y": 140, "z": 0, "tier": 5},
    "C10": {"x": 0, "y": 210, "z": 0, "tier": 6},
}

# 3D Cybernetic Palette for Dark Graph Segment
STATUS_3D_COLORS = {
    "mastered": {"color": 0x10B981, "hex": "#10B981", "glow": "rgba(16, 185, 129, 0.40)"},
    "practicing": {"color": 0x38BDF8, "hex": "#38BDF8", "glow": "rgba(56, 189, 248, 0.40)"},
    "provisional": {"color": 0xF59E0B, "hex": "#F59E0B", "glow": "rgba(245, 158, 11, 0.40)"},
    "fragile": {"color": 0xF43F5E, "hex": "#F43F5E", "glow": "rgba(244, 63, 94, 0.40)"},
    "unseen": {"color": 0x64748B, "hex": "#64748B", "glow": "rgba(100, 116, 139, 0.25)"},
}


def build_3d_universe_html(
    concepts_meta: Dict[str, Dict[str, Any]],
    mastery_map: Dict[str, Dict[str, Any]],
    active_concept_id: str = "C1",
    height: int = 620,
) -> str:
    """Generates the self-contained Three.js WebGL 3D Knowledge Universe HTML/JS payload in Apitex Warm Alabaster theme."""
    nodes_data = []
    links_data = []

    for cid, coord in NODE_3D_COORDINATES.items():
        cm = concepts_meta.get(cid, {})
        ms = mastery_map.get(cid, {})

        p_eff = float(ms.get("p_eff", 0.30))
        is_fragile = bool(ms.get("is_fragile", False))
        status_raw = str(ms.get("status", "unseen"))
        stability = ms.get("stability_days", 7.0)

        if is_fragile:
            st_key = "fragile"
        elif status_raw in STATUS_3D_COLORS:
            st_key = status_raw
        else:
            st_key = "practicing" if p_eff > 0.35 else "unseen"

        is_active = (cid == active_concept_id)

        node_entry = {
            "id": cid,
            "name": cm.get("name", cid),
            "icon": cm.get("icon", ""),
            "x": coord["x"],
            "y": coord["y"],
            "z": coord["z"],
            "tier": coord["tier"],
            "status": st_key,
            "p_eff": round(p_eff * 100, 1),
            "stability": stability,
            "isActive": is_active,
            "prereqs": cm.get("prerequisites", []),
        }
        nodes_data.append(node_entry)

        # Build links from prerequisites
        for p_id in cm.get("prerequisites", []):
            if p_id in NODE_3D_COORDINATES:
                links_data.append({"source": p_id, "target": cid})

    nodes_json = json.dumps(nodes_data)
    links_json = json.dumps(links_data)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MasteryFlow 3D Universe - Apitex Edition</title>
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                user-select: none;
            }}
            body {{
                background: #0B0F19;
                overflow: hidden;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #F8FAFC;
                width: 100vw;
                height: 100vh;
                border-radius: 18px;
            }}
            #canvas-container {{
                width: 100%;
                height: 100%;
                position: relative;
            }}
            /* HUD Controls */
            .hud-overlay {{
                position: absolute;
                top: 14px;
                left: 18px;
                z-index: 10;
                pointer-events: none;
            }}
            .hud-badge {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: rgba(15, 23, 42, 0.88);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.15);
                padding: 6px 14px;
                border-radius: 9999px;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 0.5px;
                color: #38BDF8;
                box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
                text-transform: uppercase;
            }}
            .hud-title {{
                font-size: 15px;
                font-weight: 800;
                color: #F8FAFC;
                margin-top: 5px;
                letter-spacing: -0.2px;
            }}
            .hud-desc {{
                font-size: 11px;
                color: #94A3B8;
                margin-top: 2px;
            }}
            /* Interactive 3D Tool Controls */
            .controls-panel {{
                position: absolute;
                bottom: 16px;
                left: 18px;
                display: flex;
                gap: 8px;
                z-index: 10;
                flex-wrap: wrap;
            }}
            .hud-btn {{
                background: rgba(15, 23, 42, 0.88);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                color: #F1F5F9;
                font-size: 11px;
                font-weight: 700;
                padding: 7px 14px;
                border-radius: 9999px;
                cursor: pointer;
                transition: all 0.18s ease;
                display: flex;
                align-items: center;
                gap: 5px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
            }}
            .hud-btn:hover {{
                background: #38BDF8;
                border-color: #38BDF8;
                color: #0B0F19;
                box-shadow: 0 4px 16px rgba(56, 189, 248, 0.45);
            }}
            /* Floating Hologram Inspection Card */
            #inspect-card {{
                position: absolute;
                top: 14px;
                right: 18px;
                width: 290px;
                background: rgba(15, 23, 42, 0.94);
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 20px;
                padding: 18px;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.08);
                z-index: 10;
                display: none;
                backdrop-filter: blur(20px);
                animation: fadeIn 0.25s ease;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(-6px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            .inspect-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 6px;
            }}
            .inspect-id {{
                font-size: 14px;
                font-weight: 800;
                color: #FFFFFF;
            }}
            .inspect-badge {{
                font-size: 10px;
                font-weight: 800;
                padding: 2px 8px;
                border-radius: 999px;
                text-transform: uppercase;
                letter-spacing: 0.4px;
            }}
            .inspect-name {{
                font-size: 13px;
                font-weight: 700;
                color: #F1F5F9;
                margin-bottom: 10px;
                line-height: 1.3;
            }}
            .inspect-stat-row {{
                display: flex;
                justify-content: space-between;
                font-size: 11px;
                color: #94A3B8;
                margin-bottom: 4px;
            }}
            .inspect-stat-val {{
                color: #FFFFFF;
                font-weight: 700;
                font-family: monospace;
            }}
            .inspect-bar {{
                width: 100%;
                height: 6px;
                background: rgba(255, 255, 255, 0.12);
                border-radius: 999px;
                overflow: hidden;
                margin: 6px 0 10px 0;
            }}
            .inspect-bar-fill {{
                height: 100%;
                border-radius: 999px;
                transition: width 0.4s ease;
            }}
            .inspect-prereq {{
                font-size: 10px;
                color: #94A3B8;
                border-top: 1px solid rgba(255, 255, 255, 0.12);
                padding-top: 7px;
            }}
            .legend-panel {{
                position: absolute;
                bottom: 16px;
                right: 18px;
                display: flex;
                gap: 10px;
                background: rgba(15, 23, 42, 0.88);
                backdrop-filter: blur(14px);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 9999px;
                padding: 7px 16px;
                font-size: 10.5px;
                font-weight: 600;
                color: #CBD5E1;
                z-index: 10;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
            }}
            .legend-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 3px;
            }}
        </style>
        <!-- Include Three.js & OrbitControls via CDN -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <!-- HUD Overlay -->
            <div class="hud-overlay">
                <div class="hud-badge">3D KNOWLEDGE UNIVERSE</div>
                <div class="hud-title">10-Node Prerequisite Topological Graph</div>
                <div class="hud-desc">Drag to Rotate 360&deg; &middot; Scroll to Zoom &middot; Click Node to Inspect Telemetry</div>
            </div>

            <!-- Floating Inspector Card -->
            <div id="inspect-card">
                <div class="inspect-header">
                    <span id="card-id" class="inspect-id">C1</span>
                    <span id="card-badge" class="inspect-badge">MASTERED</span>
                </div>
                <div id="card-name" class="inspect-name">Fraction Basics</div>
                <div class="inspect-stat-row">
                    <span>Effective Mastery:</span>
                    <span id="card-peff" class="inspect-stat-val">85%</span>
                </div>
                <div class="inspect-bar">
                    <div id="card-bar-fill" class="inspect-bar-fill" style="width: 85%; background: #10B981;"></div>
                </div>
                <div class="inspect-stat-row">
                    <span>Memory Stability:</span>
                    <span id="card-stab" class="inspect-stat-val">7.0d</span>
                </div>
                <div id="card-prereqs" class="inspect-prereq">Prerequisites: None (Baseline)</div>
            </div>

            <!-- Controls Panel -->
            <div class="controls-panel">
                <button class="hud-btn" onclick="resetCamera()">Reset Orbit</button>
                <button class="hud-btn" onclick="toggleAutoRotate()">Auto-Spin</button>
                <button class="hud-btn" onclick="focusActiveConcept()">Focus Target</button>
                <button class="hud-btn" onclick="viewTopDown()">Top-Down DAG</button>
            </div>

            <!-- Status Legend -->
            <div class="legend-panel">
                <span><span class="legend-dot" style="background: #10B981;"></span> Mastered</span>
                <span><span class="legend-dot" style="background: #38BDF8;"></span> Practicing</span>
                <span><span class="legend-dot" style="background: #F59E0B;"></span> Provisional</span>
                <span><span class="legend-dot" style="background: #F43F5E;"></span> Fragile</span>
                <span><span class="legend-dot" style="background: #64748B;"></span> Locked</span>
            </div>
        </div>

        <script>
            const nodes = {nodes_json};
            const links = {links_json};

            const statusColors = {{
                "mastered": 0x10B981,
                "practicing": 0x38BDF8,
                "provisional": 0xF59E0B,
                "fragile": 0xF43F5E,
                "unseen": 0x64748B
            }};

            const statusHex = {{
                "mastered": "#10B981",
                "practicing": "#38BDF8",
                "provisional": "#F59E0B",
                "fragile": "#F43F5E",
                "unseen": "#64748B"
            }};

            // Setup Scene, Camera, Renderer
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x0B0F19, 0.0012);

            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2000);
            camera.position.set(0, 40, 480);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.setClearColor(0x0B0F19, 1.0);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.06;
            controls.maxDistance = 800;
            controls.minDistance = 80;
            controls.autoRotate = true;
            controls.autoRotateSpeed = 0.5;

            // Ambient & Directional Lights for Cybernetic Dark Theme
            const ambientLight = new THREE.AmbientLight(0x334155, 1.4);
            scene.add(ambientLight);

            const pointLight1 = new THREE.PointLight(0x38BDF8, 2.2, 1000);
            pointLight1.position.set(200, 350, 200);
            scene.add(pointLight1);

            const pointLight2 = new THREE.PointLight(0x818CF8, 1.6, 900);
            pointLight2.position.set(-200, -200, -100);
            scene.add(pointLight2);

            // 1. Starlight Particles
            const starGeo = new THREE.BufferGeometry();
            const starCount = 500;
            const starPos = new Float32Array(starCount * 3);
            for (let i = 0; i < starCount * 3; i += 3) {{
                starPos[i] = (Math.random() - 0.5) * 1600;
                starPos[i + 1] = (Math.random() - 0.5) * 1600;
                starPos[i + 2] = (Math.random() - 0.5) * 1600;
            }}
            starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
            const starMat = new THREE.PointsMaterial({{
                color: 0x93C5FD,
                size: 2.2,
                transparent: true,
                opacity: 0.65
            }});
            const starField = new THREE.Points(starGeo, starMat);
            scene.add(starField);

            // 2. Build 3D Concept Spheres & Text Labels
            const nodeMeshMap = {{}};
            const interactiveMeshes = [];
            const pulseRings = [];

            nodes.forEach(n => {{
                const group = new THREE.Group();
                group.position.set(n.x, n.y, n.z);

                const baseCol = statusColors[n.status] || 0x64748B;

                // Sphere Geometry with Emissive Glow
                const sphereRadius = n.isActive ? 18 : 14;
                const sphereGeo = new THREE.SphereGeometry(sphereRadius, 32, 32);
                const sphereMat = new THREE.MeshStandardMaterial({{
                    color: baseCol,
                    roughness: 0.22,
                    metalness: 0.35,
                    emissive: baseCol,
                    emissiveIntensity: n.isActive ? 0.38 : 0.16
                }});
                const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
                sphereMesh.userData = n;
                group.add(sphereMesh);
                interactiveMeshes.push(sphereMesh);

                // Orbital Corona Glow Ring
                const ringGeo = new THREE.RingGeometry(sphereRadius + 3, sphereRadius + 5, 32);
                const ringMat = new THREE.MeshBasicMaterial({{
                    color: baseCol,
                    side: THREE.DoubleSide,
                    transparent: true,
                    opacity: n.isActive ? 0.85 : 0.35
                }});
                const ringMesh = new THREE.Mesh(ringGeo, ringMat);
                ringMesh.rotation.x = Math.PI / 2;
                group.add(ringMesh);
                pulseRings.push(ringMesh);

                // If active target concept, add rotating outer cyan beacon
                if (n.isActive) {{
                    const beaconGeo = new THREE.TorusGeometry(sphereRadius + 9, 1.2, 16, 64);
                    const beaconMat = new THREE.MeshBasicMaterial({{
                        color: 0x38BDF8,
                        transparent: true,
                        opacity: 0.85
                    }});
                    const beaconMesh = new THREE.Mesh(beaconGeo, beaconMat);
                    group.add(beaconMesh);
                    n.beaconMesh = beaconMesh;
                }}

                // Create 2D Sprite Text Billboard for Concept ID in luminous white font
                const canvas = document.createElement('canvas');
                canvas.width = 256;
                canvas.height = 128;
                const ctx = canvas.getContext('2d');
                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 52px -apple-system, BlinkMacSystemFont, sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.shadowColor = 'rgba(0, 0, 0, 0.9)';
                ctx.shadowBlur = 8;
                ctx.fillText(n.id, 128, 64);

                const texture = new THREE.CanvasTexture(canvas);
                const spriteMat = new THREE.SpriteMaterial({{ map: texture, transparent: true }});
                const sprite = new THREE.Sprite(spriteMat);
                sprite.scale.set(40, 20, 1);
                sprite.position.set(0, sphereRadius + 18, 0);
                group.add(sprite);

                scene.add(group);
                nodeMeshMap[n.id] = group;
            }});

            // 3. Neural Prerequisite Arcs & Traveling Energy Pulses
            const pulsePackets = [];

            links.forEach(l => {{
                const src = nodeMeshMap[l.source];
                const tgt = nodeMeshMap[l.target];
                if (src && tgt) {{
                    const p1 = src.position;
                    const p2 = tgt.position;
                    const mid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
                    mid.z += 25;

                    const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
                    const points = curve.getPoints(32);
                    const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
                    const lineMat = new THREE.LineBasicMaterial({{
                        color: 0x475569,
                        transparent: true,
                        opacity: 0.65,
                        linewidth: 2
                    }});
                    const line = new THREE.Line(lineGeo, lineMat);
                    scene.add(line);

                    // Traveling Energy Packet
                    const packetGeo = new THREE.SphereGeometry(2.5, 12, 12);
                    const packetMat = new THREE.MeshBasicMaterial({{ color: 0xFBBF24 }});
                    const packetMesh = new THREE.Mesh(packetGeo, packetMat);
                    scene.add(packetMesh);

                    pulsePackets.push({{
                        mesh: packetMesh,
                        curve: curve,
                        progress: Math.random()
                    }});
                }}
            }});

            // 4. Raycasting for Click / Inspection Interaction
            const raycaster = new THREE.Raycaster();
            const mouse = new THREE.Vector2();
            const inspectCard = document.getElementById('inspect-card');

            function onPointerDown(event) {{
                const rect = renderer.domElement.getBoundingClientRect();
                mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(interactiveMeshes);

                if (intersects.length > 0) {{
                    const hitData = intersects[0].object.userData;
                    displayInspectCard(hitData);
                }}
            }}
            window.addEventListener('pointerdown', onPointerDown);

            function displayInspectCard(n) {{
                document.getElementById('card-id').innerText = n.id;
                const badgeEl = document.getElementById('card-badge');
                badgeEl.innerText = n.status.toUpperCase();
                badgeEl.style.background = statusHex[n.status] + '18';
                badgeEl.style.color = statusHex[n.status];
                badgeEl.style.border = '1px solid ' + statusHex[n.status] + '44';

                document.getElementById('card-name').innerText = n.name;
                document.getElementById('card-peff').innerText = n.p_eff + '%';
                const fillEl = document.getElementById('card-bar-fill');
                fillEl.style.width = n.p_eff + '%';
                fillEl.style.background = statusHex[n.status];

                document.getElementById('card-stab').innerText = n.stability + ' Days';
                const prereqStr = n.prereqs.length > 0 ? n.prereqs.join(', ') : 'None (Foundational)';
                document.getElementById('card-prereqs').innerText = 'Prerequisites: ' + prereqStr;

                inspectCard.style.display = 'block';
                smoothLookAt(n.x, n.y, n.z);
            }}

            function smoothLookAt(tx, ty, tz) {{
                controls.target.set(tx, ty, tz);
            }}

            // Camera View Controls
            window.resetCamera = function() {{
                camera.position.set(0, 40, 480);
                controls.target.set(0, 0, 0);
                inspectCard.style.display = 'none';
            }};

            window.toggleAutoRotate = function() {{
                controls.autoRotate = !controls.autoRotate;
            }};

            window.viewTopDown = function() {{
                camera.position.set(0, 520, 20);
                controls.target.set(0, 0, 0);
            }};

            window.focusActiveConcept = function() {{
                const activeNode = nodes.find(n => n.isActive);
                if (activeNode) {{
                    displayInspectCard(activeNode);
                    camera.position.set(activeNode.x, activeNode.y + 40, activeNode.z + 160);
                    controls.target.set(activeNode.x, activeNode.y, activeNode.z);
                }}
            }};

            // Auto-display active node inspection on initial load
            const initialActive = nodes.find(n => n.isActive);
            if (initialActive) {{
                displayInspectCard(initialActive);
            }}

            // Resize handling
            window.addEventListener('resize', () => {{
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }});

            // Animation Loop
            let clock = new THREE.Clock();

            function animate() {{
                requestAnimationFrame(animate);
                const delta = clock.getDelta();
                const elapsed = clock.getElapsedTime();

                // Rotate starfield slowly
                starField.rotation.y = elapsed * 0.02;

                // Animate pulse rings
                pulseRings.forEach((r, idx) => {{
                    const s = 1 + Math.sin(elapsed * 2.5 + idx) * 0.08;
                    r.scale.set(s, s, s);
                }});

                // Rotate active beacon ring
                nodes.forEach(n => {{
                    if (n.beaconMesh) {{
                        n.beaconMesh.rotation.x = elapsed * 1.5;
                        n.beaconMesh.rotation.y = elapsed * 2.0;
                    }}
                }});

                // Animate traveling prerequisite energy pulses
                pulsePackets.forEach(p => {{
                    p.progress += delta * 0.45;
                    if (p.progress > 1.0) p.progress = 0.0;
                    const pos = p.curve.getPoint(p.progress);
                    p.mesh.position.copy(pos);
                }});

                controls.update();
                renderer.render(scene, camera);
            }}

            animate();
        </script>
    </body>
    </html>
    """
    return html_content


def render_3d_universe_widget(
    concepts_meta: Dict[str, Dict[str, Any]],
    mastery_map: Dict[str, Dict[str, Any]],
    active_concept_id: str = "C1",
    height: int = 620,
) -> None:
    """Renders the interactive 3D WebGL Three.js Knowledge Universe directly in Streamlit."""
    import streamlit as st
    html_code = build_3d_universe_html(
        concepts_meta=concepts_meta,
        mastery_map=mastery_map,
        active_concept_id=active_concept_id,
        height=height,
    )
    st.markdown(
        """<div style="border-radius: 20px; overflow: hidden; border: 1px solid #1E293B; box-shadow: 0 12px 36px -4px rgba(11, 15, 25, 0.45); margin-bottom: 18px;">""",
        unsafe_allow_html=True,
    )
    components.html(html_code, height=height, scrolling=False)
    st.markdown("""</div>""", unsafe_allow_html=True)
