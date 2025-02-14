from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
import re

def is_temporary_content(keyword):
    """
    Mengecek apakah sebuah keyword adalah konten yang cepat basi
    """
    # Pattern untuk mendeteksi konten yang cepat basi
    temporary_patterns = [
        r'vs\.?|versus',           # Pertandingan
        r'skor|score',             # Skor pertandingan
        r'hasil pertandingan',     # Hasil pertandingan
        r'liga|league',            # Liga olahraga
        r'klasemen',               # Klasemen pertandingan
        r'final|semifinal',        # Babak final/semifinal
        r'jadwal',                 # Jadwal pertandingan
        r'live\s?score',           # Live score
        r'streaming',              # Streaming pertandingan
        r'kode\s?redeem',         # Kode redeem game
        r'prediksi',              # Prediksi pertandingan
        r'fc$|fc\s',              # Football Club
        r'united$|united\s',      # Tim dengan nama United
        r'city$|city\s',         # Tim dengan nama City
    ]
    
    # Daftar tim dan liga olahraga populer
    sports_teams = [
        'madrid', 'barcelona', 'liverpool', 'chelsea', 'arsenal',
        'juventus', 'milan', 'inter', 'bayern', 'dortmund',
        'psg', 'benfica', 'porto', 'persib', 'persija',
        'arema', 'psim', 'persebaya'
    ]
    
    # Ubah keyword menjadi lowercase untuk pengecekan
    keyword_lower = keyword.lower()
    
    # Cek pattern temporary content
    for pattern in temporary_patterns:
        if re.search(pattern, keyword_lower):
            return True
            
    # Cek nama tim olahraga
    for team in sports_teams:
        if team in keyword_lower:
            return True
            
    return False

def get_top_trends(region='indonesia', limit=20):
    """
    Mengambil trend teratas dari Google Trends
    """
    try:
        # Inisialisasi pytrends
        pytrends = TrendReq(hl='id-ID', tz=420)
        
        # Mengambil trending searches
        trending_searches_df = pytrends.trending_searches(pn=region.lower())
        df = pd.DataFrame(trending_searches_df)
        df.columns = ['Keyword']
        
        # Filter konten temporer
        df = df[~df['Keyword'].apply(is_temporary_content)]
        
        # Reset index mulai dari 1
        df.index = range(1, len(df) + 1)
        
        return df
        
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data dari Google Trends:")
        print(f"Error: {str(e)}")
        return None

def save_to_markdown(df, filename=None):
    """
    Menyimpan hasil ke file markdown
    """
    if df is None:
        return
        
    if filename is None:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"trends_{current_time}.md"
    
    current_datetime = datetime.now().strftime("%d %B %Y %H:%M:%S")
    
    # Buat konten markdown
    markdown_content = f"""# Trend Google Indonesia

> Diperbarui: {current_datetime}

## Ringkasan
- Total trend: {len(df)}
- Catatan: Tidak termasuk berita olahraga dan konten temporer

## Daftar Trend

| No. | Keyword |
|-----|---------|
"""
    
    # Tambahkan setiap trend ke tabel
    for idx, row in df.iterrows():
        markdown_content += f"| {idx} | {row['Keyword']} |\n"
    
    # Tambahkan catatan kaki
    markdown_content += "\n\n---\n"
    markdown_content += "_Data diambil dari Google Trends Indonesia (sudah difilter dari konten olahraga dan temporer)_\n"
    
    # Simpan ke file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Hasil telah disimpan ke file: {filename}")

def main():
    print("Mengambil trend dari Google Trends Indonesia...")
    print("(Mengecualikan berita olahraga dan konten temporer)")
    
    trends_df = get_top_trends(region='indonesia')
    
    if trends_df is not None:
        total_trends = len(trends_df)
        print(f"\n=== {total_trends} TREND DI INDONESIA ===")
        print("(Sudah difilter dari konten olahraga dan temporer)")
        print(trends_df)
        
        # Simpan ke file markdown
        save_to_markdown(trends_df)
    else:
        print("\nTidak ada data yang berhasil diambil.")

if __name__ == "__main__":
    main() 