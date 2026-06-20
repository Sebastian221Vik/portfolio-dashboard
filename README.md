# Portfolio Analytics Dashboard

Aplicación web interactiva para el análisis y seguimiento de portafolios de inversión utilizando datos reales del mercado.

---

## Introducción

Este proyecto es una herramienta que permite analizar de forma visual y detallada cómo se comportaría un portafolio de inversiones compuesto por acciones, ETFs o criptomonedas.

Su objetivo es ayudar al usuario a entender el rendimiento histórico, el riesgo y las posibles tendencias futuras de su portafolio de manera sencilla e interactiva.

---

## Conceptos Financieros

### ¿Qué es un Portafolio?

Un portafolio es el conjunto de diferentes activos (acciones de empresas, criptomonedas, etc.) en los que inviertes tu dinero. En lugar de poner todo en una sola empresa, se distribuye en varios para reducir riesgos.

### Métricas Explicadas

**Retorno Total**  
Es el porcentaje de ganancia o pérdida que tuvo el portafolio en el período seleccionado.  
Ejemplo: Un retorno de +30% significa que por cada $100 invertidos, se obtuvieron $30 de ganancia.

**Volatilidad Anual**  
Mide cuánto varía (sube y baja) el valor del portafolio. Representa el **riesgo**.  
Mientras más baja sea la volatilidad, más estable es el portafolio.

**Sharpe Ratio**  
Mide la relación entre el retorno obtenido y el riesgo asumido.

- Mayor a 1.0 → Considerado bueno
- Mayor a 2.0 → Excelente  
  Es una de las métricas más importantes para evaluar si vale la pena el riesgo.

**Max Drawdown (Máxima Caída)**  
Es la mayor pérdida que habría sufrido el portafolio desde su punto más alto hasta su punto más bajo.  
Ejemplo: -25% significa que en algún momento se perdió el 25% del valor.  
Mientras más cerca de 0% esté, mejor.

---

## Funcionamiento del Dashboard

1. El usuario selecciona los activos que quiere analizar.
2. Asigna un porcentaje de inversión (peso) a cada activo.
3. Elige el período de tiempo.
4. El sistema descarga datos históricos reales y calcula:
    - El rendimiento del portafolio completo (ponderado por los porcentajes)
    - Todas las métricas financieras
    - Gráficos interactivos

### Predicción con Machine Learning

En la sección "Predicción ML" se utiliza un modelo de **Regresión Lineal** para estimar el precio futuro de un activo seleccionado durante los próximos 30 días.  
**Nota importante**: Esta predicción es educativa y no debe usarse como consejo financiero.

---

## Tecnologías Utilizadas

- **Python**
- **Streamlit** - Framework para crear aplicaciones web
- **yfinance** - Obtención de datos financieros en tiempo real
- **Pandas** - Procesamiento y análisis de datos
- **Plotly** - Gráficos interactivos
- **scikit-learn** - Implementación del modelo de Machine Learning

---

## Estructura del Proyecto

portfolio-dashboard/
├── app.py # Código principal de la aplicación
├── README.md # Documentación del proyecto
└── venv/ # Entorno virtual (no incluir en repositorios)
text---

## Instalación y Ejecución

### Requisitos

- Python 3.9 o superior

### Pasos de Instalación

1. Descarga o clona el proyecto.

2. Abre una terminal en la carpeta del proyecto y crea un entorno virtual:
    ```bash
    python -m venv venv
    ```

Activa el entorno virtual:
Windows: venv\Scripts\activate

Instala las dependencias:Bashpip install streamlit yfinance pandas plotly numpy scikit-learn
Ejecuta la aplicación:Bashstreamlit run app.py

Cómo Usar la Aplicación

En la barra lateral selecciona los activos que deseas analizar.
Elige un Benchmark de comparación (S&P 500 recomendado).
Ajusta los porcentajes de cada activo (deben sumar cerca de 100%).
Selecciona las fechas de inicio y fin.
Presiona el botón "Cargar Datos".

Explora las distintas pestañas:

Precios Normalizados: Compara el rendimiento de los activos desde una base de 100.
Retornos: Evolución del portafolio completo.
Distribución: Gráfico de cómo está repartido el dinero.
Correlaciones: Muestra cómo se mueven juntos o en direcciones opuestas los activos.
Detalles: Tablas de rendimiento y opción para descargar los datos.
Predicción ML: Predicción simple a 30 días.

Decisiones Técnicas

Se implementó caché de datos (@st.cache_data) para mejorar el rendimiento.
Los cálculos se realizan utilizando precios de cierre.
Se usan precios normalizados para poder comparar activos con precios muy diferentes.
El modelo de Machine Learning es intencionalmente simple para fines educativos.

Limitaciones

Los datos provienen de Yahoo Finance y pueden tener pequeños retrasos.
El modelo predictivo es básico y no considera noticias ni eventos económicos.
No se incluyen comisiones ni impuestos.
