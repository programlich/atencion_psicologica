import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

rows_1 = st.container().columns([0.3, 0.3, 0.3, 0.1])
rows_2 = st.container().columns([0.4, 0.4, 0.2])
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
balance_df["precio / unidad (€)"] = balance_df["precio / unidad (PEN)"] / euro_to_soles
balance_df["gastos / unidad (€)"] = balance_df["gastos / unidad (PEN)"] / euro_to_soles


st.dataframe(balance_df)