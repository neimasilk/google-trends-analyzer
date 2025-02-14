from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
import time

def get_tech_trends(limit=30):
    """
    Mengambil trend teknologi dari Google Trends
    """
    try:
        # Inisialisasi pytrends
        pytrends = TrendReq(hl='id-ID', tz=420)
        
        # List untuk menyimpan semua trend
        all_trends = []
        
        # Timeframes yang berbeda untuk mendapatkan lebih banyak variasi
        timeframes = [
            'today 1-m',
            'today 3-m',
            'today 12-m'
        ]
        
        # Keywords teknologi untuk mendapatkan related queries
        tech_keywords = [
            'teknologi',
            'aplikasi',
            'smartphone',
            'software',
            'digital'
        ]
        
        for timeframe in timeframes:
            print(f"\nMengambil data untuk timeframe: {timeframe}")
            
            for keyword in tech_keywords:
                print(f"- Mencoba keyword: {keyword}")
                try:
                    # Tunggu sebentar antara requests
                    time.sleep(2)
                    
                    # Build payload dengan kategori teknologi
                    pytrends.build_payload(
                        kw_list=[keyword],
                        cat=5,  # ID kategori Technology
                        timeframe=timeframe,
                        geo='ID'
                    )
                    
                    # Ambil related queries
                    related = pytrends.related_queries()
                    if related and keyword in related and related[keyword]['top'] is not None:
                        df = related[keyword]['top']
                        df['timeframe'] = timeframe
                        df['source_keyword'] = keyword
                        all_trends.append(df)
                        
                except Exception as e:
                    print(f"  Error untuk {keyword}: {str(e)}")
                    continue
        
        if all_trends:
            # Gabungkan semua hasil
            final_df = pd.concat(all_trends, ignore_index=True)
            
            # Rename kolom
            final_df.columns = ['Keyword', 'Score', 'Timeframe', 'Source']
            
            # Hapus duplikat
            final_df = final_df.drop_duplicates(subset=['Keyword'])
            
            # Urutkan berdasarkan score
            final_df = final_df.sort_values('Score', ascending=False)
            
            # Ambil sejumlah limit yang diminta
            final_df = final_df.head(limit)
            
            # Reset index
            final_df.index = range(1, len(final_df) + 1)
            
            return final_df
            
        return None
        
    except Exception as e:
        print(f"Error umum: {str(e)}")
        return None

def save_to_markdown(df, filename=None):
    """
    Menyimpan hasil ke file markdown
    """
    if df is None:
        return
        
    if filename is None:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tech_trends_{current_time}.md"
    
    current_datetime = datetime.now().strftime("%d %B %Y %H:%M:%S")
    
    # Buat konten markdown
    markdown_content = f"""# Trend Teknologi di Indonesia

> Diperbarui: {current_datetime}

## Ringkasan
- Total trend: {len(df)}
- Timeframes: {', '.join(sorted(df['Timeframe'].unique()))}
- Keywords: {', '.join(sorted(df['Source'].unique()))}

## Daftar Trend

| No. | Keyword | Score | Timeframe | Source |
|-----|---------|-------|-----------|---------|
"""
    
    # Tambahkan setiap trend ke tabel
    for idx, row in df.iterrows():
        markdown_content += f"| {idx} | {row['Keyword']} | {row['Score']} | {row['Timeframe']} | {row['Source']} |\n"
    
    # Tambahkan catatan kaki
    markdown_content += "\n\n---\n"
    markdown_content += "_Data diambil dari Google Trends Indonesia - Kategori Teknologi_\n"
    
    # Simpan ke file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Hasil telah disimpan ke file: {filename}")

def main():
    print("Mengambil trend teknologi dari Google Trends Indonesia...")
    
    trends_df = get_tech_trends(limit=30)
    
    if trends_df is not None:
        print("\n=== TREND TEKNOLOGI DI INDONESIA ===")
        print(trends_df)
        
        # Simpan ke file markdown
        save_to_markdown(trends_df)
    else:
        print("\nTidak ada data yang berhasil diambil.")

if __name__ == "__main__":
    main() 