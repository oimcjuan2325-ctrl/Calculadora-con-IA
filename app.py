import mpmath
import numpy as np
import streamlit as st
import sympy as sp
from google import genai

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

# Inicializar estados globales de la aplicación
if "lang" not in st.session_state:
    st.session_state.lang = "Español"
if "sci_val" not in st.session_state:
    st.session_state.sci_val = ""
if "last_result" not in st.session_state:
    st.session_state.last_result = "Ningún cálculo realizado todavía."

# Sistema de gestión de múltiples chats en la IA
if "conversations" not in st.session_state:
    st.session_state.conversations = {
        "Chat Principal": []
    }
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat Principal"

# Diccionario de traducciones para la interfaz
t = {
    "Español": {
        "title": "🧮 Consola Científica de Precisión & Motor Simbólico",
        "subtitle": "Sistema de cálculo avanzado con símbolos LaTeX, GeoGebra y Asistente IA multilingüe.",
        "settings_header": "⚙️ Ajustes de la App",
        "lang_label": "Idioma / Hizkuntza",
        "save_btn": "Guardar ajustes",
        "mode_label": "Modo de Operación:",
        "modes": [
            "Calculadora Científica Interactiva",
            "Geometría Avanzada (GeoGebra)",
            "Resolución de Sistemas Lineales",
        ],
        "ai_header": "🤖 Asistente Matemático IA",
        "ai_desc": "Gestiona tus conversaciones y pregunta sobre lo que hay en pantalla:",
        "new_chat_name": "Nombre del nuevo chat:",
        "create_chat_btn": "➕ Crear Nuevo Chat",
        "select_chat": "Conversación activa:",
        "rename_chat_input": "Renombrar chat actual:",
        "rename_btn": "✏️ Cambiar Nombre",
        "ai_placeholder": "Ej: ¿Por qué da error esto?",
        "ai_btn": "Preguntar a la IA",
        "calc_sub": "🔢 Calculadora Científica Interactiva & Símbolos Matemáticos",
        "calc_desc": "Usa el teclado virtual. Las expresiones se renderizan automáticamente con notación matemática formal.",
        "keyboard": "⌨️ Teclado Científico Unificado:",
        "clear": "🗑️ Borrar",
        "trig": "Trigonometría e Hiperbólicas:",
        "powers": "Potencias, Raíces, Logaritmos y Constantes:",
        "input_label": "Expresión Científica:",
        "calc_btn": "🚀 Calcular Expresión y Mostrar Símbolos",
        "warning_empty": "Por favor, introduce alguna expresión para calcular.",
        "success_calc": "¡Expresión evaluada con éxito!",
        "symbolic_label": "✨ Representación Matemática Formal (LaTeX):",
        "geo_sub": "📐 Entorno de Geometría Avanzada (GeoGebra en Pantalla Completa)",
        "geo_desc": "Utiliza la herramienta interactiva de GeoGebra expandida al máximo para ocupar toda la pantalla.",
        "sys_sub": "📐 Resolución de Sistemas Lineales",
        "matrix_label": "Matriz A (ej: 2,1 / 1,3):",
        "vector_label": "Vector B (ej: 5,5):",
        "solve_btn": "Resolver Sistema",
        "sys_success": "Solución del sistema:",
        "footer": "Consola científica avanzada impulsada por Python, Streamlit, SymPy y Google Gemini.",
    },
    "Euskera": {
        "title": "🧮 Doitasun Handiko Kontsola Zientifikoa & Motor Sinbolikoa",
        "subtitle": "Kalkulu sistema aurreratua ikur LaTeX-ekin, GeoGebratekin eta hizkuntza anitzeko IA Laguntzailearekin.",
        "settings_header": "⚙️ Aplikazioaren Ezarpenak",
        "lang_label": "Idioma / Hizkuntza",
        "save_btn": "Gorde ezarpenak",
        "mode_label": "Eragiketa Modua:",
        "modes": [
            "Kalkulagailu Zientifiko Interaktiboa",
            "Geometria Aurreratua (GeoGebra)",
            "Sistema Linealen Ebazpena",
        ],
        "ai_header": "🤖 IA Laguntzaile Matematikoa",
        "ai_desc": "Kudeatu zure elkarrizketak eta galdetu pantailan daukazunari buruz:",
        "new_chat_name": "Txat berriaren izena:",
        "create_chat_btn": "➕ Sortu Txat Berria",
        "select_chat": "Elkarrizketa aktiboa:",
        "rename_chat_input": "Aldatu uneko txataren izena:",
        "rename_btn": "✏️ Aldatu Izena",
        "ai_placeholder": "Adib: Zergatik ematen du akats hau?",
        "ai_btn": "IArif galdetu",
        "calc_sub": "🔢 Kalkulagailu Zientifiko Interaktiboa & Ikur Matematikoak",
        "calc_desc": "Erabili teklatu birtuala. Adierazpenak modu formalean marrazten dira pantailan.",
        "keyboard": "⌨️ Teklatu Zientifiko Bateratua:",
        "clear": "🗑️ Garbitu",
        "trig": "Trigonometria eta Hiperbolikoak:",
        "powers": "Berreketak, Erraiak, Logaritmoak eta Konstanteak:",
        "input_label": "Adierazpen Zientifikoa:",
        "calc_btn": "🚀 Kalkulatu Adierazpena eta Erakutsi Ikurrak",
        "warning_empty": "Mesedez, sartu adierazpen bat kalkulatzeko.",
        "success_calc": "Adierazpena arrakastaz ebaluatuta!",
        "symbolic_label": "✨ Matematika Erakustaldia (LaTeX formatuan):",
        "geo_sub": "📐 Geometria Aurreratuaren Ingurunea (GeoGebra Pantaila Osoan)",
        "geo_desc": "Erabili GeoGebraten tresna interaktiboa pantaila osoa betetzeko zabalduta.",
        "sys_sub": "📐 Sistema Linealen Ebazpena",
        "matrix_label": "A Matrizea (adib: 2,1 / 1,3):",
        "vector_label": "B Bektorea (adib: 5,5):",
        "solve_btn": "Sistema Ebatzi",
        "sys_success": "Sistemaren soluzioa:",
        "footer": "Kontsola zientifiko aurreratua Python, Streamlit, SymPy eta Google Geminik bultzatuta.",
    },
}

lang_texts = t[st.session_state.lang]

# ==========================================
# BARRA LATERAL
# ==========================================
with st.sidebar:
    # 1. BOTÓN DE AJUSTES (ARRIBA)
    with st.expander(lang_texts["settings_header"], expanded=False):
        selected_lang = st.selectbox(
            lang_texts["lang_label"],
            ["Español", "Euskera"],
            index=0 if st.session_state.lang == "Español" else 1,
        )
        if st.button(lang_texts["save_btn"]):
            st.session_state.lang = selected_lang
            st.rerun()

    st.markdown("---")

    # 2. SELECTOR DE MODOS DE LA CALCULADORA
    modo = st.selectbox(lang_texts["mode_label"], lang_texts["modes"])

    st.markdown("---")

    # 3. ASISTENTE DE IA MATEMÁTICA CON GESTIÓN DE CHATS
    st.subheader(lang_texts["ai_header"])
    st.markdown(lang_texts["ai_desc"])

    chat_names = list(st.session_state.conversations.keys())
    selected_chat = st.selectbox(
        lang_texts["select_chat"],
        chat_names,
        index=chat_names.index(st.session_state.current_chat)
        if st.session_state.current_chat in chat_names
        else 0,
    )
    if selected_chat != st.session_state.current_chat:
        st.session_state.current_chat = selected_chat
        st.rerun()

    with st.expander("⚙️ Opciones de Conversación"):
        new_chat_title = st.text_input(lang_texts["new_chat_name"], value="")
        if st.button(lang_texts["create_chat_btn"]):
            if new_chat_title.strip() and new_chat_title not in st.session_state.conversations:
                st.session_state.conversations[new_chat_title] = []
                st.session_state.current_chat = new_chat_title
                st.rerun()

        rename_title = st.text_input(
            lang_texts["rename_chat_input"], value=st.session_state.current_chat
        )
        if st.button(lang_texts["rename_btn"]):
            if rename_title.strip() and rename_title not in st.session_state.conversations:
                st.session_state.conversations[rename_title] = st.session_state.conversations.pop(
                    st.session_state.current_chat
                )
                st.session_state.current_chat = rename_title
                st.rerun()

    st.markdown("---")

    current_messages = st.session_state.conversations[st.session_state.current_chat]
    for msg in current_messages[-2:]:
        if msg["role"] == "user":
            st.markdown(f"**Tú / Zu:** {msg['content']}")
        else:
            st.markdown(f"**IA:** {msg['content']}")

    user_query = st.text_input(
        "Duda / Zalantza:",
        key="ai_quick_query",
        placeholder=lang_texts["ai_placeholder"],
    )

    if st.button(lang_texts["ai_btn"]):
        if user_query.strip():
            try:
                api_key = st.secrets.get("GEMINI_API_KEY", "")
                if not api_key:
                    st.error("Falta configurar GEMINI_API_KEY en st.secrets.")
                else:
                    client = genai.Client(api_key=api_key)
                    contexto_pantalla = st.session_state.get(
                        "last_result", "Sin datos"
                    )

                    system_prompt = (
                        f"Eres un profesor experto en matemáticas. Responde SIEMPRE en el idioma: {st.session_state.lang}. "
                        "Analiza el contexto actual de la pantalla del usuario y responde de forma concisa y directa "
                        "a su duda sobre si hay errores, conceptos o el significado matemático de lo que está viendo.\n\n"
                        f"Contexto de la pantalla actual: {contexto_pantalla}\n"
                        f"Pregunta del usuario: {user_query}"
                    )

                    response = client.models.generate_content(
                        model="gemini-3.6-flash", contents=system_prompt
                    )
                    respuesta_ia = response.text

                    st.session_state.conversations[
                        st.session_state.current_chat
                    ].append({"role": "user", "content": user_query})
                    st.session_state.conversations[
                        st.session_state.current_chat
                    ].append({"role": "assistant", "content": respuesta_ia})
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# CONTENIDO PRINCIPAL DE LA PÁGINA
# ==========================================
st.title(lang_texts["title"])
st.markdown(lang_texts["subtitle"])
st.markdown("---")

modo_actual = modo
if (
    modo_actual == "Kalkulagailu Zientifiko Interaktiboa"
    or modo_actual == "Calculadora Científica Interactiva"
):
    st.subheader(lang_texts["calc_sub"])
    st.markdown(lang_texts["calc_desc"])


    def add_sci(val):
        st.session_state.sci_val += val


    st.markdown(lang_texts["keyboard"])

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
    if b7.button(lang_texts["clear"]):
        st.session_state.sci_val = ""
        st.session_state.last_result = (
            "Limpiado." if st.session_state.lang == "Español" else "Garbituta."
        )

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

    st.markdown(lang_texts["trig"])
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

    st.markdown(lang_texts["powers"])
    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 = st.columns(12)
    if p1.button("sqrt("):
        add_sci("sqrt(")
    if p2.button("cbrt("):
        add_sci("cbrt(")
    if p3.button("**"):
        add_sci("**")
    if p4.button("/"):
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
    if p10.button("π"):
        add_sci("pi")
    if p11.button("ℯ"):
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

    sci_input = st.text_input(lang_texts["input_label"], key="sci_val")

    if st.button(lang_texts["calc_btn"], type="primary"):
        if not sci_input.strip():
            st.warning(lang_texts["warning_empty"])
        else:
            try:
                # 1. Cálculo numérico de ultra-precisión con mpmath
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

                st.session_state.last_result = (
                    f"Expresión: {sci_input} | Resultado: {res_sci}"
                )
                st.success(lang_texts["success_calc"])

                # Mostrar resultado numérico exacto de 30 decimales
                st.code(res_sci, language="text")

                # 2. Renderizado de símbolos matemáticos reales mediante SymPy (LaTeX)
                st.markdown(lang_texts["symbolic_label"])
                
                # Traducir sintaxis común para SymPy
                expr_sympy_str = (
                    sci_input.replace("ln(", "log(")
                    .replace("log10(", "log(..., 10)")
                    .replace("cbrt(", "(...)**(1/3)")
                )
                
                expr_simbolica = sp.sympify(expr_sympy_str, evaluate=False)
                st.latex(sp.latex(expr_simbolica))

            except Exception as e:
                st.session_state.last_result = (
                    f"Expresión: {sci_input} | Error: {e}"
                )
                st.error(f"Error: {e}")

elif (
    modo_actual == "Geometria Aurreratua (GeoGebra)"
    or modo_actual == "Geometría Avanzada (GeoGebra)"
):
    st.subheader(lang_texts["geo_sub"])
    st.markdown(lang_texts["geo_desc"])
    st.session_state.last_result = (
        "El usuario interactúa con GeoGebra."
        if st.session_state.lang == "Español"
        else "Erabiltzailea GeoGebraten ari da."
    )

    geogebra_html = """
    <div style="width: 100%; height: 85vh; background-color: #161b22; border-radius: 10px; overflow: hidden; border: 1px solid #30363d;">
        <iframe src="https://www.geogebra.org/classic?embed" width="100%" height="100%" style="border:none;" allowfullscreen></iframe>
    </div>
    """
    st.components.v1.html(geogebra_html, height=750, scrolling=False)

else:
    st.subheader(lang_texts["sys_sub"])
    matriz_txt = st.text_area(lang_texts["matrix_label"], value="2, 1\n1, 3")
    vector_txt = st.text_input(lang_texts["vector_label"], value="5, 5")
    if st.button(lang_texts["solve_btn"], type="primary"):
        try:
            A = np.array(
                [[float(n) for n in l.split(",")] for l in matriz_txt.split("\n")]
            )
            B = np.array([float(n) for n in vector_txt.split(",")])
            sol = np.linalg.solve(A, B)
            st.session_state.last_result = (
                f"Matriz A:\n{matriz_txt}\nVector B: {vector_txt}\nSolución: {sol}"
            )
            st.success(lang_texts["sys_success"])
            st.write(sol)
        except Exception as e:
            st.session_state.last_result = f"Error: {e}"
            st.error(f"Error: {e}")

st.markdown("---")
st.caption(lang_texts["footer"])
