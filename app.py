import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Sayfa Ayarları
st.set_page_config(page_title="Endüstriyel Verimlilik Analizörü", layout="wide")

st.title("📊 Endüstriyel Verimlilik (OEE) Dashboard'u")
st.markdown("_Endüstri Mühendisliği Karar Destek Sistemi_")
st.markdown("---")

# 2. Yan Panel Girişleri
with st.sidebar:
    st.header("⚙️ Üretim Parametreleri")
    vardiya = st.number_input("Vardiya Süresi (Dakika)", value=480)
    durus = st.number_input("Planlı Duruşlar (Dakika)", value=60)
    ideal_hiz = st.number_input("İdeal Çevrim (Saniye/Adet)", value=30)
    
    st.markdown("---")
    st.header("📈 Gerçekleşen Veriler")
    uretim = st.number_input("Toplam Üretim (Adet)", value=700)
    fire = st.number_input("Hatalı Ürün (Adet)", value=20)
    ariza = st.number_input("Arıza Süresi (Dakika)", value=40)

# 3. Hesaplamalar
net_sure = vardiya - durus
calisma_suresi = net_sure - ariza

# OEE Formülleri
kullanilabilirlik = (calisma_suresi / net_sure) * 100
performans = ((uretim * ideal_hiz) / (calisma_suresi * 60)) * 100
kalite = ((uretim - fire) / uretim) * 100
oee = (kullanilabilirlik/100) * (performans/100) * (kalite/100) * 100

# 4. Gösterge Paneli
c1, c2, c3, c4 = st.columns(4)
c1.metric("Kullanılabilirlik", f"%{kullanilabilirlik:.1f}")
c2.metric("Performans", f"%{performans:.1f}")
c3.metric("Kalite", f"%{kalite:.1f}")
c4.metric("OEE SKORU", f"%{oee:.1f}")

st.markdown("---")

# 5. Grafik ve Analiz
col_sol, col_sag = st.columns(2)

with col_sol:
    st.subheader("📊 Verimlilik Grafiği")
    data = pd.DataFrame({
        "Metrik": ["Kullanılabilirlik", "Performans", "Kalite"],
        "Yüzde": [kullanilabilirlik, performans, kalite]
    })
    fig = px.bar(data, x="Metrik", y="Yüzde", color="Metrik", range_y=[0,100], text_auto='.1f')
    st.plotly_chart(fig, use_container_width=True)

with col_sag:
    st.subheader("💡 Mühendislik Tavsiyesi")
    if oee < 85:
        st.error(f"OEE Hedefi (%85) Altında!")
        if kullanilabilirlik < 90:
            st.write("- **Bakım:** Arıza sürelerini azaltmak için Koruyucu Bakım (TPM) çalışmaları başlatılmalı.")
        if performans < 90:
            st.write("- **Metot:** Standart iş yönergeleri ve operatör çevrim süreleri optimize edilmeli.")
        if kalite < 98:
            st.write("- **Kalite:** Hata kaynağında kurutulmalı (Poka-Yoke sistemleri).")
    else:
        st.success("Sistem Dünya Standartlarında Çalışıyor!")

# 6. Raporu Dışa Aktarma Bölümü (DÜZELTİLDİ)
st.markdown("---")
st.subheader("📥 Analiz Raporunu İndir")

# İndirilecek veriyi hazırlıyoruz
detay_df = pd.DataFrame({
    "Metrik Adı": ["Kullanılabilirlik", "Performans", "Kalite", "Genel OEE Skoru", "Toplam Üretim", "Sağlam Ürün", "Fire Sayısı"],
    "Değer (%)": [
        f"{kullanilabilirlik:.2f}", 
        f"{performans:.2f}", 
        f"{kalite:.2f}", 
        f"{oee:.2f}", 
        str(uretim), 
        str(uretim - fire), 
        str(fire)
    ]
})

# CSV'ye dönüştürme işlemi
csv_verisi = detay_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📊 Mühendislik Raporunu CSV Olarak İndir",
    data=csv_verisi,
    file_name='uretim_verimlilik_raporu.csv',
    mime='text/csv',
)