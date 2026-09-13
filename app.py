import mpmath
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

mpmath.mp.dps = 30

st.set_page_config(
    page_title="HyperCalc | Consola Científica Avanzada",
    page_icon="🧮",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00ffcc; }
    .stTextInput input, .stTextArea textarea { 
        background-color: #161b22; 
        color: #00ffcc; 
        border: 1px solid #30363d; 
        font-family: monospace;
        font-size: 1.1rem;
    }
    div.stButton > button {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #30363d;
        color: #00ffcc;
        border-color: #00ffcc;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🧮 Consola Científica de Precisión & Motor Simbólico")
st.markdown(
    "Sistema de cálculo avanzado con teclados virtuales unificados, plano interactivo dinámico y GeoGebra integrado."
)
st.markdown("---")

modo = st.sidebar.selectbox(
    "Modo de Operación:",
    [
        "Calculadora Científica Interactiva",
        "Cálculo Simbólico, Derivadas/Integrales y Plano Cartesiano",
        "Geometría Avanzada (GeoGebra)",
        "Resolución de Sistemas Lineales",
    ],
)

if modo == "Calculadora Científica Interactiva":
    st.subheader(
        "🔢 Calculadora Científica Interactiva & Alta Precisión (30+ decimales)"
    )
    st.markdown(
        "Utiliza el teclado virtual unificado para realizar operaciones científicas completas y evaluaciones extremas."
    )

    if "sci_val" not in st.session_state:
        st.session_state.sci_val = ""


    def add_sci(val):
        st.session_state.sci_val += val


    st.markdown("**⌨️ Teclado Científico Unificado:**")

    # Fila de operadores numéricos básicos y de alta precisión
    b1, b2, b3, b4, b5, b6, b7 = st.columns(7)
    if b1.button("➕ (+)"):
        add_sci("+")
    if b2.button("➖ (-)"):
        add_sci("-")
    if b3.button("✖️ (*)"):
        add_sci("*")
    if b4.button("➗ (/)"):
        add_sci("/")
    if b5.button("("):
        add_sci("(")
    if b6.button(")"):
        add_sci(")")
    if b7.button("🗑️ Clear"):
        st.session_state.sci_val = ""

    # Fila de números y punto
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    if c1.button("7"):
        add_sci("7")
    if c2.button("8"):
        add_sci("8")
    if c3.button("9"):
        add_sci("9")
    if c4.button("4"):
        add_sci("4")
    if c5.button("5"):
        add_sci("5")
    if c6.button("6"):
        add_sci("6")

    c7, c8, c9, c10, c11, c12 = st.columns(6)
    if c7.button("1"):
        add_sci("1")
    if c8.button("2"):
        add_sci("2")
    if c9.button("3"):
        add_sci("3")
    if c10.button("0"):
        add_sci("0")
    if c11.button("."):
        add_sci(".")
    if c12.button("exp("):
        add_sci("exp(")

    st.markdown("**Trigonometría e Hiperbólicas:**")
    t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.columns(9)
    if t1.button("sen("):
        add_sci("sin(")
    if t2.button("cos("):
        add_sci("cos(")
    if t3.button("tan("):
        add_sci("tan(")
    if t4.button("senh("):
        add_sci("sinh(")
    if t5.button("cosh("):
        add_sci("cosh(")
    if t6.button("tanh("):
        add_sci("tanh(")
    if t7.button("arcoseno("):
        add_sci("asin(")
    if t8.button("arcocoseno("):
        add_sci("acos(")
    if t9.button("arcotangente("):
        add_sci("atan(")

    st.markdown("**Potencias, Raíces, Logaritmos y Constantes:**")
    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 = st.columns(12)
    if p1.button("sqrt("):
        add_sci("sqrt(")
    if p2.button("raices cubicas("):
        add_sci("cbrt(")
    if p3.button("potencias"):
        add_sci("**")
    if p4.button("fracciones"):
        add_sci("/")
    if p5.button("!"):
        add_sci("factorial(")
    if p6.button("%"):
        add_sci("%")
    if p7.button("lg("):
        add_sci("log10(")
    if p8.button("ln("):
        add_sci("ln(")
    if p9.button("log("):
        add_sci("log(")
    if p10.button("π (pi)"):
        add_sci("pi")
    if p11.button("ℯ (euler)"):
        add_sci("e")
    if p12.button("x"):
        add_sci("x")

    v1, v2, v3 = st.columns(3)
    if v1.button("a"):
        add_sci("a")
    if v2.button("b"):
        add_sci("b")
    if v3.button("c"):
        add_sci("c")

    sci_input = st.text_input(
        "Expresión Científica de Alta Precisión:", key="sci_val"
    )

    if st.button(
        "🚀 Calcular Resultado con 30+ Decimales", type="primary"
    ):
        if not sci_input.strip():
            st.warning("Por favor, introduce alguna expresión para calcular.")
        else:
            try:
                safe_dict = {
                    "sin": mpmath.sin,
                    "cos": mpmath.cos,
                    "tan": mpmath.tan,
                    "sinh": mpmath.sinh,
                    "cosh": mpmath.cosh,
                    "tanh": mpmath.tanh,
                    "asin": mpmath.asin,
                    "acos": mpmath.acos,
                    "atan": mpmath.atan,
                    "sqrt": mpmath.sqrt,
                    "exp": mpmath.exp,
                    "cbrt": lambda val: mpmath.power(val, 1 / 3),
                    "factorial": mpmath.factorial,
                    "log10": mpmath.log10,
                    "ln": mpmath.ln,
                    "log": mpmath.log,
                    "pi": mpmath.pi,
                    "e": mpmath.e,
                    "x": 1,
                    "a": 1,
                    "b": 1,
                    "c": 1,
                    "__builtins__": None,
                }
                resultado_eval = eval(sci_input, safe_dict, {})
                res_sci = mpmath.nstr(resultado_eval, 30)
                st.success("¡Resultado calculado con éxito (30 decimales)!")
                st.code(res_sci, language="text")
            except Exception as e:
                st.error(f"Error en el cálculo: {e}")

elif modo == "Cálculo Simbólico, Derivadas/Integrales y Plano Cartesiano":
    st.subheader("∫ Motor Simbólico y Editor Dinámico del Plano Cartesiano")
    st.markdown(
        "Mueve los controles deslizantes o edita los parámetros para transformar el dibujo en tiempo real; la fórmula analítica se actualizará automáticamente."
    )

    col_param1, col_param2, col_param3, col_param4 = st.columns(4)
    with col_param1:
        coef_a = st.slider("Coeficiente a (Curvatura)", -5.0, 5.0, 1.0, 0.1)
    with col_param2:
        coef_b = st.slider("Coeficiente b (Pendiente)", -5.0, 5.0, 0.0, 0.1)
    with col_param3:
        coef_c = st.slider("Coeficiente c (Desplazamiento Y)", -10.0, 10.0, 0.0, 0.5)
    with col_param4:
        shift_x = st.slider("Desplazamiento X", -5.0, 5.0, 0.0, 0.5)

    func_input = f"{coef_a}*(x - {shift_x})**2 + {coef_b}*(x - {shift_x}) + {coef_c}"
    st.info(f"📌 **Fórmula Actualizada Automáticamente:** `f(x) = {func_input}`")

    x = sp.Symbol("x")

    try:
        expr = sp.sympify(func_input)
        st.markdown("---")
        st.subheader("📊 Resultados Analíticos")

        derivada = sp.diff(expr, x)
        integral = sp.integrate(expr, x)

        st.latex(f"f(x) = {sp.latex(expr)}")
        st.latex(f"\\frac{{d}}{{dx}} f(x) = {sp.latex(derivada)}")
        st.latex(f"\\int f(x) \\, dx = {sp.latex(integral)} + C")

        st.markdown("---")
        st.subheader("📈 Plano Cartesiano Dinámico e Interactivo")

        f_lambdified = sp.lambdify(x, expr, modules=["numpy"])
        x_vals = np.linspace(-15, 15, 500)
        y_vals = f_lambdified(x_vals)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="lines",
                name=f"f(x)",
                line=dict(color="#00ffcc", width=3.5),
            )
        )
        fig.update_layout(
            title="Plano Cartesiano con Actualización Dinámica de Fórmula",
            xaxis_title="Eje X",
            yaxis_title="Eje Y",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#161b22",
            font_color="white",
            xaxis=dict(
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="gray",
                gridcolor="#30363d",
            ),
            yaxis=dict(
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="gray",
                gridcolor="#30363d",
            ),
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al procesar la función dinámica: {e}")

elif modo == "Geometría Avanzada (GeoGebra)":
    st.subheader("📐 Entorno de Geometría Avanzada (GeoGebra en Pantalla Completa)")
    st.markdown(
        "Utiliza la herramienta interactiva de GeoGebra expandida al máximo para ocupar toda la pantalla."
    )

    geogebra_html = """
    <div style="width: 100%; height: 85vh; background-color: #161b22; border-radius: 10px; overflow: hidden; border: 1px solid #30363d;">
        <iframe src="https://www.geogebra.org/classic?embed" width="100%" height="100%" style="border:none;" allowfullscreen></iframe>
    </div>
    """
    st.components.v1.html(geogebra_html, height=750, scrolling=False)

else:
    st.subheader("📐 Resolución de Sistemas Lineales")
    matriz_txt = st.text_area("Matriz A (ej: 2,1 / 1,3):", value="2, 1\n1, 3")
    vector_txt = st.text_input("Vector B (ej: 5,5):", value="5, 5")
    if st.button("Resolver Sistema", type="primary"):
        try:
            A = np.array(
                [[float(n) for n in l.split(",")] for l in matriz_txt.split("\n")]
            )
            B = np.array([float(n) for n in vector_txt.split(",")])
            sol = np.linalg.solve(A, B)
            st.success("Solución del sistema:")
            st.write(sol)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Consola científica avanzada impulsada por Python y Streamlit.")
