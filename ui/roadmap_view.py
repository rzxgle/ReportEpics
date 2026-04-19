import streamlit as st
import plotly.express as px
from datetime import date


def render_roadmap(roadmap_df, start_date=None, end_date=None):
    if roadmap_df.empty:
        st.info("Nenhum épico com datas válidas para exibir no roadmap.")
        return

    fig = px.timeline(
        roadmap_df,
        x_start="start_date",
        x_end="end_date",
        y="display_name",
        color="roadmap_status",
        text="progress_label",
        color_discrete_map={
            "Em andamento": "#2563eb",
            "Concluído": "#16a34a",
            "Em risco": "#dc2626",
            "Transbordo": "#7c3aed"
        },
        custom_data=[
            "team",
            "epic_full_name",
            "progress_label",
            "date_range_label",
            "roadmap_status",
            "risk_label",
            "transbordo_label"
        ]
    )

    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=11, color="white"),
        marker_line_color="white",
        marker_line_width=1.2,
        hovertemplate=
        "<b>%{customdata[1]}</b><br><br>" +
        "Squad: %{customdata[0]}<br>" +
        "Progresso: %{customdata[2]}<br>" +
        "Período: %{customdata[3]}<br>" +
        "Status: %{customdata[4]}<br>" +
        "Risco: %{customdata[5]}<br>" +
        "Transbordo: %{customdata[6]}<extra></extra>"
    )

    today = date.today()

    # Área sombreada do quarter
    if start_date is not None and end_date is not None:
        fig.add_vrect(
            x0=start_date,
            x1=end_date,
            fillcolor="#e5e7eb",
            opacity=0.28,
            line_width=0,
            layer="below"
        )

    # Limites do quarter
    if start_date is not None:
        fig.add_vline(
            x=start_date,
            line_width=1.5,
            line_dash="dot",
            line_color="#6b7280"
        )
        fig.add_annotation(
            x=start_date,
            y=1.04,
            xref="x",
            yref="paper",
            text="Início do quarter",
            showarrow=False,
            font=dict(size=11, color="#6b7280")
        )

    if end_date is not None:
        fig.add_vline(
            x=end_date,
            line_width=1.5,
            line_dash="dot",
            line_color="#6b7280"
        )
        fig.add_annotation(
            x=end_date,
            y=1.04,
            xref="x",
            yref="paper",
            text="Fim do quarter",
            showarrow=False,
            font=dict(size=11, color="#6b7280")
        )

    # Linha de hoje
    fig.add_vline(
        x=today,
        line_width=2.5,
        line_dash="dash",
        line_color="#dc2626"
    )

    fig.add_annotation(
        x=today,
        y=1.08,
        xref="x",
        yref="paper",
        text="Hoje",
        showarrow=False,
        font=dict(size=12, color="#dc2626")
    )

    fig.update_yaxes(
        autorange="reversed",
        title=None,
        showgrid=False,
        tickfont=dict(size=12, color="#111827")
    )

    fig.update_xaxes(
        title=None,
        showgrid=True,
        gridcolor="#e5e7eb",
        tickfont=dict(size=11, color="#4b5563"),
        tickformat="%d/%m"
    )

    fig.update_layout(
        height=max(650, len(roadmap_df) * 38),
        legend_title="Status",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.12,
            xanchor="left",
            x=0
        ),
        margin=dict(l=20, r=20, t=80, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.30,
        font=dict(family="Arial, sans-serif", color="#111827")
    )

    st.plotly_chart(fig, use_container_width=True)