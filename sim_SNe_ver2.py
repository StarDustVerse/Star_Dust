import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

class ZoneLayerSupernova:
    def __init__(self, width=800, height=600, num_layers=5):
        self.width = width
        self.height = height
        self.center = (width // 2, height // 2)
        self.num_layers = num_layers
        self.time = 0
        self.explosion_time = 50
        self.core_collapse_time = 30
        self.max_radius = min(width, height) // 2.5
        self.explosion_started = False

        # Distinct zone colors
        self.zone_colors = ["#FFD700", "#FF8C00", "#FF4500", "#8B0000", "#4B0082"]
        self.base_radii = np.linspace(self.max_radius * 0.2, self.max_radius, num_layers)

        # Set up the plot
        self.fig, self.ax = plt.subplots(figsize=(12, 9))
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('black')

        # Create concentric circle patches
        self.layers = []
        for i in range(num_layers):
            color = self.zone_colors[i % len(self.zone_colors)]
            circle = patches.Circle(
                self.center,
                radius=self.base_radii[i],
                facecolor=color,
                edgecolor='none',
                alpha=0.6
            )
            self.ax.add_patch(circle)
            self.layers.append(circle)

        # Title and info text
        self.title = self.ax.set_title('Supernova Zone Layer Simulation', fontsize=16, color='white')
        self.info_text = self.ax.text(
            0.02, 0.98, '', transform=self.ax.transAxes,
            fontsize=10, color='white', verticalalignment='top'
        )

    def update_layers(self, frame):
        self.time = frame

        # Reset everything at loop start
        if frame == 0:
            self.explosion_started = False
            for i, circle in enumerate(self.layers):
                circle.set_radius(self.base_radii[i])
                circle.set_alpha(0.6)
                circle.set_facecolor(self.zone_colors[i % len(self.zone_colors)])

        if self.time < self.core_collapse_time:
            phase = "Core Collapse"
            progress = 1 - (frame / self.core_collapse_time) * 0.7
            for i, circle in enumerate(self.layers):
                radius = self.base_radii[i] * progress
                circle.set_radius(radius)

        elif self.time < self.explosion_time:
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

        info = f"Phase: {phase}\nFrame: {frame}"
        self.info_text.set_text(info)
        return self.layers + [self.info_text]

    def run(self, frames=200, interval=50, save=False):
        self.ani = animation.FuncAnimation(
            self.fig, self.update_layers, frames=frames,
            interval=interval, blit=True
        )

        # Always display the live animation
        plt.tight_layout()
        plt.show()
        plt.close(self.fig) 

# Run the simulation and save as MP4
if __name__ == "__main__":
    print("Starting supernova zone simulation with distinct colors...")
    sim = ZoneLayerSupernova(width=800, height=600, num_layers=5)
    sim.run(frames=130, interval=50, save=False)

