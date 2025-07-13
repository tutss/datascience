from PIL import Image

import pandas as pd
import requests
import whisper

import streamlit as st
from st_audiorec import st_audiorec
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt

from database_items import db_files


@st.cache_resource
def load_audio_model(model_name='small', device='cuda:0'):
    return whisper.load_model(model_name, device=device)


@st.cache_resource
def load_model(model_name='openai/clip-vit-base-patch32', device='cuda:0'):
    return CLIPModel.from_pretrained(model_name).to(device)


@st.cache_resource
def load_processor(model_name='openai/clip-vit-base-patch32'):
    return CLIPProcessor.from_pretrained(model_name)

@st.cache_data
def create_db(_image_processor):
    data = pd.DataFrame(columns=["tipo", "url", "img_embeddings"])
    for roupa in db_files:
        roupas = db_files[roupa]
        print(f"Processando {roupa}...")
        for url in roupas:
            image = Image.open(requests.get(url, stream=True).raw)
            roupa_emb = pd.Series(compute_image_embeddings(image, _image_processor).cpu().detach().numpy().squeeze())
            row = pd.DataFrame({"tipo": roupa, "url": url, "img_embeddings": [roupa_emb.values]})
            data = pd.concat([row, data], ignore_index=True)
    return data

def transcribe(audio_model, audio_file) -> str:
    result = audio_model.transcribe(audio_file)
    print(result)
    return result["text"]

def compute_text_embeddings(list_of_strings, processor, device='cuda:0'):
    inputs = processor(text=list_of_strings, return_tensors="pt", padding=True).to(device)
    return model.get_text_features(**inputs)

def compute_image_embeddings(image, processor, device='cuda:0'):
    inputs = processor(images=image, return_tensors="pt")["pixel_values"].to(device)
    return model.get_image_features(inputs)

def get_top_N_images(query, db, processor, top_K=3):
    query_vect = compute_text_embeddings([query], processor).cpu().detach().numpy()
    
    # Run similarity Search
    similarities = db["img_embeddings"].apply(lambda x: cosine_similarity(query_vect, [x]))
    sorted_similarities = similarities.sort_values(ascending=False)
    idxs = sorted_similarities.index[:top_K]

    return db.iloc[idxs]

def show_images(df, n_images):
    fig, axs = plt.subplots(1, n_images, figsize=(9,3))

    for item, ax in zip(df["url"], axs):
        image = Image.open(requests.get(item, stream=True).raw)
        ax.imshow(image)
        ax.axis('off')

    st.pyplot(fig)


if __name__ == "__main__":
    st.title("Welcome to Voice to Product!")
    model     = load_model()
    processor = load_processor()
    audio_model = load_audio_model()
    db = create_db(processor)

    wav_audio_data = st_audiorec()
    audio_file = 'microphone-results.wav'
    wrote = False
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')
        with open(audio_file, "wb") as f:
            f.write(wav_audio_data)
        wrote = True

    if wrote:
        result = transcribe(audio_model, audio_file)
        st.subheader(result)

        most_similar = get_top_N_images(result, db, processor)
        show_images(most_similar, 3)
        urls = ' '.join(most_similar['url'])
        types = ' '.join(most_similar['tipo'])
        st.text(f"Item URLs = ")
        for url, item_type in zip(urls.split(' '), types.split(' ')):
            st.markdown(f"    URL = [here]({url}), Item Type = {item_type}")

