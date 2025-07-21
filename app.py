import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ====================
# Streamlit page config
# ====================
st.set_page_config(page_title="Spar Structural Analysis", layout="wide")

# Apply dark mode
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stApp {
            background-color: #0e1117;
        }
    </style>
    """, unsafe_allow_html=True)

# ====================
# Sidebar Input
# ====================
st.sidebar.header("Spar Parameters")

# Global Parameters
L = st.sidebar.number_input("Spar Length (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
F = st.sidebar.number_input("Applied Load (N)", min_value=0.0, max_value=10000.0, value=100.0, step=10.0)
E = st.sidebar.number_input("Young's Modulus (GPa)", min_value=1.0, max_value=500.0, value=70.0, step=1.0)
sigma_yield = st.sidebar.number_input("Yield Strength (MPa)", min_value=10.0, max_value=2000.0, value=500.0, step=10.0)
density = st.sidebar.number_input("Density (kg/m³)", min_value=500.0, max_value=3000.0, value=1600.0, step=10.0)

# Spar 1
st.sidebar.subheader("Spar 1")
od1 = st.sidebar.number_input("OD Spar 1 (mm)", min_value=1.0, value=20.0)
id1 = st.sidebar.number_input("ID Spar 1 (mm)", min_value=0.0, value=18.0)

# Spar 2
st.sidebar.subheader("Spar 2")
od2 = st.sidebar.number_input("OD Spar 2 (mm)", min_value=1.0, value=10.0)
id2 = st.sidebar.number_input("ID Spar 2 (mm)", min_value=0.0, value=8.0)

# ====================
# Function Definitions
# ====================
def calc_spar_properties(OD_mm, ID_mm, L, F, E, sigma_yield, density):
    OD = OD_mm / 1000
    ID = ID_mm / 1000
    I = (np.pi / 64) * (OD**4 - ID**4)
    c = OD / 2
    stress = (F * L) / I * c  # Bending stress
    deflection = (F * L**3) / (3 * (E * 1e9) * I)
    volume = np.pi * (OD**2 - ID**2) / 4 * L
    mass = volume * density
    safety = sigma_yield * 1e6 / stress if stress > 0 else np.inf
    return stress / 1e6, deflection * 1000, mass, safety  # MPa, mm, kg, ratio

# ====================
# Calculation
# ====================
s1 = calc_spar_properties(od1, id1, L, F, E, sigma_yield, density)
s2 = calc_spar_properties(od2, id2, L, F, E, sigma_yield, density)

# ====================
# Output
# ====================
st.title("🛠️ Spar Structural Analysis Dashboard")
st.markdown("Compare two different spar tube configurations under the same loading.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🔵 Spar 1")
    st.metric("Bending Stress", f"{s1[0]:.2f} MPa")
    st.metric("Deflection", f"{s1[1]:.2f} mm")
    st.metric("Mass", f"{s1[2]:.3f} kg")
    st.metric("Safety Factor", f"{s1[3]:.2f}")

with col2:
    st.subheader("🟢 Spar 2")
    st.metric("Bending Stress", f"{s2[0]:.2f} MPa")
    st.metric("Deflection", f"{s2[1]:.2f} mm")
    st.metric("Mass", f"{s2[2]:.3f} kg")
    st.metric("Safety Factor", f"{s2[3]:.2f}")

# ====================
# Charts
# ====================
loads = np.linspace(0, F, 50)
s1_stress = [(f * L) / ((np.pi / 64) * ((od1/1000)**4 - (id1/1000)**4)) * (od1/2000) / 1e6 for f in loads]
s2_stress = [(f * L) / ((np.pi / 64) * ((od2/1000)**4 - (id2/1000)**4)) * (od2/2000) / 1e6 for f in loads]

fig, ax = plt.subplots()
ax.plot(loads, s1_stress, label="Spar 1", color='cyan')
ax.plot(loads, s2_stress, label="Spar 2", color='lime')
ax.set_xlabel("Load (N)")
ax.set_ylabel("Bending Stress (MPa)")
ax.set_title("Bending Stress vs Load")
ax.grid(True)
ax.legend()
st.pyplot(fig)

fig2, ax2 = plt.subplots()
s1_defl = [(f * L**3) / (3 * (E * 1e9) * (np.pi / 64) * ((od1/1000)**4 - (id1/1000)**4)) * 1000 for f in loads]
s2_defl = [(f * L**3) / (3 * (E * 1e9) * (np.pi / 64) * ((od2/1000)**4 - (id2/1000)**4)) * 1000 for f in loads]
ax2.plot(loads, s1_defl, label="Spar 1", color='cyan')
ax2.plot(loads, s2_defl, label="Spar 2", color='lime')
ax2.set_xlabel("Load (N)")
ax2.set_ylabel("Deflection (mm)")
ax2.set_title("Deflection vs Load")
ax2.grid(True)
ax2.legend()
st.pyplot(fig2)

# Optional: Data download
df = pd.DataFrame({
    "Load (N)": loads,
    "Stress Spar 1 (MPa)": s1_stress,
    "Stress Spar 2 (MPa)": s2_stress,
    "Deflection Spar 1 (mm)": s1_defl,
    "Deflection Spar 2 (mm)": s2_defl,
})
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV Data", data=csv, file_name="spar_comparison.csv", mime="text/csv")
