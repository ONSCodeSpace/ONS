"""Calculator — Streamlit App

Run: streamlit run calendar_pro.py
"""

import ast
import operator
from html import escape
from decimal import Decimal, DivisionByZero, InvalidOperation, getcontext

import streamlit as st

getcontext().prec = 28

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

BUTTON_ROWS = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["±", "0", ".", "="],
]

DISPLAY_REPLACEMENTS = {
    "×": "*",
    "÷": "/",
    "−": "-",
    "^": "**",
}


def normalize_expression(expression: str) -> str:
    """Translate friendly calculator symbols to Python arithmetic symbols."""
    normalized = expression.strip()
    for visible_symbol, python_symbol in DISPLAY_REPLACEMENTS.items():
        normalized = normalized.replace(visible_symbol, python_symbol)
    return normalized


def format_decimal(value: Decimal) -> str:
    """Format calculator results without unnecessary trailing zeros."""
    if value == value.to_integral_value():
        return str(value.quantize(Decimal(1)))

    formatted = format(value.normalize(), "f")
    return formatted.rstrip("0").rstrip(".")


def evaluate_node(node: ast.AST) -> Decimal:
    """Evaluate a restricted arithmetic AST using Decimal numbers."""
    if isinstance(node, ast.Expression):
        return evaluate_node(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return Decimal(str(node.value))

    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
        operand = evaluate_node(node.operand)
        return UNARY_OPERATORS[type(node.op)](operand)

    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 12:
            raise ValueError("Exponent is too large")
        return BINARY_OPERATORS[type(node.op)](left, right)

    raise ValueError("Use numbers and arithmetic operators only")


def calculate(expression: str) -> str:
    """Calculate a safe arithmetic expression and return a display string."""
    normalized = normalize_expression(expression)
    if not normalized:
        return "0"

    try:
        tree = ast.parse(normalized, mode="eval")
        result = evaluate_node(tree)
    except (DivisionByZero, ZeroDivisionError):
        raise ValueError("Cannot divide by zero") from None
    except (InvalidOperation, OverflowError):
        raise ValueError("Result is too large") from None
    except SyntaxError:
        raise ValueError("Enter a complete expression") from None

    return format_decimal(result)


def append_token(token: str) -> None:
    """Append a calculator token to the expression in session state."""
    if st.session_state.just_calculated and token not in {"+", "−", "×", "÷", "%"}:
        st.session_state.expression = ""
    st.session_state.just_calculated = False
    st.session_state.expression += token


def toggle_sign() -> None:
    """Toggle the sign of the full expression/result where possible."""
    expression = st.session_state.expression.strip()
    if not expression:
        st.session_state.expression = "-"
    elif expression.startswith("-"):
        st.session_state.expression = expression[1:]
    else:
        st.session_state.expression = f"-({expression})"
    st.session_state.just_calculated = False


def handle_button(label: str) -> None:
    """Update calculator state for a pressed calculator button."""
    if label == "C":
        st.session_state.expression = ""
        st.session_state.result = "0"
        st.session_state.error = ""
        st.session_state.just_calculated = False
        return

    if label == "⌫":
        st.session_state.expression = st.session_state.expression[:-1]
        st.session_state.error = ""
        st.session_state.just_calculated = False
        return

    if label == "±":
        toggle_sign()
        st.session_state.error = ""
        return

    if label == "=":
        try:
            st.session_state.result = calculate(st.session_state.expression)
            st.session_state.expression = st.session_state.result
            st.session_state.error = ""
            st.session_state.just_calculated = True
        except ValueError as error:
            st.session_state.error = str(error)
        return

    append_token(label)
    st.session_state.error = ""


def initialize_state() -> None:
    """Create calculator session-state defaults."""
    st.session_state.setdefault("expression", "")
    st.session_state.setdefault("result", "0")
    st.session_state.setdefault("error", "")
    st.session_state.setdefault("just_calculated", False)


def render_calculator() -> None:
    """Render the Streamlit calculator interface."""
    initialize_state()

    st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

    st.markdown(
        """
        <style>
            #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(108, 92, 231, 0.20), transparent 32rem),
                    linear-gradient(135deg, #101828 0%, #182230 100%);
                color: #f8fafc;
            }
            .block-container { max-width: 34rem; padding-top: 3rem; }
            .calculator-shell {
                background: rgba(15, 23, 42, 0.86);
                border: 1px solid rgba(148, 163, 184, 0.24);
                border-radius: 28px;
                box-shadow: 0 30px 80px rgba(0, 0, 0, 0.35);
                padding: 1.4rem;
            }
            .calculator-title {
                color: #c4b5fd;
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.18em;
                margin-bottom: 1rem;
                text-transform: uppercase;
            }
            .calculator-display {
                background: #020617;
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: 22px;
                margin-bottom: 1rem;
                min-height: 8rem;
                padding: 1rem;
                text-align: right;
            }
            .expression {
                color: #94a3b8;
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                font-size: 1rem;
                min-height: 1.4rem;
                overflow-wrap: anywhere;
            }
            .result {
                color: #f8fafc;
                font-size: 3rem;
                font-weight: 800;
                line-height: 1.1;
                margin-top: 0.55rem;
                overflow-wrap: anywhere;
            }
            .error {
                color: #fca5a5;
                font-size: 0.9rem;
                min-height: 1.3rem;
                padding: 0.1rem 0 0.6rem;
                text-align: right;
            }
            .stButton > button {
                background: rgba(30, 41, 59, 0.95);
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 18px;
                color: #f8fafc;
                font-size: 1.35rem;
                font-weight: 750;
                height: 4.2rem;
                transition: transform 120ms ease, background 120ms ease, border-color 120ms ease;
                width: 100%;
            }
            .stButton > button:hover {
                background: #334155;
                border-color: rgba(196, 181, 253, 0.65);
                color: #ffffff;
                transform: translateY(-1px);
            }
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #8b5cf6, #6366f1);
                border-color: transparent;
                color: #ffffff;
            }
            .stTextInput input {
                background: #020617;
                border: 1px solid rgba(148, 163, 184, 0.24);
                border-radius: 14px;
                color: #f8fafc;
                font-size: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="calculator-shell">', unsafe_allow_html=True)
    st.markdown('<div class="calculator-title">Smart Calculator</div>', unsafe_allow_html=True)

    typed_expression = st.text_input(
        "Type an expression",
        value=st.session_state.expression,
        placeholder="Example: (12 + 8) ÷ 4",
        label_visibility="collapsed",
    )
    if typed_expression != st.session_state.expression:
        st.session_state.expression = typed_expression
        st.session_state.just_calculated = False

    expression = escape(st.session_state.expression or "Ready")
    result = escape(st.session_state.result)
    error = escape(st.session_state.error)
    st.markdown(
        f"""
        <div class="calculator-display">
            <div class="expression">{expression}</div>
            <div class="result">{result}</div>
        </div>
        <div class="error">{error}</div>
        """,
        unsafe_allow_html=True,
    )

    for row_index, row in enumerate(BUTTON_ROWS):
        columns = st.columns(4, gap="small")
        for column, label in zip(columns, row):
            with column:
                is_primary = label in {"÷", "×", "−", "+", "="}
                if st.button(
                    label,
                    key=f"button-{row_index}-{label}",
                    type="primary" if is_primary else "secondary",
                    use_container_width=True,
                ):
                    handle_button(label)
                    st.rerun()

    st.caption("Supports +, −, ×, ÷, %, parentheses, decimals, and typed expressions.")
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render_calculator()
