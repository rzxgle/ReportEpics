import streamlit as st
import plotly.express as px
from datetime import date


def render_roadmap(roadmap_df, start_date=None, end_date=None, quarter_time_progress=None, sprints=None):
    if roadmap_df.empty:
        st.info("Nenhum épico para exibir no roadmap.")
        return
    
    all_display_names = roadmap_df["display_name"].tolist()

    plot_df = roadmap_df.dropna(subset=["start_date", "end_date"]).copy()

    if plot_df.empty:
        st.info("Nenhum épico com datas válidas para gerar barras no roadmap.")
        return
    
    fig = px.timeline(
        plot_df,
        x_start="start_date",
        x_end="end_date",
        y="display_name",
        color="roadmap_status",
        text="progress_label",
        color_discrete_map={
            "Em andamento": "#537edb",
            "Concluído": "#16a34a",
            "Em risco": "#f97316",
            "Atrasado": "#e24242",
            "Transbordo": "#935eee"
        },
        custom_data=[
            "team",
            "epic_full_name",
            "progress_label",
            "date_range_label",
            "roadmap_status",
            "risk_label",
            "transbordo_label",
            "temporal_status"
        ]
    )

    fig.update_traces(
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(size=17, color="white"),
        marker_line_color="white",
        marker_line_width=0,
        hovertemplate=
        "<b>%{customdata[1]}</b><br><br>" +
        "Squad: %{customdata[0]}<br>" +
        "Progresso: %{customdata[2]}<br>" +
        "Período: %{customdata[3]}<br>" +
        "Status: %{customdata[4]}<br>" +
        "Risco: %{customdata[5]}<br>" +
        "Prazo: %{customdata[7]}<br>" +
        "Transbordo: %{customdata[6]}<extra></extra>"
    )

    today = date.today()

    # Áreas de tempo do quarter: passado x restante
    if start_date is not None and end_date is not None:
        if today < start_date:
            fig.add_vrect(
                x0=start_date,
                x1=end_date,
                fillcolor="#f3f4f6",
                opacity=0.35,
                line_width=0,
                layer="below",
                annotation_text="Quarter futuro",
                annotation_position="top left",
                annotation_font_size=11,
                annotation_font_color="#6b7280"
            )

        elif today > end_date:
            fig.add_vrect(
                x0=start_date,
                x1=end_date,
                fillcolor="#fee2e2",
                opacity=0.18,
                line_width=0,
                layer="below",
                annotation_text="Quarter encerrado",
                annotation_position="top left",
                annotation_font_size=11,
                annotation_font_color="#991b1b"
            )

        else:
            fig.add_vrect(
                x0=start_date,
                x1=today,
                fillcolor="#D8D8D8",
                opacity=0.30,
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
        
    # Divisões de sprint
    if sprints:
        for sprint in sprints:

            sprint_start = sprint["start"]

            fig.add_vline(
                x=sprint_start,
                line_width=1,
                line_dash="dot",
                line_color="#d1d5db"
            )

            fig.add_annotation(
                x=sprint_start,
                y=1.01,
                xref="x",
                yref="paper",
                text=sprint["name"],
                showarrow=False,
                font=dict(size=9, color="#9ca3af")
            )

    # Linha de hoje
    fig.add_vline(
        x=today,
        line_width=1.5,
        line_dash="dash",
        line_color="#bfbfbf"
    )
    
    today_label = "Hoje"

    if quarter_time_progress is not None:
        today_label = f"Hoje"

    fig.add_annotation(
        x=today,
        y=1.08,
        xref="x",
        yref="paper",
        text=today_label,
        showarrow=False,
        font=dict(size=12, color="#dc2626")
    )

    fig.update_yaxes(
        autorange="reversed",
        title=None,
        showgrid=False,
        tickfont=dict(size=12, color="#111827"),
        categoryorder="array",
        categoryarray=all_display_names[::-1]
    )

    fig.update_xaxes(
        title=None,
        showgrid=False,
        showticklabels=False,
        zeroline=False
    )
    
    chart_height = min(
        max(750, len(roadmap_df) * 48),
        1800
    )

    fig.update_layout(
        height=chart_height,
        legend_title="Status",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0
        ),
        margin=dict(l=20, r=20, t=80, b=80),
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.30
    )

    st.plotly_chart(fig, use_container_width=True)