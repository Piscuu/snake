import random
import time
import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Snake",
    page_icon="🐍",
    layout="centered",
)

BOARD_SIZE = 20
INITIAL_SPEED = 0.15
MIN_SPEED = 0.055


# ============================================================
# ESTADO DEL JUEGO
# ============================================================

def create_food(snake):
    available = [
        (x, y)
        for x in range(BOARD_SIZE)
        for y in range(BOARD_SIZE)
        if (x, y) not in snake
    ]

    return random.choice(available) if available else None


def reset_game():
    center = BOARD_SIZE // 2

    st.session_state.snake = [
        (center, center),
        (center - 1, center),
        (center - 2, center),
    ]

    st.session_state.direction = (1, 0)
    st.session_state.next_direction = (1, 0)
    st.session_state.food = create_food(st.session_state.snake)

    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.started = False
    st.session_state.paused = False
    st.session_state.last_update = time.time()


def initialize_state():
    if "snake" not in st.session_state:
        reset_game()


# ============================================================
# CONTROLES
# ============================================================

def change_direction(new_direction):
    current = st.session_state.direction

    # Evita girar directamente en sentido contrario.
    if (
        new_direction[0] == -current[0]
        and new_direction[1] == -current[1]
    ):
        return

    st.session_state.next_direction = new_direction


# ============================================================
# LÓGICA DEL JUEGO
# ============================================================

def update_game():
    if (
        st.session_state.game_over
        or not st.session_state.started
        or st.session_state.paused
    ):
        return

    st.session_state.direction = st.session_state.next_direction

    head_x, head_y = st.session_state.snake[0]
    dx, dy = st.session_state.direction

    new_head = (head_x + dx, head_y + dy)

    # Colisión con las paredes.
    if (
        new_head[0] < 0
        or new_head[0] >= BOARD_SIZE
        or new_head[1] < 0
        or new_head[1] >= BOARD_SIZE
    ):
        st.session_state.game_over = True
        return

    eating = new_head == st.session_state.food

    # La cola se mueve si no estamos comiendo.
    body_to_check = (
        st.session_state.snake
        if eating
        else st.session_state.snake[:-1]
    )

    # Colisión con el propio cuerpo.
    if new_head in body_to_check:
        st.session_state.game_over = True
        return

    new_snake = [new_head] + st.session_state.snake

    if eating:
        st.session_state.score += 1
        st.session_state.food = create_food(new_snake)
    else:
        new_snake.pop()

    st.session_state.snake = new_snake


def get_speed():
    speed = INITIAL_SPEED - (st.session_state.score * 0.005)
    return max(MIN_SPEED, speed)


# ============================================================
# TABLERO
# ============================================================

def render_board():
    snake = st.session_state.snake
    food = st.session_state.food

    cells = []

    for y in range(BOARD_SIZE):
        row = []

        for x in range(BOARD_SIZE):
            position = (x, y)

            if position == snake[0]:
                cell = "🟢"
            elif position in snake:
                cell = "🟩"
            elif position == food:
                cell = "🍎"
            else:
                cell = "⬛"

            row.append(cell)

        cells.append("".join(row))

    board = "\n".join(cells)

    st.markdown(
        f"""
        <div class="game-board">
            <pre>{board}</pre>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# JAVASCRIPT - CONTROLES WASD
# ============================================================

def keyboard_controls():
    components.html(
        """
        <script>
        document.addEventListener("keydown", function(event) {

            const key = event.key.toLowerCase();

            const allowedKeys = ["w", "a", "s", "d",
                                 "arrowup", "arrowdown",
                                 "arrowleft", "arrowright"];

            if (!allowedKeys.includes(key)) {
                return;
            }

            event.preventDefault();

            /*
             * Streamlit escucha los cambios de los botones.
             * Buscamos los botones de dirección por su texto.
             */
            const buttons = window.parent.document.querySelectorAll(
                'button'
            );

            let target = null;

            if (key === "w" || key === "arrowup") {
                target = "⬆️";
            }

            if (key === "a" || key === "arrowleft") {
                target = "⬅️";
            }

            if (key === "s" || key === "arrowdown") {
                target = "⬇️";
            }

            if (key === "d" || key === "arrowright") {
                target = "➡️";
            }

            if (target) {
                for (const button of buttons) {
                    if (button.innerText.includes(target)) {
                        button.click();
                        break;
                    }
                }
            }
        });
        </script>
        """,
        height=0,
    )


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0;
        }

        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 25px;
        }

        .game-board {
            background: #111827;
            border: 4px solid #374151;
            border-radius: 12px;
            padding: 12px;
            width: fit-content;
            margin: 20px auto;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .game-board pre {
            margin: 0;
            padding: 0;
            font-size: 17px;
            line-height: 1;
            letter-spacing: 0;
            font-family: monospace;
        }

        .instructions {
            text-align: center;
            color: #aaa;
            margin-top: 15px;
        }

        .game-over {
            text-align: center;
            color: #ef4444;
            font-size: 1.8rem;
            font-weight: bold;
        }

        .score {
            text-align: center;
            font-size: 1.5rem;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INICIALIZACIÓN
# ============================================================

initialize_state()

# Activar controles de teclado.
keyboard_controls()


# ============================================================
# INTERFAZ
# ============================================================

st.markdown(
    '<div class="main-title">🐍 Snake</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">La clásica viborita hecha con Python + Streamlit</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CONTROLES
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("⬆️", use_container_width=True):
        change_direction((0, -1))

with col2:
    if st.button("⬅️", use_container_width=True):
        change_direction((-1, 0))

with col3:
    if st.button("⏯️", use_container_width=True):
        if st.session_state.started:
            st.session_state.paused = not st.session_state.paused

with col4:
    if st.button("➡️", use_container_width=True):
        change_direction((1, 0))

with col5:
    if st.button("⬇️", use_container_width=True):
        change_direction((0, 1))


# ============================================================
# BOTONES PRINCIPALES
# ============================================================

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "▶️ Iniciar",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.started = True
        st.session_state.paused = False
        st.session_state.last_update = time.time()

with col2:
    if st.button(
        "🔄 Reiniciar",
        use_container_width=True,
    ):
        reset_game()


# ============================================================
# INFORMACIÓN
# ============================================================

st.markdown(
    f'<div class="score">🏆 Puntaje: {st.session_state.score}</div>',
    unsafe_allow_html=True,
)

if st.session_state.game_over:
    st.markdown(
        '<div class="game-over">💀 GAME OVER</div>',
        unsafe_allow_html=True,
    )

elif st.session_state.paused:
    st.info("⏸️ Juego pausado")

elif not st.session_state.started:
    st.info("Presioná ▶️ Iniciar para comenzar")


# ============================================================
# TABLERO
# ============================================================

render_board()

st.markdown(
    """
    <div class="instructions">
        ⌨️ <b>WASD</b> o las flechas para moverte.<br>
        🍎 Comé las manzanas para crecer y sumar puntos.<br>
        💥 No choques contra las paredes ni contra tu propio cuerpo.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOOP DEL JUEGO
# ============================================================

if (
    st.session_state.started
    and not st.session_state.game_over
    and not st.session_state.paused
):
    current_time = time.time()
    elapsed = current_time - st.session_state.last_update

    if elapsed >= get_speed():
        update_game()
        st.session_state.last_update = current_time
        st.rerun()

    else:
        time.sleep(0.01)
        st.rerun()
