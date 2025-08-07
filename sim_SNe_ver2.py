import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ---- COMPACT LAYOUT ----
st.set_page_config(layout="wide", page_title="Supernova Sim", initial_sidebar_state="collapsed")

# CSS to remove Streamlit padding and make it iframe-friendly
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---- SIMULATION CLASS ----
class ZoneLayerSupernova:
    def __init__(self, width=400, height=300, num_layers=5):
        self.width = width
        self.height = height
        self.center = (width // 2, height // 2)
        self.num_layers = num_layers
        self.explosion_time = 50
        self.core_collapse_time = 30
        self.max_radius = min(width, height) // 2.5
        self.explosion_started = False

        self.zone_colors = ["#FFD700", "#FF8C00", "#FF4500", "#8B0000", "#4B0082"]
        self.base_radii = np.linspace(self.max_radius * 0.2, self.max_radius, num_layers)

        self.fig, self.ax = plt.subplots(figsize=(4, 3))  # Smaller figure
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('black')

        self.layers = []
        for i in range(num_layers):
            circle = patches.Circle(
                self.center,
                radius=self.base_radii[i],
                facecolor=self.zone_colors[i % len(self.zone_colors)],
                edgecolor='none',
                alpha=0.6
            )
            self.ax.add_patch(circle)
            self.layers.append(circle)

        self.title = self.ax.set_title('', fontsize=14, color='white')
        self.info_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, fontsize=8, color='white', va='top')

    def update_layers(self, frame):
        if frame == 0:
            self.explosion_started = False
            for i, circle in enumerate(self.layers):
                circle.set_radius(self.base_radii[i])
                circle.set_alpha(0.6)

        if frame < self.core_collapse_time:
            phase = "Core Collapse"
            progress = 1 - (frame / self.core_collapse_time) * 0.7
            for i, circle in enumerate(self.layers):
                circle.set_radius(self.base_radii[i] * progress)

        elif frame < self.explosion_time:
            phase = "Critical Moment"
            for i, circle in enumerate(self.layers):
                circle.set_radius(self.base_radii[i] * 0.3)

        else:
            if not self.explosion_started:
                self.explosion_started = True
                self.explosion_start_radii = [c.get_radius() for c in self.layers]

            phase = "Supernova Explosion"
            expansion_progress = min((frame - self.explosion_time) / 60, 1.5)
            fade = max(0, 1.2 - expansion_progress)

            for i, circle in enumerate(self.layers):
                radius = self.explosion_start_radii[i] * (1 + expansion_progress * (1 + i * 0.2))
                circle.set_radius(radius)
                circle.set_alpha(0.6 * fade)

        self.info_text.set_text(f"{phase} - Frame {frame}")

    def draw_final_frame(self, frame):
        self.update_layers(frame)
        return self.fig

# ---- APP UI ----
st.markdown("### 💥 Supernova Simulation")

col1, col2 = st.columns([1, 1])

with col1:
    num_layers = st.slider("Layers", 2, 10, 5, key="layers", label_visibility="collapsed")
with col2:
    frame = st.slider("Frame", 0, 130, 80, key="frame", label_visibility="collapsed")

sim = ZoneLayerSupernova(num_layers=num_layers)
fig = sim.draw_final_frame(frame)
st.pyplot(fig, use_container_width=True)
