import streamlit as st

def main():
    # Page configuration
    st.set_page_config(
        page_title="Análisis de Ventas Northwind", 
        page_icon="📊", 
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-title {
        color: #2C3E50;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    .project-intro {
        background-color: #F0F2F6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Title
    st.markdown('<h1 class="main-title">📊 Análisis de Ventas Northwind</h1>', unsafe_allow_html=True)
    
    # Project Introduction
    st.markdown('<div class="project-intro">', unsafe_allow_html=True)
    st.markdown("""
    ## Introducción al Proyecto

    ### Objetivo
    Realizar un análisis detallado de las tendencias de ventas de la empresa Northwind utilizando técnicas avanzadas de visualización y análisis de datos.

    ### Contexto
    Este proyecto fue desarrollado como parte del curso de **Taller de Programación** bajo la supervisión del profesor Nayib Vargas, con el propósito de aplicar conocimientos de análisis de datos y programación.

    ### Metodología
    - **Herramientas utilizadas:** Python, Streamlit, Plotly
    - **Base de datos:** Northwind
    - **Técnicas de análisis:** Visualización de ventas, análisis por categorías y países
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Información Adicional
    st.subheader("Descripción del Proyecto")
    st.write("""
    En este proyecto, analizaremos la base de datos de Northwind para obtener insights sobre las ventas, 
    categorías de productos y distribución geográfica. Utilizaremos visualizaciones interactivas 
    y técnicas de análisis de datos para comprender mejor el rendimiento de la empresa.
    """)

    # Footer and Acknowledgments
    st.markdown("---")
    st.markdown("""
   
    **Desarrollado por: Dunia Picado Navarro**
    *Taller de Programación - 2024*
    """)

if __name__ == "__main__":
    main()