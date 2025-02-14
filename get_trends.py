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

def get_region_code(region):
    """
    Mendapatkan kode region untuk Google Trends
    """
    region_codes = {
        'indonesia': {'code': 'indonesia', 'name': 'Indonesia'},
        'dunia': {'code': 'global', 'name': 'Dunia'},
        'amerika': {'code': 'united_states', 'name': 'Amerika Serikat'},
    }
    
    return region_codes.get(region.lower(), region_codes['indonesia'])

def get_global_trends(pytrends, limit=20):
    """
    Mengambil trend global dengan menggabungkan trend dari beberapa sumber
    """
    # Daftar negara dengan kode yang benar untuk trending_searches
    countries = {
        'united_states': 'Amerika Serikat',
        'india': 'India',
        'japan': 'Jepang',
        'singapore': 'Singapura',
        'australia': 'Australia',
        'canada': 'Kanada'
    }
    
    all_trends = []
    print("\nMengambil trend dari beberapa negara:")
    
    for country_code, country_name in countries.items():
        try:
            print(f"- Mencoba {country_name}...")
            trending_searches_df = pytrends.trending_searches(pn=country_code)
            if not trending_searches_df.empty:
                # Ambil 5 trend teratas dari setiap negara
                top_trends = trending_searches_df.head(5)
                all_trends.extend(top_trends.values.flatten())
                print(f"  ✓ Berhasil mendapatkan {len(top_trends)} trend")
        except Exception as e:
            print(f"  ✗ Gagal: {str(e)}")
            continue
    
    # Jika masih tidak ada trend, kembalikan DataFrame kosong
    if not all_trends:
        print("\nTidak ada trend yang berhasil diambil dari semua negara.")
        return pd.DataFrame(columns=['Keyword'])
    
    print(f"\nTotal trend mentah: {len(all_trends)}")
    
    # Hapus duplikat
    all_trends = list(dict.fromkeys(all_trends))
    print(f"Total trend setelah hapus duplikat: {len(all_trends)}")
    
    # Buat DataFrame
    df = pd.DataFrame(all_trends[:limit], columns=['Keyword'])
    return df

def get_top_trends(region='indonesia', limit=20):
    """
    Mengambil trend teratas dari Google Trends
    """
    try:
        # Dapatkan kode region
        region_info = get_region_code(region)
        
        # Inisialisasi pytrends dengan bahasa yang sesuai
        if region.lower() in ['dunia', 'amerika']:
            pytrends = TrendReq(hl='en-US', tz=420)
        else:
            pytrends = TrendReq(hl='id-ID', tz=420)
        
        # Mengambil trending searches berdasarkan region
        if region.lower() == 'dunia':
            df = get_global_trends(pytrends, limit)
        else:
            trending_searches_df = pytrends.trending_searches(pn=region_info['code'])
            df = pd.DataFrame(trending_searches_df)
            df.columns = ['Keyword']
        
        # Filter konten temporer
        df = df[~df['Keyword'].apply(is_temporary_content)]
        
        # Reset index mulai dari 1
        df.index = range(1, len(df) + 1)
        
        return df, region_info
        
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data dari Google Trends:")
        print(f"Error: {str(e)}")
        return None, None

def save_to_markdown(df, region_info, filename=None):
    """
    Menyimpan hasil ke file markdown
    """
    if df is None:
        return
        
    if filename is None:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        region_code = region_info['code'].lower()
        filename = f"trends_{region_code}_{current_time}.md"
    
    current_datetime = datetime.now().strftime("%d %B %Y %H:%M:%S")
    
    # Buat konten markdown
    markdown_content = f"""# Trend Google {region_info['name']}

> Diperbarui: {current_datetime}

## Ringkasan
- Total trend: {len(df)}
- Region: {region_info['name']}
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
    markdown_content += f"_Data diambil dari Google Trends {region_info['name']} (sudah difilter dari konten olahraga dan temporer)_\n"
    
    # Simpan ke file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Hasil telah disimpan ke file: {filename}")

def main():
    # Tampilkan pilihan region
    print("\nPilih region untuk trend:")
    print("1. Indonesia")
    print("2. Dunia")
    print("3. Amerika")
    
    # Minta input dari user
    choice = input("\nMasukkan pilihan (1-3, default: 1): ").strip()
    
    # Tentukan region berdasarkan pilihan
    region_map = {
        '1': 'indonesia',
        '2': 'dunia',
        '3': 'amerika'
    }
    
    region = region_map.get(choice, 'indonesia')
    
    print(f"\nMengambil trend dari Google Trends {region.title()}...")
    print("(Mengecualikan berita olahraga dan konten temporer)")
    
    trends_df, region_info = get_top_trends(region=region)
    
    if trends_df is not None:
        total_trends = len(trends_df)
        print(f"\n=== {total_trends} TREND DI {region_info['name'].upper()} ===")
        print("(Sudah difilter dari konten olahraga dan temporer)")
        print(trends_df)
        
        # Simpan ke file markdown
        save_to_markdown(trends_df, region_info)
    else:
        print("\nTidak ada data yang berhasil diambil.")

if __name__ == "__main__":
    main() 