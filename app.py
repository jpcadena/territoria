"""
Streamlit application for UI Dashboard
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

COLORS: dict[str, str] = {"CACAO": "#2ecc71", "BANANO": "#f1c40f"}
TABLE_NAME: str = "Hoja 1"


class DataService:
    """Service class responsible for data acquisition and transformation."""

    @staticmethod
    @st.cache_data(ttl=60, persist="disk")
    def _fetch_raw_data(url: str) -> pd.DataFrame:
        """
        Fetches the raw CSV data from the cloud with disk persistence.

        Args:
            url (str): The public URL of the Google Sheets CSV export.

        Returns:
            pd.DataFrame: The raw dataframe directly from the source.
        """
        return pd.read_csv(url)

    @staticmethod
    @st.cache_data
    def fetch_processed_data() -> pd.DataFrame:
        """
        Applies transformation logic over cached raw data using layered caching.

        Returns:
            pd.DataFrame: A processed dataframe with coordinates and mapped image URLs.
        """
        try:
            url: str = st.secrets["CSV_URL"]
            app_id: str = st.secrets["APP_ID"]
        except KeyError:
            st.error("Error: No se encontraron las variables en Secrets.")
            return pd.DataFrame()
        try:
            dataframe: pd.DataFrame = DataService._fetch_raw_data(url)
            if "GPS" in dataframe.columns:
                coords = (
                    dataframe["GPS"].str.split(",", expand=True).astype(float)
                )
                dataframe["lat"], dataframe["lon"] = coords[0], coords[1]
            if "FECHA" in dataframe.columns:
                dataframe["FECHA"] = pd.to_datetime(
                    dataframe["FECHA"], dayfirst=True
                )
            if "FOTO" in dataframe.columns:
                base_url = "https://www.appsheet.com/template/gettablefileurl"
                dataframe["FOTO"] = dataframe["FOTO"].apply(
                    lambda x: (
                        f"{base_url}?appName={app_id}&tableName={TABLE_NAME}&fileName={x}"
                        if pd.notna(x) and not str(x).startswith("http")
                        else x
                    )
                )
            return dataframe
        except Exception as e:
            st.sidebar.error(f"Error técnico: {e}")
            return pd.DataFrame()


class Visualizer:
    """Utility class for generating interactive data visualizations."""

    @staticmethod
    def plot_distribution(dataframe: pd.DataFrame) -> go.Figure:
        """
        Creates a donut chart for crop distribution.

        Args:
            dataframe (pd.DataFrame): The source dataframe.

        Returns:
            go.Figure: A Plotly Express pie figure.
        """
        return px.pie(
            dataframe,
            names="CULTIVO",
            hole=0.5,
            color="CULTIVO",
            color_discrete_map=COLORS,
            title="Distribución de Cultivos",
        )

    @staticmethod
    def plot_trends(df: pd.DataFrame) -> go.Figure:
        """
        Generates a line chart for temperature trends.

        Args:
            df (pd.DataFrame): The source dataframe.

        Returns:
            go.Figure: A Plotly Express line figure.
        """
        figure: go.Figure = px.line(
            df.sort_values("FECHA"),
            x="FECHA",
            y="TEMPERATURA",
            color="CULTIVO",
            color_discrete_map=COLORS,
            markers=True,
            title="Tendencia de Temperatura",
        )
        figure.update_layout(xaxis_title="Fecha", yaxis_title="Temp °C")
        return figure


class DashboardUI:
    """Orchestrator class for the Streamlit user interface."""

    def __init__(self):
        """Initializes the page configuration and main services."""
        st.set_page_config(
            page_title="AgTech Pro Dashboard", layout="wide", page_icon="🌱"
        )

    @staticmethod
    def render_sidebar():
        """
        Renders the configuration sidebar.

        Returns:
            NoneType: None
        """
        with st.sidebar:
            st.header("⚙️ Configuración")
            if st.button("🔄 Actualizar Datos"):
                st.cache_data.clear()
                st.rerun()

    @staticmethod
    def render_metrics(dataframe: pd.DataFrame) -> None:
        """
        Displays KPI metrics at the top of the dashboard.

        Args:
            dataframe (pd.DataFrame): The dataframe to calculate metrics from.

        Returns:
            NoneType: None
        """
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Inspecciones", len(dataframe))
        with c2:
            st.metric("Temp. Media", f"{dataframe['TEMPERATURA'].mean():.1f}°C")
        with c3:
            st.metric("Humedad Media", f"{dataframe['HUMEDAD'].mean():.1f}%")
        with c4:
            alerts = (
                dataframe["DIAGNOSTICO"]
                .str.contains(
                    "riesgo|plaga|enfermedad|Monilia", case=False, na=False
                )
                .sum()
            )
            st.metric(
                "Alertas IA",
                alerts,
                delta=f"{alerts} críticas",
                delta_color="inverse",
            )

    @staticmethod
    def render_content(dataframe: pd.DataFrame) -> None:
        """
        Renders the main tabs and interactive content.

        Args:
            dataframe (pd.DataFrame): The dataframe to visualize.

        Returns:
            NoneType: None
        """
        t1, t2, t3 = st.tabs(
            [
                "📍 Mapa de Campo",
                "📊 Análisis Estadístico",
                "📋 Registros de Inspección",
            ]
        )
        with t1:
            st.subheader("Ubicación de Lotes")
            st.map(dataframe[["lat", "lon"]])
        with t2:
            c1, c2 = st.columns(2)
            c1.plotly_chart(
                Visualizer.plot_distribution(dataframe), width="stretch"
            )
            c2.plotly_chart(Visualizer.plot_trends(dataframe), width="stretch")
        with t3:
            query: str | None = st.text_input("Buscar por Agricultor:")
            filtered = (
                dataframe[
                    dataframe["AGRICULTOR"].str.contains(query, case=False)
                ]
                if query
                else dataframe
            )
            st.dataframe(
                filtered[
                    [
                        "FECHA",
                        "AGRICULTOR",
                        "CULTIVO",
                        "TEMPERATURA",
                        "HUMEDAD",
                        "DIAGNOSTICO",
                    ]
                ],
                width="stretch",
            )
            for _, row in filtered.iterrows():
                with st.expander(
                    f"Reporte: {row['AGRICULTOR']} - {row['CULTIVO']}"
                ):
                    st.write(f"**Diagnóstico de IA:** {row['DIAGNOSTICO']}")
                    if "FOTO" in row and pd.notna(row["FOTO"]):
                        st.image(
                            row["FOTO"], width=500, caption="Evidencia visual"
                        )

    def run(self) -> None:
        """
        Main execution flow for the dashboard application.

        Returns:
            NoneType: None
        """
        st.title("🌱 Sistema de Inteligencia Agrícola")
        st.markdown(
            "Monitoreo avanzado mediante integración AppSheet, Make y Gemini IA."
        )
        self.render_sidebar()
        data: pd.DataFrame = DataService.fetch_processed_data()
        if not data.empty:
            self.render_metrics(data)
            st.divider()
            self.render_content(data)
        else:
            st.error(
                "Error: No se pudo cargar la base de datos desde Google Sheets."
            )
            st.info(
                "Asegúrese de que el archivo esté publicado como CSV en la web."
            )


if __name__ == "__main__":
    DashboardUI().run()
