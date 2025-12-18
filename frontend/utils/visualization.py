import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def display_histogram(image, mode: str = "interactive"):
    """Affiche l'histogramme d'une image avec Plotly avec échelle logarithmique optionnelle"""
    img_array = np.array(image)
    
    if mode == "simple":
        sns.set_style("whitegrid")
        fig, ax = plt.subplots(figsize=(12, 5))
        if len(img_array.shape) == 2:
            ax.hist(img_array.ravel(), bins=256, color='gray', alpha=0.7, edgecolor='black', linewidth=0.5)
            ax.set_title("Histogramme (Niveaux de gris)", fontsize=14, fontweight='bold')
        else:
            colors = ['red', 'green', 'blue']
            for i, color in enumerate(colors):
                ax.hist(img_array[:,:,i].ravel(), bins=256, color=color, alpha=0.4, label=color.capitalize(), edgecolor=color, linewidth=0.3)
            ax.set_title("Histogramme RGB", fontsize=14, fontweight='bold')
            ax.legend(loc='upper right')
        ax.set_xlabel("Valeur de pixel (0-255)", fontsize=11)
        ax.set_ylabel("Fréquence", fontsize=11)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        # Mode interactif avec Plotly
        fig = go.Figure()
        
        if len(img_array.shape) == 2:
            hist, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
            # Normaliser pour éviter les pics extrêmes
            max_freq = np.max(hist)
            
            fig.add_trace(go.Bar(
                x=list(range(256)),
                y=hist,
                name='Intensité',
                marker_color='gray',
                opacity=0.7,
                hovertemplate='Valeur: %{x}<br>Fréquence: %{y}<extra></extra>'
            ))
            title = "Histogramme (Niveaux de gris)"
        else:
            colors = ['red', 'green', 'blue']
            color_names = ['Rouge', 'Vert', 'Bleu']
            max_freq = 0
            
            for i, (color, name) in enumerate(zip(colors, color_names)):
                hist, bins = np.histogram(img_array[:,:,i].flatten(), bins=256, range=[0, 256])
                max_freq = max(max_freq, np.max(hist))
                
                fig.add_trace(go.Scatter(
                    x=list(range(256)),
                    y=hist,
                    mode='lines',
                    name=name,
                    line=dict(color=color, width=2.5),
                    fill='tozeroy',
                    fillcolor=f'rgba({int(color=="red")*255}, {int(color=="green")*255}, {int(color=="blue")*255}, 0.15)',
                    hovertemplate=f'{name}<br>Valeur: %{{x}}<br>Fréquence: %{{y}}<extra></extra>'
                ))
            title = "Histogramme RGB"
        
        # Améliorer l'échelle Y pour éviter les pics excessifs
        # Utiliser le 95ème percentile pour fixer la limite Y
        all_values = []
        if len(img_array.shape) == 2:
            hist, _ = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
            all_values = hist
        else:
            for i in range(3):
                hist, _ = np.histogram(img_array[:,:,i].flatten(), bins=256, range=[0, 256])
                all_values.extend(hist)
        
        # Calculer le 98ème percentile pour limiter l'axe Y
        y_max = np.percentile(all_values, 98) * 1.1
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=20, color='#111827', family='Arial Black')
            ),
            # Axis styling (titles configured via *_title and *_title_font)
            xaxis=dict(
                gridcolor='rgba(200, 200, 200, 0.3)',
                showgrid=True,
                zeroline=True,
                range=[0, 255],
                tickfont=dict(color='#000000', size=12)
            ),
            yaxis=dict(
                gridcolor='rgba(200, 200, 200, 0.3)',
                showgrid=True,
                zeroline=True,
                range=[0, y_max],  # Limiter l'axe Y au 98ème percentile
                tickfont=dict(color='#000000', size=12)
            ),
            xaxis_title="Valeur de pixel (0-255)",
            xaxis_title_font=dict(size=14, color='#000000'),
            yaxis_title="Fréquence",
            yaxis_title_font=dict(size=14, color='#000000'),
            height=450,
            showlegend=True,
            hovermode='x unified',
            plot_bgcolor='#ffffff',
            paper_bgcolor='white',
            font=dict(color='#111827', family='Arial'),
            margin=dict(l=60, r=40, t=60, b=60),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='gray',
                borderwidth=1
            )
        )
        
        return fig
