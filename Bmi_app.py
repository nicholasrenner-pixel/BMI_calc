import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

st.title("⚖️ BMI Calculator")
st.caption("Body Mass Index — a simple screening tool based on height and weight.")

# ── Unit toggle ───────────────────────────────────────────────────────────────
unit = st.radio("Unit system", ["Metric (kg / cm)", "Imperial (lbs / in)"], horizontal=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
if unit == "Metric (kg / cm)":
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.5)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=300.0, value=170.0, step=0.5)
    weight_kg = weight
    height_m  = height / 100
else:
    weight = st.number_input("Weight (lbs)", min_value=1.0, max_value=1100.0, value=154.0, step=1.0)
    height = st.number_input("Height (inches)", min_value=20.0, max_value=120.0, value=67.0, step=0.5)
    weight_kg = weight * 0.453592
    height_m  = height * 0.0254

# ── Calculation ───────────────────────────────────────────────────────────────
def bmi_category(bmi: float) -> tuple[str, str]:
    """Return (category label, colour hex) for a given BMI."""
    if bmi < 18.5:
        return "Underweight", "#3b9edd"
    elif bmi < 25.0:
        return "Normal weight", "#2ecc71"
    elif bmi < 30.0:
        return "Overweight", "#f39c12"
    else:
        return "Obese", "#e74c3c"

if st.button("Calculate BMI", use_container_width=True, type="primary"):
    if height_m <= 0:
        st.error("Height must be greater than zero.")
    else:
        bmi = weight_kg / (height_m ** 2)
        category, colour = bmi_category(bmi)

        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("Your BMI", f"{bmi:.1f}")
        col2.markdown(
            f"<div style='padding:8px 14px;border-radius:8px;"
            f"background:{colour};color:#fff;font-weight:600;font-size:1.1rem;"
            f"text-align:center;margin-top:8px'>{category}</div>",
            unsafe_allow_html=True,
        )

        # ── Reference table ───────────────────────────────────────────────────
        st.divider()
        st.subheader("BMI Reference Ranges")
        st.table(
            {
                "Category":   ["Underweight", "Normal weight", "Overweight", "Obese"],
                "BMI Range":  ["< 18.5", "18.5 – 24.9", "25.0 – 29.9", "≥ 30.0"],
            }
        )

        st.caption(
            "⚠️ BMI is a screening tool, not a diagnostic measure. "
            "Consult a healthcare professional for personalised advice."
        )
