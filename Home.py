import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

rows_2_container = st.container()
st.divider()
rows_1 = st.container().columns([0.2, 0.2, 0.2, 0.1, 0.3])

# Misc input
misc_input_container = rows_1[3].container(border=True)

misc_input_container.write("###### Tipo de cambio")
euro_to_soles = misc_input_container.number_input(label="1€ = x PEN", value=4.0, key="exchange_rate_key",
                                                  help="tipo de cambio € | PEN")

balance_df = pd.DataFrame({"type": [],
                           "precio / unidad (PEN)": [],
                           "gastos / unidad (PEN)": [],
                           "unidades / mes": [],
                           "tiempo / unidad (h)": [],
                           "precio / unidad (€)": [],
                           "gastos / unidad (€)": []})
# Add values row by row
rows = [
    {"type": "terapia individual"},
    {"type": "terapia de grupo"},
    {"type": "talleres"},
]
balance_df = pd.concat([balance_df, pd.DataFrame(rows)], ignore_index=True)

# Terapia individual
ti_container = rows_1[0].container(border=True)
ti_container.subheader("Terapia individual")

ti_precio = ti_container.number_input(label="Precio / unidad (PEN)", value=0.0, key="ti_precio_key", min_value=0.0,
                                      step=10.0, help="Precio que pedimos por unidad en Soles peruanos")
ti_gastos = ti_container.number_input(label="Gastos / unidad (PEN)", value=0.0, key="ti_gastos_key", min_value=0.0,
                                      step=10.0, help="Gastos que hay por unidad en Soles peruanos")
ti_unidades = ti_container.number_input(label="Unidades / mes", value=0, key="ti_unidades_key", min_value=0,
                                      step=1, help="Unidades dado por mes")
ti_tiempo = ti_container.number_input(label="Tiempo / unidad (h)", value=0.0, key="ti_tiempo_key", min_value=0.0,
                                      step=0.5, help="Tiempo de una unidad en horas (90 min = 1.5 horas)")

# Terapia grupal
tg_container = rows_1[1].container(border=True)
tg_container.subheader("Terapia de grupo")

tg_precio = tg_container.number_input(label="Precio / unidad (PEN)", value=0.0, key="tg_precio_key", min_value=0.0,
                                      step=10.0, help="Precio que pedimos por unidad en Soles peruanos")
tg_gastos = tg_container.number_input(label="Gastos / unidad (PEN)", value=0.0, key="tg_gastos_key", min_value=0.0,
                                      step=10.0, help="Gastos por unidad en Soles peruanos (material, administración,...)")
tg_unidades = tg_container.number_input(label="Unidades / mes", value=0, key="tg_unidades_key", min_value=0,
                                      step=1, help="Unidades dado por mes")
tg_tiempo = tg_container.number_input(label="Tiempo / unidad (h)", value=0.0, key="tg_tiempo_key", min_value=0.0,
                                      step=0.5, help="Tiempo de una unidad en horas (90 min = 1.5 horas)")

# Talleres
taller_container = rows_1[2].container(border=True)
taller_container.subheader("Talleres")

taller_precio = taller_container.number_input(label="Precio / unidad (PEN)", value=0.0, key="taller_precio_key",
                                              min_value=0.0,
                                      step=10.0, help="Precio que pedimos por unidad en Soles peruanos")
taller_gastos = taller_container.number_input(label="Gastos / unidad (PEN)", value=0.0, key="taller_gastos_key",
                                              min_value=0.0,
                                      step=10.0, help="Gastos que hay por unidad en Soles peruanos")
taller_unidades = taller_container.number_input(label="Unidades / mes", value=0, key="taller_unidades_key", min_value=0,
                                      step=1, help="Unidades dado por mes")
taller_tiempo = taller_container.number_input(label="Tiempo / unidad (h)", value=0.0, key="taller_tiempo_key",
                                              min_value=0.0,
                                      step=0.5, help="Tiempo de una unidad en horas (90 min = 1.5 horas)")

# Add prices / unit to balance_df
balance_df.loc[balance_df["type"] == "terapia individual", "precio / unidad (PEN)"] = ti_precio
balance_df.loc[balance_df["type"] == "terapia de grupo", "precio / unidad (PEN)"] = tg_precio
balance_df.loc[balance_df["type"] == "talleres", "precio / unidad (PEN)"] = taller_precio

# Add expenses / unit to balance_df
balance_df.loc[balance_df["type"] == "terapia individual", "gastos / unidad (PEN)"] = ti_gastos
balance_df.loc[balance_df["type"] == "terapia de grupo", "gastos / unidad (PEN)"] = tg_gastos
balance_df.loc[balance_df["type"] == "talleres", "gastos / unidad (PEN)"] = taller_gastos

# Add units / mes to balance_df
balance_df.loc[balance_df["type"] == "terapia individual", "unidades / mes"] = ti_unidades
balance_df.loc[balance_df["type"] == "terapia de grupo", "unidades / mes"] = tg_unidades
balance_df.loc[balance_df["type"] == "talleres", "unidades / mes"] = taller_unidades

# Add time / unit to balance_df
balance_df.loc[balance_df["type"] == "terapia individual", "tiempo / unidad (h)"] = ti_tiempo
balance_df.loc[balance_df["type"] == "terapia de grupo", "tiempo / unidad (h)"] = tg_tiempo
balance_df.loc[balance_df["type"] == "talleres", "tiempo / unidad (h)"] = taller_tiempo

# Calculate values for remaining cols
# Price and expenses in €
balance_df["precio / unidad (€)"] = balance_df["precio / unidad (PEN)"] / euro_to_soles
balance_df["gastos / unidad (€)"] = balance_df["gastos / unidad (PEN)"] / euro_to_soles

# Total time per month and year
balance_df["tiempo / mes"] = balance_df["tiempo / unidad (h)"] * balance_df["unidades / mes"]
balance_df["tiempo / ano"] = balance_df["tiempo / unidad (h)"] * balance_df["unidades / mes"] * 12

# Income per unit
balance_df["ingreso / unidad (PEN)"] = balance_df["precio / unidad (PEN)"] - balance_df["gastos / unidad (PEN)"]
balance_df["ingreso / unidad (€)"] = balance_df["precio / unidad (€)"] - balance_df["gastos / unidad (€)"]

# Income per month and year in PEN and €
balance_df["ingreso / mes (PEN)"] = balance_df["ingreso / unidad (PEN)"] * balance_df["unidades / mes"]
balance_df["ingreso / ano (PEN)"] = balance_df["ingreso / unidad (PEN)"] * balance_df["unidades / mes"] * 12
balance_df["ingreso / mes (€)"] = balance_df["ingreso / unidad (€)"] * balance_df["unidades / mes"]
balance_df["ingreso / ano (€)"] = balance_df["ingreso / unidad (€)"] * balance_df["unidades / mes"] * 12

balance_df_without_sum = balance_df.copy()

# Create a sum row
sum_row = balance_df.select_dtypes(include=np.number).sum()
sum_row["type"] = "total"
sum_df = pd.DataFrame([sum_row])
balance_df = pd.concat([balance_df, sum_df], ignore_index=True, axis=0)

# Show key metrics
time_unit_tabs = rows_2_container.tabs(["Mes", "Año"])

with time_unit_tabs[0]:
    month_cols = st.columns([0.4, 0.4, 0.2])

    # Time barplot
    time_month_container = month_cols[0].container(border=True, height=550)
    time_month_container.write("#### Tiempo planificado")
    time_bar_fig = px.bar(data_frame=balance_df, x="type", y="tiempo / mes")
    time_bar_fig.update_layout(xaxis_title="",
                                 yaxis={"showgrid":False,
                                        "titlefont": {"size": 20},
                                        "tickfont": {"size": 15}},
                                 xaxis={"titlefont": {"size": 20},
                                        "tickfont": {"size": 15},
                                        "linecolor": "white"})
    time_bar_fig.update_traces(marker_color="#C6A95D")
    time_month_container.plotly_chart(time_bar_fig)

    # Income barplot
    income_month_container = month_cols[1].container(border=True)
    income_month_top_cols = income_month_container.columns(2)
    unit = income_month_top_cols[1].radio(label="Divisa", options=["PEN", "€"], horizontal=True, key="unit_month_key")
    income_month_top_cols[0].write(f"#### Ingreso expectado ({unit})")
    income_bar_fig = px.bar(data_frame=balance_df, x="type", y=f"ingreso / mes ({unit})")
    income_bar_fig.update_layout(xaxis_title="",
                                 yaxis={"showgrid":False,
                                        "titlefont": {"size": 20},
                                        "tickfont": {"size": 15}},
                                 xaxis={"titlefont": {"size": 20},
                                        "tickfont": {"size": 15},
                                        "linecolor": "white"})
    income_bar_fig.update_traces(marker_color="#C6A95D")
    income_month_container.plotly_chart(income_bar_fig)

    # Key metrics
    total_time_month = balance_df_without_sum["tiempo / mes"].sum()
    month_cols[2].container(border=True).metric(label="Tiempo total", value=f"{total_time_month} h")

    total_income_month_pen = balance_df_without_sum["ingreso / mes (PEN)"].sum()
    month_cols[2].container(border=True).metric(label="Ingreso total (PEN)", value=f"{total_income_month_pen} S")


    total_income_month_euro = balance_df_without_sum["ingreso / mes (€)"].sum()
    month_cols[2].container(border=True).metric(label="Ingreso total (€)", value=f"{total_income_month_euro} €")


with time_unit_tabs[1]:
    year_cols = st.columns([0.4, 0.4, 0.2])

    # Time barplot
    time_year_container = year_cols[0].container(border=True, height=550)
    time_year_container.write("#### Tiempo planificado")
    time_bar_year_fig = px.bar(data_frame=balance_df, x="type", y="tiempo / ano")
    time_bar_year_fig.update_layout(xaxis_title="",
                                 yaxis={"showgrid":False,
                                        "titlefont": {"size": 20},
                                        "tickfont": {"size": 15}},
                                 xaxis={"titlefont": {"size": 20},
                                        "tickfont": {"size": 15},
                                        "linecolor": "white"})
    time_bar_year_fig.update_traces(marker_color="#C6A95D")
    time_year_container.plotly_chart(time_bar_year_fig)

    # Income barplot
    income_year_container = year_cols[1].container(border=True)
    income_year_top_cols = income_year_container.columns(2)
    unit = income_year_top_cols[1].radio(label="Divisa", options=["PEN", "€"], horizontal=True, key="unit_year_key")
    income_year_top_cols[0].write(f"#### Ingreso expectado ({unit})")
    income_bar_year_fig = px.bar(data_frame=balance_df, x="type", y=f"ingreso / ano ({unit})")
    income_bar_year_fig.update_layout(xaxis_title="",
                                 yaxis={"showgrid":False,
                                        "titlefont": {"size": 20},
                                        "tickfont": {"size": 15}},
                                 xaxis={"titlefont": {"size": 20},
                                        "tickfont": {"size": 15},
                                        "linecolor": "white"})
    income_bar_year_fig.update_traces(marker_color="#C6A95D")
    income_year_container.plotly_chart(income_bar_year_fig)

    # Key metrics
    total_time_year = balance_df_without_sum["tiempo / ano"].sum()
    year_cols[2].container(border=True).metric(label="Tiempo total", value=f"{total_time_year} h")

    total_income_year_pen = balance_df_without_sum["ingreso / ano (PEN)"].sum()
    year_cols[2].container(border=True).metric(label="Ingreso total (PEN)", value=f"{total_income_year_pen} S")


    total_income_year_euro = balance_df_without_sum["ingreso / ano (€)"].sum()
    year_cols[2].container(border=True).metric(label="Ingreso total (€)", value=f"{total_income_year_euro} €")


st.dataframe(balance_df)