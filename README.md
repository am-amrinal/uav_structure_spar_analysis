# UAV Spar Structural Analysis Dashboard

🔩 An interactive **Streamlit** web application to analyze and compare the structural performance of UAV wing spars (bending stress, tip deflection, weight, and safety margin).

## ✨ Features

- ✅ **Dark mode UI**
- 📊 Multi-spar comparison (e.g., 20mm vs 10mm carbon tubes)
- 📈 Visualizations for stress & deflection
- 🧠 Real-time calculations for:
  - Bending stress (σ)
  - Tip deflection
  - Weight estimation
  - Safety margin

## ⚙️ Input Parameters

Accessible from the **left sidebar**:

- Spar length (m)
- Load at tip (N)
- Young’s Modulus (GPa)
- Yield strength (MPa)
- Material density (kg/m³)

## 🚀 Getting Started

### 1. Clone this repo

```bash
git clone https://github.com/your-username/uav-spar-analysis.git
cd uav-spar-analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will launch in your default browser at `http://localhost:8501`.

## 📦 Requirements

Create a `requirements.txt` file with:

```
streamlit
numpy
pandas
matplotlib
```

## 📚 Structural Theory Used

- **Moment of Inertia** for hollow circular section:
  \[
  I = \frac{\pi}{4} (r_o^4 - r_i^4)
  \]

- **Bending stress**:
  \[
  \sigma = \frac{M \cdot c}{I}
  \]

- **Deflection (cantilever beam with tip load)**:
  \[
  \delta = \frac{F L^3}{3 E I}
  \]

## 📸 Preview

> _Add screenshot or GIF of app interface here if needed._

## 🛠️ Author

Developed by am-amrinal.

## 📄 License

MIT License.
