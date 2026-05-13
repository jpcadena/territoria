# 🌱 Territoria Dashboard

<a name="readme-top"></a>

<br />
<div align="center">
  <h1 align="center">Territoria Dashboard System</h1>

  <p align="center">
    Monitoreo agrícola avanzado con IA Multimodal para cultivos de Cacao y Banano.
    <br />
    <a href="https://territoria-jpcadena.streamlit.app/"><strong>Explorar App en Vivo »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jpcadena/territoria/issues">Report Bug</a>
    ·
    <a href="https://github.com/jpcadena/territoria/issues">Request Feature</a>
  </p>
</div>

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://territoria-jpcadena.streamlit.app/)

<details>
  <summary>Tabla de Contenidos</summary>
  <ol>
    <li><a href="#acerca-del-proyecto">Acerca del Proyecto</a></li>
    <li><a href="#stack-tecnológico">Stack Tecnológico</a></li>
    <li><a href="#empezando">Empezando</a></li>
    <li><a href="#configuración">Configuración</a></li>
    <li><a href="#despliegue">Despliegue</a></li>
    <li><a href="#licencia">Licencia</a></li>
  </ol>
</details>

## Acerca del Proyecto

Este sistema integra una arquitectura robusta de recolección de datos y análisis predictivo. Diseñado bajo principios **SOLID** y **GRASP**, permite transformar imágenes capturadas en campo en diagnósticos fitopatológicos accionables mediante IA.

**Componentes clave:**

* **Captura:** Interfaz móvil vía AppSheet para recolección offline/online.
* **Orquestación:** Workflows automatizados en Make.com.
* **Inteligencia:** Análisis multimodal con Google Gemini IA.
* **Visualización:** Dashboard interactivo desarrollado en Streamlit.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Stack Tecnológico

#### Core & IA

[![Python][python-shield]][python-url]
[![Streamlit][streamlit-shield]][streamlit-url]
[![Pandas][pandas-shield]][pandas-url]

#### Automatización & Data

[![Make][make-shield]][make-url]
[![AppSheet][appsheet-shield]][appsheet-url]
[![Google Sheets][google-sheets-shield]][google-sheets-url]

#### Herramientas de Desarrollo

[![Ruff][ruff-shield]][ruff-url]
[![Visual Studio Code][visual-studio-code-shield]][visual-studio-code-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Empezando

### Prerrequisitos

* [![uv][uv-shield]][uv-url] instalado en el sistema.

### Instalación

1. Clonar el repositorio

   ```bash
   git clone https://github.com/jpcadena/territoria.git
    ```

2. Instalar dependencias y sincronizar el entorno

    ```bash
    uv sync
    ```

3. Ejecutar la aplicación

    ```bash
    uv run streamlit run app.py
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Configuración

Para garantizar la seguridad de los datos y la portabilidad del código, este proyecto utiliza **Streamlit Secrets**.

### Desarrollo Local

Cree un archivo en la raíz del proyecto siguiendo la ruta `.streamlit/secrets.toml`. Este archivo está excluido del control de versiones para proteger sus credenciales:

```toml
CSV_URL = "https://docs.google.com/spreadsheets/d/e/.csv"
APP_ID = "tu-app-id-de-appsheet"
```

### Producción (Streamlit Cloud)

Para el despliegue en la nube, Streamlit Community Cloud gestiona las variables de entorno de forma segura a través de su propia bóveda de secretos cifrados.

1. Acceda al panel de su aplicación en [share.streamlit.io](https://share.streamlit.io).
2. Diríjase a **Settings > Secrets**.
3. Pegue sus credenciales respetando el formato TOML:

   ```toml
   CSV_URL = "https://docs.google.com/spreadsheets/d/e/.csv"
   APP_ID = "tu-app-id-de-appsheet"
   ```

## Despliegue

Este proyecto está optimizado para un despliegue ágil en **Streamlit Community Cloud**. Siga estos pasos para poner su dashboard en producción:

1. **Fork del Repositorio**: Realice un fork de este proyecto a su cuenta personal de GitHub.
2. **Nueva Aplicación**: Acceda a [share.streamlit.io](https://share.streamlit.io) y cree una nueva aplicación vinculando su fork.
3. **Entrypoint**: Asegúrese de que el archivo de entrada sea `src/territoria/sessions/session_5.py`.
4. **Configuración de Secrets**: Antes del despliegue final, vaya a **Advanced Settings > Secrets** y pegue sus variables de entorno:

   ```toml
   CSV_URL = "https://docs.google.com/spreadsheets/d/e/.csv"
   APP_ID = "tu-app-id-de-appsheet"
   ```

5. **Lanzamiento**: Haga clic en **Deploy**. La aplicación estará lista en un par de minutos.

## Licencia

Distribuido bajo la Licencia MIT. Consulte el archivo LICENSE para obtener más detalles sobre el uso y distribución del código.

## Contacto

[![Outlook][outlook-shield]](mailto:jpcadena@espol.edu.ec?subject=[GitHub]territoria)

[outlook-shield]: https://img.shields.io/badge/Microsoft_Outlook-0078D4?style=for-the-badge&logo=microsoft-outlook&logoColor=white
[uv-shield]: https://img.shields.io/badge/uv-toolkit-blue?logo=uv&style=flat-square
[uv-url]: https://docs.astral.sh/uv/getting-started/installation/
[python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[visual-studio-code-shield]: https://img.shields.io/badge/Visual_Studio_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white
[visual-studio-code-url]: https://code.visualstudio.com/
[ruff-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json
[ruff-url]: https://beta.ruff.rs/docs/
[streamlit-shield]: https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white
[streamlit-url]: https://streamlit.io/
[pandas-shield]: https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[pandas-url]: https://pandas.pydata.org/
[google-sheets-shield]: https://img.shields.io/badge/Google%20Sheets-%2334A853?style=for-the-badge&logo=googlesheets&logoColor=white
[google-sheets-url]: https://docs.google.com/spreadsheets/create
[make-url]: https://www.make.com/en
[make-shield]: https://img.shields.io/badge/Make.com-4353FF?style=for-the-badge&logo=make&logoColor=white
[appsheet-shield]: https://img.shields.io/badge/AppSheet-4285F4?style=for-the-badge&logo=appsheet&logoColor=white
[appsheet-url]: https://www.appsheet.com
