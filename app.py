import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import io

def ghirri_style(image):
    # Converti in RGB se non lo è già
    img = image.convert("RGB")
    
    # Aumenta la luminosità (meno intenso per non bruciare i dettagli)
    brightness = ImageEnhance.Brightness(img)
    img = brightness.enhance(1.1)  # Aumento moderato della luminosità
    
    # Riduci leggermente il contrasto
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(0.9)  # Leggero abbassamento del contrasto
    
    # Riduci la saturazione
    color = ImageEnhance.Color(img)
    img = color.enhance(0.85)  # Colori pastello ma non troppo sbiaditi
    
    # Applica un filtro per dare un aspetto morbido (sfocatura leggera)
    img = img.filter(ImageFilter.GaussianBlur(0.5))  # Sfocatura leggera
    
    # Aggiungi un leggero filtro di colore (viraggio pastello)
    np_img = np.array(img)
    filter_color = np.array([255, 230, 200])  # Un tono di pesca molto tenue
    
    # Mescola il filtro con l'immagine
    np_img = np_img * 0.95 + filter_color * 0.05  # Effetto pastello leggero
    np_img = np_img.clip(0, 255).astype(np.uint8)
    
    # Converti di nuovo in immagine Pillow
    img = Image.fromarray(np_img)
    
    # Aggiungi una leggera grana (rumore)
    noise = np.random.normal(0, 2, np_img.shape)  # Grana molto leggera
    noisy_img = np_img + noise
    noisy_img = noisy_img.clip(0, 255).astype(np.uint8)
    
    # Converti di nuovo in immagine Pillow
    img = Image.fromarray(noisy_img)
    
    return img

# Titolo dell'app Streamlit
st.title("Filtro Stile Ghirri per Immagini")

# Carica immagine da elaborare
uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Apri l'immagine con PIL
    img = Image.open(uploaded_file)
    
    # Mostra l'immagine originale
    st.image(img, caption="Immagine Originale", use_column_width=True)
    
    # Applica lo stile Ghirri
    processed_img = ghirri_style(img)
    
    # Mostra l'immagine elaborata
    st.image(processed_img, caption="Immagine con Filtro Stile Ghirri", use_column_width=True)
    
    # Salva l'immagine elaborata in un buffer
    buffer = io.BytesIO()
    processed_img.save(buffer, format="JPEG")
    buffer.seek(0)
    
    # Bottone per scaricare l'immagine
    st.download_button(
        label="Scarica immagine elaborata",
        data=buffer,
        file_name="ghirri_style.jpg",
        mime="image/jpeg"
    )

