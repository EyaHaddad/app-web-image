import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def display_histogram(image, mode: str = "interactive"):
    """Affiche l'histogramme d'une image avec Plotly"""
    img_array = np.array(image)
    
    if mode == "simple":
        fig, ax = plt.subplots(figsize=(10, 4))
        if len(img_array.shape) == 2:
            ax.hist(img_array.ravel(), bins=256, color='gray', alpha=0.7)
            ax.set_title("Histogramme (Niveaux de gris)")
        else:
            colors = ['red', 'green', 'blue']
            for i, color in enumerate(colors):
                ax.hist(img_array[:,:,i].ravel(), bins=256, color=color, alpha=0.5, label=color)
            ax.set_title("Histogramme RGB")
            ax.legend()
        ax.set_xlabel("Valeur de pixel")
        ax.set_ylabel("Fréquence")
        st.pyplot(fig)
    else:
        # Mode interactif avec Plotly
        fig = go.Figure()
        
        if len(img_array.shape) == 2:
            hist, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
            fig.add_trace(go.Bar(
                x=list(range(256)),
                y=hist,
                name='Intensité',
                marker_color='gray',
                opacity=0.7
            ))
            title = "Histogramme (Niveaux de gris)"
        else:
            colors = ['red', 'green', 'blue']
            color_names = ['Rouge', 'Vert', 'Bleu']
            for i, (color, name) in enumerate(zip(colors, color_names)):
                hist, bins = np.histogram(img_array[:,:,i].flatten(), bins=256, range=[0, 256])
                fig.add_trace(go.Scatter(
                    x=list(range(256)),
                    y=hist,
                    mode='lines',
                    name=name,
                    line=dict(color=color, width=2),
                    fill='tozeroy',
                    fillcolor=f'rgba({int(color=="red")*255}, {int(color=="green")*255}, {int(color=="blue")*255}, 0.1)'
                ))
            title = "Histogramme RGB"
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=20, color='var(--dark)')
            ),
            xaxis_title="Valeur de pixel (0-255)",
            yaxis_title="Fréquence",
            height=350,
            showlegend=True,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='var(--dark)'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
