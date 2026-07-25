from pathlib import Path
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Streaming adaptativo — Análisis ABR",
    #page_icon="▶️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PLOTLY_TEMPLATE = "plotly_white"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"

st.markdown("""
<style>
.block-container{padding-top:1.4rem;padding-bottom:3rem;max-width:1450px}
#MainMenu{visibility:hidden} footer{visibility:hidden}
.hero-shell{padding:2.2rem 2.4rem;border:1px solid rgba(21,101,192,.15);border-radius:26px;background:radial-gradient(circle at 92% 8%,rgba(21,101,192,.15),transparent 30%),linear-gradient(135deg,#fff 0%,#f5f9ff 100%);box-shadow:0 18px 45px rgba(31,41,55,.08);margin-bottom:1.4rem}
.eyebrow{display:inline-block;padding:.42rem .78rem;border-radius:999px;background:#e8f1fc;color:#0d47a1;font-size:.82rem;font-weight:750;letter-spacing:.08em;text-transform:uppercase;margin-bottom:1rem}
.hero-title{font-size:clamp(2.25rem,5vw,4.3rem);line-height:1.02;letter-spacing:-.045em;font-weight:850;color:#102a43;margin:0 0 1rem 0}
.hero-copy{
    font-size:1.30rem !important;
    line-height:1.8;
    color:#486581;
    max-width:760px;
    margin-bottom:.8rem;
}
.hook{
    font-size:1.55rem !important;
    line-height:1.6;
    font-weight:700;
    color:#102A43;
    margin:.5rem 0 1.2rem 0;
}
.meme-frame{border-radius:22px;overflow:hidden;border:1px solid rgba(21,101,192,.15);box-shadow:0 16px 36px rgba(16,42,67,.14);background:#fff;padding:.65rem}
.meme-caption{
    text-align:center;
    font-size:1.18rem !important;
    color:#627d98;
    margin-top:.8rem;
    line-height:1.6;
    font-style:italic;
    font-weight:500;
}
.value-card{
    min-height:230px;
    padding:1.7rem 1.8rem;
    border-radius:20px;
    background:#fff;
    border:1px solid #e6eef7;
    box-shadow:0 8px 24px rgba(31,41,55,.055);
}
.card-icon{
    font-size:2.1rem !important;
    margin-bottom:.75rem;
}

.card-title{
    color:#163a5f;
    font-size:1.30rem !important;
    font-weight:800;
    margin-bottom:.75rem;
    line-height:1.25;
}

.card-copy{
    color:#5c7083;
    font-size:1.12rem !important;
    line-height:1.75;
}
.vision-box{margin-top:1.35rem;padding:1.45rem 1.6rem;border-radius:20px;background:linear-gradient(120deg,#0d47a1 0%,#1565c0 65%,#1976d2 100%);color:#fff;box-shadow:0 14px 34px rgba(13,71,161,.20)}
.vision-title{font-size:1.6rem;font-weight:800;margin-bottom:.55rem}.vision-copy{font-size:1.3rem;line-height:1.62;opacity:.96}
.flow{display:flex;align-items:stretch;gap:.55rem;flex-wrap:wrap;margin:1.2rem 0 .5rem}.flow-step{flex:1 1 145px;padding:1.2rem .8rem;text-align:center;border-radius:15px;border:1px solid #dce8f5;background:#fff;color:#244a6b;font-weight:800;line-height:1.3}.flow-arrow{display:flex;align-items:center;justify-content:center;color:#1565c0;font-size:1.35rem;font-weight:800}
.section-heading{margin-top:2rem;margin-bottom:1rem;color:#102a43;font-size:1.8rem;font-weight:820}
div.stButton>button{min-height:3.2rem;border-radius:14px;font-size:1.05rem;font-weight:780;border:0;transition:transform .15s ease,box-shadow .15s ease}
div.stButton>button[kind="primary"]{background:linear-gradient(90deg,#0d47a1,#1976d2);color:#fff;box-shadow:0 10px 24px rgba(21,101,192,.24)}
div.stButton>button:hover{transform:translateY(-1px)}
[data-testid="stMetric"]{background:#fff;border:1px solid #e6eef7;padding:1rem;border-radius:15px;box-shadow:0 5px 16px rgba(31,41,55,.045)}
@media(max-width:850px){.hero-shell{padding:1.4rem}.hero-title{font-size:2.4rem}.flow-arrow{display:none}}
</style>
""",unsafe_allow_html=True)


def show_landing_page():
    hero_text, hero_image = st.columns([1.35, 0.75], gap="large")
    with hero_text:
        st.markdown("""
        <div class="hero-shell">
          <div class="eyebrow">Análisis visual · Streaming adaptativo</div>
          <h1 class="hero-title">Cuando el streaming se detiene,<br>la experiencia también</h1>
          <p class="hook">Una transmisión en vivo, una película, una serie o una clase virtual: basta un instante de carga para perder la atención del usuario.</p>
          <p class="hero-copy">Detrás de cada segundo de reproducción, un algoritmo de <strong>Adaptive Bitrate (ABR)</strong> decide continuamente si mantiene la calidad, reduce la resolución o protege el buffer para evitar una interrupción.</p>
        </div>
        """,unsafe_allow_html=True)
    with hero_image:
        st.markdown('<div class="meme-frame">',unsafe_allow_html=True)
        st.image(ASSETS_DIR / "buffering_cat.png",use_container_width=True)
        st.markdown('<div class="meme-caption">«Solo quería ver los partidos de la FIFA sin que apareciera el círculo de carga»</div></div>',unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Del problema visible a la decisión inteligente</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3,gap="large")
    cards=[
      (c1,'👤','Impacto en el usuario','Las pausas, el rebuffering y las caídas de resolución afectan directamente la percepción de calidad y la continuidad de la experiencia de streaming.'),
      (c2,'⚙️','Decisiones ABR','La decisión sobre el siguiente segmento no depende de una única métrica, sino de la interacción entre múltiples variables que describen el estado de la red y de la reproducción.'),
      (c3,'📊','Valor del análisis visual','Explorar estas relaciones permite detectar patrones de degradación, comprender la respuesta del algoritmo e identificar señales relevantes para un modelo predictivo.')
    ]
    for col,icon,title,copy in cards:
        with col:
            st.markdown(f'<div class="value-card"><div class="card-icon">{icon}</div><div class="card-title">{title}</div><div class="card-copy">{copy}</div></div>',unsafe_allow_html=True)

    st.markdown("""
    <div class="vision-box"><div class="vision-title">Visión del proyecto</div><div class="vision-copy">Este dashboard es la etapa exploratoria de una investigación más amplia: desarrollar una arquitectura basada en <strong>Transformers</strong> que utilice la secuencia reciente de métricas de red y reproducción para <strong>predecir la decisión de bitrate o resolución del siguiente segmento de video</strong>.</div></div>
    <div class="flow">
      <div class="flow-step">Datos reales de streaming</div><div class="flow-arrow">→</div>
      <div class="flow-step">Exploración visual</div><div class="flow-arrow">→</div>
      <div class="flow-step">Variables y patrones relevantes</div><div class="flow-arrow">→</div>
      <div class="flow-step">Arquitectura Transformer</div><div class="flow-arrow">→</div>
      <div class="flow-step">Predicción del siguiente segmento</div>
    </div>
    """,unsafe_allow_html=True)
    st.write("")
    _,button_col,_=st.columns([1,1.25,1])
    with button_col:
        if st.button("Explorar el dashboard  →",type="primary",use_container_width=True):
            st.session_state["show_dashboard"]=True
            st.rerun()
    st.caption("Datos: Stanford Puffer · Análisis de condiciones de red, buffer, calidad y cambios de resolución.")


def show_dashboard_navigation():
    return option_menu(menu_title=None,options=["Resumen","Evolución temporal","Condiciones de red","Cambios de calidad"],icons=["bar-chart","graph-up","scatter-chart","arrow-repeat","table"],orientation="horizontal",styles={"container":{"padding":"0!important","background-color":"white","border-radius":"14px","border":"1px solid #E6EEF7"},"nav-link":{"font-size":"17px","font-weight":"650","text-align":"center","margin":"0px","--hover-color":"#EAF3FD"},"nav-link-selected":{"background-color":"#1565C0","color":"white"}})

PLOTLY_TEMPLATE = "plotly_white"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "output"


@st.cache_data(show_spinner="Cargando datos...")
def load_data():
    segments = pd.read_parquet(DATA_DIR / "puffer_segments_dashboard.parquet")
    streams = pd.read_parquet(DATA_DIR / "puffer_stream_summary.parquet")
    events = pd.read_parquet(DATA_DIR / "puffer_client_events.parquet")
    ladder = pd.read_parquet(DATA_DIR / "puffer_bitrate_ladder.parquet")

    for column in ["datetime_utc", "ack_datetime_utc"]:
        if column in segments.columns:
            segments[column] = pd.to_datetime(
                segments[column], utc=True, errors="coerce"
            )

    return segments, streams, events, ladder


def ordered_resolutions(data):
    return (
        data[["resolution", "height"]]
        .dropna()
        .drop_duplicates()
        .sort_values("height")["resolution"]
        .astype(str)
        .tolist()
    )


def filter_data(data, channels, experiments, resolutions, streams):
    filtered = data.copy()

    if channels:
        filtered = filtered[filtered["channel"].isin(channels)]

    if experiments:
        filtered = filtered[filtered["expt_id"].isin(experiments)]

    if resolutions:
        filtered = filtered[filtered["resolution"].isin(resolutions)]

    if streams:
        filtered = filtered[filtered["stream_id"].isin(streams)]

    return filtered


def create_resolution_distribution(data):
    counts = (
        data.dropna(subset=["resolution", "height"])
        .groupby(["height", "resolution"], as_index=False, observed=True)
        .size()
        .rename(columns={"size": "segmentos"})
        .sort_values("height")
    )

    counts["porcentaje"] = counts["segmentos"] / counts["segmentos"].sum() * 100

    fig = px.bar(
        counts,
        x="resolution",
        y="segmentos",
        text=counts["porcentaje"].map(lambda value: f"{value:.1f}%"),
        labels={
            "resolution": "Resolución",
            "segmentos": "Número de segmentos",
        },
        title="Distribución de resoluciones seleccionadas",
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=460, showlegend=False)
    return fig


def create_network_scatter(data, max_points=20000):
    plot_data = data.dropna(
        subset=["delivery_rate_mbps", "rtt_ms", "resolution", "height"]
    ).copy()

    if len(plot_data) > max_points:
        plot_data = plot_data.sample(max_points, random_state=42)

    fig = px.scatter(
        plot_data,
        x="delivery_rate_mbps",
        y="rtt_ms",
        color="resolution",
        category_orders={"resolution": ordered_resolutions(plot_data)},
        opacity=0.5,
        hover_data={
            "stream_label": True,
            "channel": True,
            "segment_number": True,
            "buffer": ":.3f",
            "ssim_index": ":.4f",
            "delivery_rate_mbps": ":.3f",
            "rtt_ms": ":.3f",
        },
        labels={
            "delivery_rate_mbps": "Tasa de entrega (Mbps)",
            "rtt_ms": "RTT (ms)",
            "resolution": "Resolución",
        },
        title="Condiciones de red y resolución seleccionada",
        template=PLOTLY_TEMPLATE,
        render_mode="webgl",
    )
    fig.update_layout(height=560)
    return fig


def create_boxplot(data, variable, label, log_scale=False):
    plot_data = data.dropna(subset=["resolution", "height", variable]).copy()

    fig = px.box(
        plot_data,
        x="resolution",
        y=variable,
        color="resolution",
        category_orders={"resolution": ordered_resolutions(plot_data)},
        points="outliers",
        labels={"resolution": "Resolución", variable: label},
        title=f"Distribución de {label} por resolución",
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(height=520, showlegend=False)

    if log_scale:
        fig.update_yaxes(type="log")

    return fig


def create_correlation_heatmap(data):
    """
    Crea una matriz de correlación de Spearman organizada
    según el flujo lógico del análisis ABR.
    """

    # ---------------------------------------------------------
    # Orden narrativo de las variables
    # 1. Condiciones de red
    # 2. Estado de reproducción
    # 3. Características del segmento y calidad
    # ---------------------------------------------------------
    variable_order = [
        # Condiciones de red
        "delivery_rate_mbps",
        "rtt_ms",
        "min_rtt_ms",
        "cwnd",
        "in_flight",

        # Estado de reproducción
        "buffer",
        "cum_rebuf",
        "ack_delay_seconds",

        # Contenido y calidad seleccionada
        "size_mb",
        "ssim_index",
        "height",
    ]

    variable_labels = {
        "delivery_rate_mbps": "Throughput",
        "rtt_ms": "RTT",
        "min_rtt_ms": "RTT mínimo",
        "cwnd": "CWND",
        "in_flight": "In-flight",
        "buffer": "Buffer",
        "cum_rebuf": "Rebuffer acumulado",
        "ack_delay_seconds": "Retardo ACK",
        "size_mb": "Tamaño",
        "ssim_index": "SSIM",
        "height": "Altura resolución",
    }

    # Usar únicamente columnas existentes y con datos
    available = [
        column
        for column in variable_order
        if column in data.columns
        and data[column].notna().any()
    ]

    if len(available) < 2:
        fig = go.Figure()
        fig.update_layout(
            title="No existen suficientes variables para calcular correlaciones",
            template=PLOTLY_TEMPLATE,
            height=600,
        )
        return fig

    # ---------------------------------------------------------
    # Correlación Spearman
    # ---------------------------------------------------------
    corr = data[available].corr(method="spearman")

    # Mantener explícitamente el orden definido
    corr = corr.loc[available, available]

    # Cambiar los nombres técnicos por nombres legibles
    corr = corr.rename(
        index=variable_labels,
        columns=variable_labels,
    )

    # ---------------------------------------------------------
    # Heatmap con escala divergente centrada en cero
    # Azul = negativa
    # Blanco = cercana a cero
    # Rojo = positiva
    # ---------------------------------------------------------
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        zmin=-1,
        zmax=1,
        color_continuous_midpoint=0,
        color_continuous_scale=[
            [0.00, "#2166AC"],
            [0.25, "#67A9CF"],
            [0.50, "#F7F7F7"],
            [0.75, "#EF8A62"],
            [1.00, "#B2182B"],
        ],
        labels={
            "color": "Correlación de Spearman",
        },
        title="Matriz de correlación entre variables ABR",
        template=PLOTLY_TEMPLATE,
    )

    # ---------------------------------------------------------
    # Mejorar contraste de los valores dentro de las celdas
    # ---------------------------------------------------------
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b> vs. <b>%{x}</b><br>"
            "Correlación Spearman: %{z:.2f}"
            "<extra></extra>"
        )
    )

    # ---------------------------------------------------------
    # Separadores visuales entre bloques temáticos
    #
    # Red: posiciones 0–4
    # Reproducción: posiciones 5–7
    # Contenido/calidad: posiciones 8–10
    # ---------------------------------------------------------
    network_count = sum(
        column in available
        for column in [
            "delivery_rate_mbps",
            "rtt_ms",
            "min_rtt_ms",
            "cwnd",
            "in_flight",
        ]
    )

    playback_count = sum(
        column in available
        for column in [
            "buffer",
            "cum_rebuf",
            "ack_delay_seconds",
        ]
    )

    first_separator = network_count - 0.5
    second_separator = network_count + playback_count - 0.5

    if network_count > 0 and network_count < len(available):
        fig.add_vline(
            x=first_separator,
            line_width=2,
            line_color="#486581",
        )
        fig.add_hline(
            y=first_separator,
            line_width=2,
            line_color="#486581",
        )

    if (
        playback_count > 0
        and network_count + playback_count < len(available)
    ):
        fig.add_vline(
            x=second_separator,
            line_width=2,
            line_color="#486581",
        )
        fig.add_hline(
            y=second_separator,
            line_width=2,
            line_color="#486581",
        )

    # ---------------------------------------------------------
    # Diseño general
    # ---------------------------------------------------------
    fig.update_xaxes(
        tickfont=dict(size=13),
        tickangle=0,
        side="bottom",
        automargin=True,
    )

    fig.update_yaxes(
        tickfont=dict(size=13),
        autorange="reversed",
        automargin=True,
    )

    fig.update_layout(
        height=760,

        title=dict(
            text=(
                "Matriz de correlación entre variables ABR"
                "<br><sup>"
                "Variables organizadas por condiciones de red, "
                "estado de reproducción y calidad del segmento"
                "</sup>"
            ),
            font=dict(
                size=22,
                color="#102A43",
            ),
            x=0,
            xanchor="left",
        ),

        margin=dict(
            l=140,
            r=90,
            t=110,
            b=100,
        ),

        font=dict(
            family="Arial",
            size=13,
            color="#102A43",
        ),

        coloraxis_colorbar=dict(
            title=dict(
                text="Correlación<br>Spearman",
            ),
            thickness=16,
            len=0.72,
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["−1", "−0.5", "0", "0.5", "1"],
        ),

        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


def create_stream_timeseries(data, stream_id):
    stream_data = (
        data[data["stream_id"] == stream_id]
        .sort_values(["datetime_utc", "video_ts"])
        .copy()
    )

    if stream_data.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No existen datos para el stream seleccionado",
            template=PLOTLY_TEMPLATE,
        )
        return fig

    # Identificar los cambios de resolución
    change_events = stream_data[
        stream_data["resolution_change"].fillna(False)
    ].copy()

    fig = make_subplots(
        rows=5,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.22, 0.18, 0.21, 0.19, 0.20],
        subplot_titles=[
            "Resolución",
            "Buffer",
            "Tasa de entrega",
            "RTT",
            "Retardo hasta ACK",
        ],
    )

    # ---------------------------------------------------------
    # 1. Resolución como gráfico escalonado
    # ---------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=stream_data["elapsed_seconds"],
            y=stream_data["height"],
            mode="lines+markers",
            line_shape="hv",
            name="Resolución",
            marker=dict(size=4),
            customdata=np.column_stack(
                [
                    stream_data["format"].astype(str),
                    stream_data["segment_number"],
                    stream_data["change_direction"].astype(str),
                ]
            ),
            hovertemplate=(
                "Tiempo: %{x:.2f} s<br>"
                "Resolución: %{y:.0f}p<br>"
                "Formato: %{customdata[0]}<br>"
                "Segmento: %{customdata[1]}<br>"
                "Cambio: %{customdata[2]}"
                "<extra></extra>"
            ),
        ),
        row=1,
        col=1,
    )

    # ---------------------------------------------------------
    # 2. Buffer
    # ---------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=stream_data["elapsed_seconds"],
            y=stream_data["buffer"],
            mode="lines",
            name="Buffer",
            hovertemplate=(
                "Tiempo: %{x:.2f} s<br>"
                "Buffer: %{y:.2f} s"
                "<extra></extra>"
            ),
        ),
        row=2,
        col=1,
    )

    # ---------------------------------------------------------
    # 3. Tasa de entrega
    # ---------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=stream_data["elapsed_seconds"],
            y=stream_data["delivery_rate_mbps"],
            mode="lines",
            name="Tasa de entrega",
            hovertemplate=(
                "Tiempo: %{x:.2f} s<br>"
                "Tasa de entrega: %{y:.2f} Mbps"
                "<extra></extra>"
            ),
        ),
        row=3,
        col=1,
    )

    # ---------------------------------------------------------
    # 4. RTT
    # ---------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=stream_data["elapsed_seconds"],
            y=stream_data["rtt_ms"],
            mode="lines",
            name="RTT",
            hovertemplate=(
                "Tiempo: %{x:.2f} s<br>"
                "RTT: %{y:.2f} ms"
                "<extra></extra>"
            ),
        ),
        row=4,
        col=1,
    )

    # ---------------------------------------------------------
    # 5. Retardo hasta ACK
    # ---------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=stream_data["elapsed_seconds"],
            y=stream_data["ack_delay_seconds"],
            mode="lines",
            name="Retardo ACK",
            hovertemplate=(
                "Tiempo: %{x:.2f} s<br>"
                "Retardo ACK: %{y:.3f} s"
                "<extra></extra>"
            ),
        ),
        row=5,
        col=1,
    )

    # ---------------------------------------------------------
    # Marcadores y líneas para cambios de resolución
    # ---------------------------------------------------------
    reductions = change_events[
        change_events["change_direction"] == "Reducción de calidad"
    ]

    increases = change_events[
        change_events["change_direction"] == "Aumento de calidad"
    ]

    if not reductions.empty:
        fig.add_trace(
            go.Scatter(
                x=reductions["elapsed_seconds"],
                y=reductions["height"],
                mode="markers",
                name="Reducción de calidad",
                marker=dict(
                    size=11,
                    color="red",
                    symbol="triangle-down",
                    line=dict(width=1, color="black"),
                ),
                customdata=np.column_stack(
                    [
                        reductions["previous_height"],
                        reductions["height"],
                    ]
                ),
                hovertemplate=(
                    "Reducción de calidad<br>"
                    "Tiempo: %{x:.2f} s<br>"
                    "De %{customdata[0]:.0f}p "
                    "a %{customdata[1]:.0f}p"
                    "<extra></extra>"
                ),
            ),
            row=1,
            col=1,
        )

    if not increases.empty:
        fig.add_trace(
            go.Scatter(
                x=increases["elapsed_seconds"],
                y=increases["height"],
                mode="markers",
                name="Aumento de calidad",
                marker=dict(
                    size=11,
                    color="green",
                    symbol="triangle-up",
                    line=dict(width=1, color="black"),
                ),
                customdata=np.column_stack(
                    [
                        increases["previous_height"],
                        increases["height"],
                    ]
                ),
                hovertemplate=(
                    "Aumento de calidad<br>"
                    "Tiempo: %{x:.2f} s<br>"
                    "De %{customdata[0]:.0f}p "
                    "a %{customdata[1]:.0f}p"
                    "<extra></extra>"
                ),
            ),
            row=1,
            col=1,
        )

    # Dibujar líneas verticales en los cinco paneles
    for _, event in change_events.iterrows():
        event_time = event["elapsed_seconds"]
        direction = event["change_direction"]

        line_color = (
            "red"
            if direction == "Reducción de calidad"
            else "green"
        )

        annotation_text = (
            f"{int(event['previous_height'])}p → "
            f"{int(event['height'])}p"
        )

        fig.add_vline(
            x=event_time,
            line_width=1.5,
            line_dash="dash",
            line_color=line_color,
            opacity=0.65,
            row="all",
            col=1,
        )

        fig.add_annotation(
            x=event_time,
            y=event["height"],
            text=annotation_text,
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-35,
            font=dict(size=11, color=line_color),
            bgcolor="white",
            bordercolor=line_color,
            borderwidth=1,
            row=1,
            col=1,
        )

    # ---------------------------------------------------------
    # Formato del eje de resolución
    # ---------------------------------------------------------
    resolution_values = sorted(
        stream_data["height"].dropna().unique().tolist()
    )

    fig.update_yaxes(
        tickmode="array",
        tickvals=resolution_values,
        ticktext=[
            f"{int(value)}p"
            for value in resolution_values
        ],
        title_text="Resolución",
        row=1,
        col=1,
    )

    # Evitar un eje muy estrecho si solo hay una resolución
    if len(resolution_values) == 1:
        resolution = resolution_values[0]

        fig.update_yaxes(
            range=[resolution - 100, resolution + 100],
            row=1,
            col=1,
        )

    # Títulos de los demás ejes
    fig.update_yaxes(title_text="s", row=2, col=1)
    fig.update_yaxes(title_text="Mbps", row=3, col=1)
    fig.update_yaxes(title_text="ms", row=4, col=1)
    fig.update_yaxes(title_text="s", row=5, col=1)

    fig.update_xaxes(
        title_text=(
            "Tiempo transcurrido desde el inicio del stream (s)"
        ),
        row=5,
        col=1,
    )

    label = stream_data["stream_label"].iloc[0]
    channel = stream_data["channel"].iloc[0]

    fig.update_layout(
        height=1000,
        title=(
            f"Evolución temporal de {label} — canal {channel}"
            f"<br><sup>"
            f"{len(change_events)} cambios de resolución detectados"
            f"</sup>"
        ),
        hovermode="x unified",
        template=PLOTLY_TEMPLATE,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
        ),
        margin=dict(t=110),
    )

    return fig



def create_quality_sankey(change_events):
    """Crea un Sankey con colores por resolución."""

    transitions = (
        change_events
        .dropna(subset=["previous_height", "height"])
        .groupby(["previous_height", "height"], as_index=False)
        .size()
        .rename(columns={"size": "eventos"})
    )

    if transitions.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No existen transiciones para los filtros seleccionados",
            template=PLOTLY_TEMPLATE,
            height=560,
        )
        return fig

    transitions["origen"] = (
        transitions["previous_height"]
        .astype(int)
        .astype(str)
        + "p"
    )

    transitions["destino"] = (
        transitions["height"]
        .astype(int)
        .astype(str)
        + "p"
    )

    # Paleta fija por resolución
    resolution_colors = {
        "240p": "#5B8FF9",
        "360p": "#F4664A",
        "480p": "#5AD8A6",
        "720p": "#9270CA",
        "1080p": "#F6BD16",
    }

    source_labels = sorted(
        transitions["origen"].unique(),
        key=lambda value: int(value.replace("p", "")),
    )

    target_labels = sorted(
        transitions["destino"].unique(),
        key=lambda value: int(value.replace("p", "")),
    )

    # Etiquetas simples
    node_labels = source_labels + target_labels

    source_index = {
        label: idx
        for idx, label in enumerate(source_labels)
    }

    target_index = {
        label: len(source_labels) + idx
        for idx, label in enumerate(target_labels)
    }

    # Color sólido de cada nodo
    node_colors = (
        [
            resolution_colors.get(label, "#9AA9B8")
            for label in source_labels
        ]
        +
        [
            resolution_colors.get(label, "#9AA9B8")
            for label in target_labels
        ]
    )

    # Conversión HEX a RGBA para los flujos
    def hex_to_rgba(hex_color, alpha=0.38):
        hex_color = hex_color.lstrip("#")

        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)

        return f"rgba({red},{green},{blue},{alpha})"

    # Cada flujo hereda el color de la resolución de origen
    link_colors = [
        hex_to_rgba(
            resolution_colors.get(origin, "#9AA9B8"),
            alpha=0.38,
        )
        for origin in transitions["origen"]
    ]

    customdata = np.column_stack([
        transitions["origen"],
        transitions["destino"],
        transitions["eventos"],
    ])

    fig = go.Figure(
        go.Sankey(
            arrangement="snap",

            node=dict(
                pad=22,
                thickness=24,
                label=node_labels,
                color=node_colors,
                line=dict(
                    color="rgba(36,74,107,0.45)",
                    width=1,
                ),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Eventos relacionados: %{value:,}"
                    "<extra></extra>"
                ),
            ),

            link=dict(
                source=[
                    source_index[value]
                    for value in transitions["origen"]
                ],
                target=[
                    target_index[value]
                    for value in transitions["destino"]
                ],
                value=transitions["eventos"].tolist(),
                color=link_colors,
                customdata=customdata,
                hovertemplate=(
                    "<b>%{customdata[0]} → %{customdata[1]}</b><br>"
                    "Número de cambios: %{customdata[2]:,}"
                    "<extra></extra>"
                ),
            ),
        )
    )

    fig.update_layout(
        title=dict(
            text=(
                "Transiciones entre resoluciones"
                "<br><sup>"
                "El grosor del flujo representa la frecuencia del cambio"
                "</sup>"
            ),
            font=dict(
                size=18,
                color="#102A43",
            ),
        ),

        template=PLOTLY_TEMPLATE,
        height=600,

        font=dict(
            size=15,
            color="#102A43",
            family="Arial",
        ),

        margin=dict(
            l=35,
            r=35,
            t=95,
            b=25,
        ),

        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


def create_channel_bubble_chart(change_events):
    """Compara los cambios de calidad entre canales."""

    required_columns = [
        "channel",
        "stream_id",
        "change_direction",
    ]

    plot_data = change_events.dropna(
        subset=[
            column
            for column in required_columns
            if column in change_events.columns
        ]
    ).copy()

    if plot_data.empty:
        fig = go.Figure()
        fig.update_layout(
        height=620,

        margin=dict(
        l=70,
        r=40,
        t=110,
        b=70,
        ),

        font=dict(
        family="Arial",
        size=13,
        color="#102A43",
        ),

        legend=dict(
        title="Canal",
        orientation="h",
        yanchor="bottom",
        y=1.01,
        xanchor="right",
        x=1,
        font=dict(size=11),
        ),

    paper_bgcolor="white",
    plot_bgcolor="white",
)
        return fig

    # ---------------------------------------------------------
    # Resumen por canal
    # ---------------------------------------------------------
    channel_summary = (
        plot_data
        .groupby("channel", as_index=False)
        .agg(
            cambios_totales=("change_direction", "size"),
            streams_afectados=("stream_id", "nunique"),
            reducciones=(
                "change_direction",
                lambda values: (
                    values == "Reducción de calidad"
                ).sum(),
            ),
            aumentos=(
                "change_direction",
                lambda values: (
                    values == "Aumento de calidad"
                ).sum(),
            ),
        )
    )

    channel_summary["cambios_por_stream"] = (
        channel_summary["cambios_totales"]
        / channel_summary["streams_afectados"].replace(0, np.nan)
    )

    channel_summary["porcentaje_reducciones"] = (
        channel_summary["reducciones"]
        / channel_summary["cambios_totales"].replace(0, np.nan)
        * 100
    )

    channel_summary["canal_etiqueta"] = (
        channel_summary["channel"]
        .astype(str)
        .str.upper()
    )

    # ---------------------------------------------------------
    # Líneas de referencia
    # ---------------------------------------------------------
    referencia_x = channel_summary["cambios_por_stream"].median()
    referencia_y = channel_summary["porcentaje_reducciones"].median()

    max_x = channel_summary["cambios_por_stream"].max()
    min_x = channel_summary["cambios_por_stream"].min()

    x_upper = max(max_x * 1.22, referencia_x * 1.30, 1)
    x_lower = min(0, min_x * 0.85)

    # ---------------------------------------------------------
    # Gráfico de burbujas
    # Cada canal conserva un color distinto
    # ---------------------------------------------------------
    fig = px.scatter(
        channel_summary,
        x="cambios_por_stream",
        y="porcentaje_reducciones",
        size="cambios_totales",
        color="channel",
        text="canal_etiqueta",
        size_max=58,

        hover_data={
            "channel": False,
            "canal_etiqueta": False,
            "cambios_totales": ":,",
            "streams_afectados": ":,",
            "aumentos": ":,",
            "reducciones": ":,",
            "cambios_por_stream": ":.2f",
            "porcentaje_reducciones": ":.1f",
        },

        labels={
            "cambios_por_stream": "Cambios promedio por stream",
            "porcentaje_reducciones": "Reducciones de calidad (%)",
            "cambios_totales": "Cambios totales",
            "streams_afectados": "Streams afectados",
            "aumentos": "Aumentos de calidad",
            "reducciones": "Reducciones de calidad",
            "channel": "Canal",
        },

        title=(
            "Comparación de estabilidad de calidad entre canales"
            "<br><sup>"
            "Cada burbuja representa un canal · "
            "Tamaño = cambios totales"
            "</sup>"
        ),
        #font=dict(
        #size=24,
        #color="#102A43",
        #),
        template=PLOTLY_TEMPLATE,
    )

    # ---------------------------------------------------------
    # Estilo
    # ---------------------------------------------------------
    fig.update_traces(
        textposition="top center",
        textfont=dict(
            size=12,
            color="#102A43",
        ),
        marker=dict(
            opacity=0.80,
            line=dict(
                width=1.5,
                color="white",
            ),
        ),
    )

    # ---------------------------------------------------------
    # Cuadrantes
    # ---------------------------------------------------------
    fig.add_vline(
        x=referencia_x,
        line_width=1.5,
        line_dash="dash",
        line_color="#7B8A9A",
        opacity=0.85,
    )

    fig.add_hline(
        y=referencia_y,
        line_width=1.5,
        line_dash="dash",
        line_color="#7B8A9A",
        opacity=0.85,
    )

    # Zona crítica
    fig.add_shape(
        type="rect",
        x0=referencia_x,
        x1=x_upper,
        y0=referencia_y,
        y1=100,
        fillcolor="rgba(214,69,69,0.06)",
        line=dict(width=0),
        layer="below",
    )

    # ---------------------------------------------------------
    # Anotaciones
    # ---------------------------------------------------------
    fig.add_annotation(
        x=x_upper * 0.98,
        y=96,
        text="<b>Mayor inestabilidad</b>",
        showarrow=False,
        xanchor="right",
        font=dict(
            size=12,
            color="#B23A3A",
        ),
        bgcolor="rgba(255,255,255,0.90)",
        borderpad=4,
    )

    fig.add_annotation(
        x=referencia_x,
        y=2,
        text=f"Mediana: {referencia_x:.1f} cambios por stream",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        font=dict(
            size=10,
            color="#627D98",
        ),
        bgcolor="rgba(255,255,255,0.88)",
    )

    fig.add_annotation(
        x=x_lower,
        y=referencia_y,
        text=f"Mediana: {referencia_y:.1f}% de reducciones",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        font=dict(
            size=10,
            color="#627D98",
        ),
        bgcolor="rgba(255,255,255,0.88)",
    )

    # ---------------------------------------------------------
    # Ejes
    # ---------------------------------------------------------
    fig.update_xaxes(
        range=[x_lower, x_upper],
        showgrid=True,
        gridcolor="#E8EEF5",
        zeroline=False,
        title_standoff=14,
        automargin=True,
        tickfont=dict(size=13),
        title_font=dict(size=18),
    )

    fig.update_yaxes(
        range=[0, 105],
        ticksuffix="%",
        dtick=20,
        showgrid=True,
        gridcolor="#E8EEF5",
        zeroline=False,
        title_standoff=14,
        automargin=True,
        tickfont=dict(size=13),
        title_font=dict(size=18),
    )

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------
    fig.update_layout(
        height=660,

        margin=dict(
            l=70,
            r=130,
            t=125,
            b=75,
        ),

        font=dict(
            family="Arial",
            size=13,
            color="#102A43",
        ),

        legend=dict(
            title="Canal",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=11),
        ),

        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


def to_csv_bytes(data):
    return data.to_csv(index=False).encode("utf-8-sig")


if "show_dashboard" not in st.session_state:
    st.session_state["show_dashboard"] = False

if not st.session_state["show_dashboard"]:
    show_landing_page()
    st.stop()

segments, stream_summary, client_events, bitrate_ladder = load_data()

top_left, top_right = st.columns([6, 1])
with top_left:
    st.title("Análisis visual de selección adaptativa de bitrate")
with top_right:
    if st.button("← Inicio", use_container_width=True):
        st.session_state["show_dashboard"] = False
        st.rerun()
st.caption(
    "Exploración de variables de red, buffer, calidad y cambios de resolución."
)

with st.sidebar:
    st.header("Filtros")

    channel_options = sorted(segments["channel"].dropna().astype(str).unique())
    selected_channels = st.multiselect(
        "Canal",
        options=channel_options,
        default=channel_options,
    )

    experiment_options = sorted(segments["expt_id"].dropna().unique().tolist())
    selected_experiments = st.multiselect(
        "Experimento",
        options=experiment_options,
        default=experiment_options,
    )

    resolution_options = ordered_resolutions(segments)
    selected_resolutions = st.multiselect(
        "Resolución",
        options=resolution_options,
        default=resolution_options,
    )

    available_streams = (
        segments[
            segments["channel"].astype(str).isin(selected_channels)
            & segments["expt_id"].isin(selected_experiments)
            & segments["resolution"].isin(selected_resolutions)
        ][["stream_id", "stream_label"]]
        .drop_duplicates()
        .sort_values("stream_label")
    )

    selected_streams = st.multiselect(
        "Streams",
        options=available_streams["stream_id"].tolist(),
        format_func=lambda stream_id: available_streams.set_index(
            "stream_id"
        ).loc[stream_id, "stream_label"],
        placeholder="Todos los streams",
    )

filtered = filter_data(
    segments,
    selected_channels,
    selected_experiments,
    selected_resolutions,
    selected_streams,
)

if filtered.empty:
    st.warning("No hay datos para la combinación de filtros seleccionada.")
    st.stop()

dominant_resolution = (
    filtered["resolution"].mode().iloc[0]
    if not filtered["resolution"].dropna().empty
    else "N/D"
)

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
kpi1.metric("Sesiones", f"{filtered['session_id'].nunique():,}")
kpi2.metric("Streams", f"{filtered['stream_id'].nunique():,}")
kpi3.metric("Segmentos", f"{len(filtered):,}")
kpi4.metric(
    "Throughput mediano",
    f"{filtered['delivery_rate_mbps'].median():.2f} Mbps",
)
kpi5.metric("RTT mediano", f"{filtered['rtt_ms'].median():.2f} ms")
kpi6.metric("Resolución dominante", dominant_resolution)

selected = show_dashboard_navigation()

if selected == "Resumen":
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_resolution_distribution(filtered),
            use_container_width=True,
            key="resolution_distribution",
        )

    with col2:
        st.plotly_chart(
            create_boxplot(
                filtered,
                "delivery_rate_mbps",
                "tasa de entrega (Mbps)",
                log_scale=True,
            ),
            use_container_width=True,
        )

    st.plotly_chart(
        create_correlation_heatmap(filtered),
        use_container_width=True,
        key="correlation_heatmap",
    )

if selected == "Evolución temporal":
    stream_choices = (
        filtered[["stream_id", "stream_label", "channel"]]
        .drop_duplicates()
        .sort_values("stream_label")
    )

    selected_stream = st.selectbox(
        "Selecciona un stream",
        options=stream_choices["stream_id"].tolist(),
        format_func=lambda stream_id: (
            stream_choices.set_index("stream_id")
            .loc[stream_id, "stream_label"]
        ),
    )

    st.plotly_chart(
        create_stream_timeseries(filtered, selected_stream),
        use_container_width=True,
        key="stream_timeseries",
    )

if selected == "Condiciones de red":
    st.plotly_chart(
        create_network_scatter(filtered),
        use_container_width=True,
        key="network_scatter",
    )

    metric = st.selectbox(
        "Variable para comparar por resolución",
        options=[
            "delivery_rate_mbps",
            "rtt_ms",
            "buffer",
            "ssim_index",
            "ack_delay_seconds",
        ],
        format_func={
            "delivery_rate_mbps": "Tasa de entrega (Mbps)",
            "rtt_ms": "RTT (ms)",
            "buffer": "Buffer (s)",
            "ssim_index": "SSIM",
            "ack_delay_seconds": "Retardo ACK (s)",
        }.get,
    )

    st.plotly_chart(
        create_boxplot(
            filtered,
            metric,
            {
                "delivery_rate_mbps": "tasa de entrega (Mbps)",
                "rtt_ms": "RTT (ms)",
                "buffer": "buffer (s)",
                "ssim_index": "SSIM",
                "ack_delay_seconds": "retardo ACK (s)",
            }[metric],
            log_scale=(metric == "delivery_rate_mbps"),
        ),
        use_container_width=True,
        key="boxplot",
    )

if selected == "Cambios de calidad":
    change_events = filtered[
        filtered["resolution_change"].fillna(False)
    ].copy()

    increase = (
        change_events["change_direction"] == "Aumento de calidad"
    ).sum()
    decrease = (
        change_events["change_direction"] == "Reducción de calidad"
    ).sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Cambios de resolución", f"{len(change_events):,}")
    c2.metric("Aumentos", f"{increase:,}")
    c3.metric("Reducciones", f"{decrease:,}")

    if change_events.empty:
        st.info("No existen cambios de resolución en el subconjunto filtrado.")
    else:
        st.plotly_chart(
        create_quality_sankey(change_events),
        use_container_width=True,
        key="quality_sankey",
        )

        st.plotly_chart(
        create_channel_bubble_chart(change_events),
        use_container_width=True,
        key="channel_bubble_chart",
        )

if selected == "Datos":
    display_columns = [
        "datetime_utc",
        "stream_label",
        "channel",
        "expt_id",
        "segment_number",
        "resolution",
        "delivery_rate_mbps",
        "rtt_ms",
        "buffer",
        "cum_rebuf",
        "ssim_index",
        "ack_delay_seconds",
        "change_direction",
    ]
    display_columns = [c for c in display_columns if c in filtered.columns]

    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
        height=520,
    )

    st.download_button(
        "Descargar datos filtrados en CSV",
        data=to_csv_bytes(filtered[display_columns]),
        file_name="puffer_datos_filtrados.csv",
        mime="text/csv",
    )
