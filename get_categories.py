from pytrends.request import TrendReq
import pandas as pd

def get_available_categories():
    """
    Mengambil dan menampilkan semua kategori yang tersedia di Google Trends
    """
    try:
        # Inisialisasi pytrends
        pytrends = TrendReq(hl='id-ID', tz=420)
        
        # Coba beberapa keyword dengan kategori berbeda
        keywords = ['berita', 'olahraga', 'hiburan', 'teknologi', 'bisnis']
        
        print("\nMencoba mendapatkan kategori untuk setiap keyword...")
        for keyword in keywords:
            print(f"\nKeyword: {keyword}")
            # Build payload dengan kategori 0 (all categories)
            pytrends.build_payload(
                kw_list=[keyword],
                cat=0,
                timeframe='today 12-m',
                geo='ID'
            )
            
            # Ambil interest over time untuk melihat kategori yang tersedia
            data = pytrends.interest_over_time()
            if not data.empty:
                print(f"- Berhasil mendapatkan data untuk '{keyword}'")
                print("- Kategori yang tersedia:")
                for col in data.columns:
                    if col != 'isPartial':
                        print(f"  * {col}")
            else:
                print(f"- Tidak ada data untuk '{keyword}'")
        
        print("\nMencoba mendapatkan trending searches per kategori...")
        # Coba beberapa ID kategori yang umum
        categories = {
            'All': '0',
            'Business': '12',
            'Entertainment': '3',
            'Health': '45',
            'Science': '8',
            'Sports': '15',
            'Technology': '5',
            'Top Stories': '1',
        }
        
        for cat_name, cat_id in categories.items():
            print(f"\nKategori: {cat_name} (ID: {cat_id})")
            try:
                # Build payload dengan kategori spesifik
                pytrends.build_payload(
                    kw_list=[''],
                    cat=cat_id,
                    timeframe='today 12-m',
                    geo='ID'
                )
                print(f"- Berhasil build payload untuk {cat_name}")
            except Exception as e:
                print(f"- Error untuk {cat_name}: {str(e)}")
        
    except Exception as e:
        print(f"Error umum: {str(e)}")

if __name__ == "__main__":
    print("Mengambil informasi kategori dari Google Trends...")
    get_available_categories() 