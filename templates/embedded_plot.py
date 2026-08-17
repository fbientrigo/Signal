# Embedded Signal-style plotting block: native Python, no Signal dependency.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6.0, 3.8), layout="constrained")
ax.plot(x, y, marker="o")
ax.set(xlabel="x", ylabel="y")
