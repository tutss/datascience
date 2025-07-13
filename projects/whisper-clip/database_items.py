import streamlit as st

db_files = {
    "blusa": [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSd8s6klk83uiiGi96lTl7_nnoxeoR7cFxCioJn_NIVrcsQ5epL-tiUlM6shrz8-qrhEZ4&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCKD2g8TYTv5RAk_Ck47gSnCjYVZGGMZMbvAtS0J396-Pxo1AtZa3ITXG8AlY2k7Cu8o&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdx9ja1BmqLSuerAPscyvqL5tNOidDS6bdmQale3km2U27hR_v6ldOW7smuetNYM2_NjE&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTamaPf4zfc7t-F7HyTK25JCf-B-hFXaWLpsmmIbQhXftmGXYFE6wnOiVYAyx5rNJuWzVo&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6iZ70MSJGwBtwHnOkXJwKoyUm8OSi5-C7cDt2KtjLwe8UtvSPrvrJpeTPeR9IT4kA0r0&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRISkK44iAvXfM2Lf3GjuVcGjqJWuU3ghITPk-j1SoOkLzSZKiyFKIB9aZIIY_d0nNrr6c&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvl9iCMkNRk67ooAA8g35gAXr0mpnhG_IFWJw1o20dh4kmt3wK_j9GSkIHaQs75NKmgLg&usqp=CAU"
    ],
    "calca": [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNclrZobuYRy-N2wr6t0z5aZdvHVUHIfNGGw&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLZVDFtiby3Qw-6w5f-WA9e1QAQ0wHR-54R1LgxQwhB3gcQaZa2HwWC5tDxK2C3fPKVu8&usqp=CAU",
        "https://cdn.awsli.com.br/600x700/809/809422/produto/39732279/b34e774923.jpg",
        "https://cdn.awsli.com.br/600x1000/622/622351/produto/54302663/1-57mg2y5pku.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9fe_sXHursYxzKlO5-COHAdrb8whUvotIMndTUgGlJlHAUmkEjjU5qM-_poLo00EVCzk&usqp=CAU",
        "https://images.tcdn.com.br/img/img_prod/952230/calca_masculina_alfaiataria_sarja_slim_marrom_2677_1_07c600b012552131b3eac41440927779.jpg",
    ],
    "tenis": [
        "https://assets.adidas.com/images/w_600,f_auto,q_auto/32c151dc88224a6f93b1af1200ec5a6a_9366/Tenis_Response_Runner_Preto_ID7336_01_standard.jpg",
        "https://imgcentauro-a.akamaihd.net/1366x1366/97360651A1.jpg",
        "https://m.media-amazon.com/images/I/41NzGgXXNtL._AC_.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJunUHQYimjlopx3ZaphqM_W9M-d-OI9nqGg&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdT9fg9YvaGBUaFofBNka8HjpTrpuYUAmgRg&usqp=CAU"
    ],
    "touca": [
        "https://m.media-amazon.com/images/I/41SWzu8V2qL._AC_SY1000_.jpg"
    ]
}


if __name__ == "__main__":
    st.title("Database")
    st.subheader("Items")
    st.write("Here you can find some items that we have in our database.")

    col1, col2, col3 = st.columns(3)

    with col1:
        calcas = db_files["calca"]
        for calca in calcas:
            st.image(calca)

    with col2:
        blusas = db_files["blusa"]
        for blusa in blusas:
            st.image(blusa)

    with col3:
        tenis = db_files["tenis"]
        for tenis in tenis:
            st.image(tenis)