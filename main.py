"""
Instagram Analytics Tools
Fitur: Follower Tracker, Monitor Pertumbuhan, Scraper Komentar & Like

Requirements:
pip install instaloader pandas matplotlib openpyxl

Note: Anda perlu login ke Instagram untuk menggunakan tools ini
"""

import instaloader
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os
from time import sleep

class InstagramTools:
    def __init__(self, username):
        self.L = instaloader.Instaloader()
        self.username = username
        self.data_folder = "instagram_data"
        
        # Buat folder untuk menyimpan data
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
    
    def login(self, username, password):
        """Login ke Instagram"""
        try:
            self.L.login(username, password)
            print(f"✓ Berhasil login sebagai {username}")
            return True
        except Exception as e:
            print(f"✗ Gagal login: {str(e)}")
            return False
    
    def load_session(self, session_username):
        """Load session yang sudah ada"""
        try:
            self.L.load_session_from_file(session_username)
            print(f"✓ Session berhasil dimuat untuk {session_username}")
            return True
        except Exception as e:
            print(f"✗ Gagal memuat session: {str(e)}")
            return False
    
    # ==================== FITUR 1: FOLLOWER TRACKER ====================
    def track_followers(self, target_username):
        """
        Track followers dan temukan siapa yang unfollow
        """
        print(f"\n Menganalisis followers dari @{target_username}...")
        
        try:
            profile = instaloader.Profile.from_username(self.L.context, target_username)
            
            # Ambil daftar followers saat ini
            current_followers = set()
            print("Mengambil daftar followers...")
            for follower in profile.get_followers():
                current_followers.add(follower.username)
                if len(current_followers) % 50 == 0:
                    print(f"  Progress: {len(current_followers)} followers...")
            
            # Path file untuk menyimpan data
            followers_file = f"{self.data_folder}/{target_username}_followers.json"
            
            # Load data sebelumnya jika ada
            if os.path.exists(followers_file):
                with open(followers_file, 'r') as f:
                    old_data = json.load(f)
                    old_followers = set(old_data['followers'])
                    
                # Analisis perubahan
                new_followers = current_followers - old_followers
                unfollowers = old_followers - current_followers
                
                print(f"\n✓ Analisis Selesai!")
                print(f"  Total followers sekarang: {len(current_followers)}")
                print(f"  New followers: {len(new_followers)}")
                print(f"  Unfollowers: {len(unfollowers)}")
                
                if new_followers:
                    print(f"\n👥 New Followers ({len(new_followers)}):")
                    for user in list(new_followers)[:10]:
                        print(f"   • @{user}")
                    if len(new_followers) > 10:
                        print(f"   ... dan {len(new_followers)-10} lainnya")
                
                if unfollowers:
                    print(f"\n Unfollowers ({len(unfollowers)}):")
                    for user in list(unfollowers)[:10]:
                        print(f"   • @{user}")
                    if len(unfollowers) > 10:
                        print(f"   ... dan {len(unfollowers)-10} lainnya")
                
                # Simpan hasil analisis
                result = {
                    'new_followers': list(new_followers),
                    'unfollowers': list(unfollowers),
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                with open(f"{self.data_folder}/{target_username}_changes.json", 'w') as f:
                    json.dump(result, f, indent=2)
            else:
                print(f"\n✓ Data pertama berhasil disimpan!")
                print(f"  Total followers: {len(current_followers)}")
                print(f"\n Jalankan lagi nanti untuk melihat perubahan followers")
            
            # Simpan data followers saat ini
            data = {
                'followers': list(current_followers),
                'count': len(current_followers),
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open(followers_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            return current_followers
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return None
    
    # ==================== FITUR 2: MONITOR PERTUMBUHAN ====================
    def monitor_growth(self, target_username):
        """
        Monitor pertumbuhan akun dan buat grafik
        """
        print(f"\n Monitoring pertumbuhan akun @{target_username}...")
        
        try:
            profile = instaloader.Profile.from_username(self.L.context, target_username)
            
            # Data statistik saat ini
            stats = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'followers': profile.followers,
                'following': profile.followees,
                'posts': profile.mediacount,
                'engagement_rate': 0
            }
            
            # Hitung engagement rate dari 12 post terakhir
            total_engagement = 0
            post_count = 0
            print("Menghitung engagement rate...")
            
            for post in profile.get_posts():
                if post_count >= 12:
                    break
                total_engagement += post.likes + post.comments
                post_count += 1
            
            if post_count > 0 and profile.followers > 0:
                avg_engagement = total_engagement / post_count
                stats['engagement_rate'] = (avg_engagement / profile.followers) * 100
            
            print(f"\n✓ Data statistik saat ini:")
            print(f"  Followers: {stats['followers']:,}")
            print(f"  Following: {stats['following']:,}")
            print(f"  Posts: {stats['posts']:,}")
            print(f"  Engagement Rate: {stats['engagement_rate']:.2f}%")
            
            # Simpan data historis
            history_file = f"{self.data_folder}/{target_username}_growth.json"
            
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            history.append(stats)
            
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            # Buat grafik jika ada data historis
            if len(history) > 1:
                self._create_growth_chart(target_username, history)
            else:
                print(f"\n Jalankan lagi nanti untuk melihat grafik pertumbuhan")
            
            return stats
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return None
    
    def _create_growth_chart(self, username, history):
        """Buat grafik pertumbuhan"""
        df = pd.DataFrame(history)
        df['date'] = pd.to_datetime(df['date'])
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Analisis Pertumbuhan @{username}', fontsize=16, fontweight='bold')
        
        # Grafik Followers
        axes[0, 0].plot(df['date'], df['followers'], marker='o', color='#E1306C', linewidth=2)
        axes[0, 0].set_title('Pertumbuhan Followers', fontweight='bold')
        axes[0, 0].set_xlabel('Tanggal')
        axes[0, 0].set_ylabel('Jumlah Followers')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Grafik Following
        axes[0, 1].plot(df['date'], df['following'], marker='o', color='#405DE6', linewidth=2)
        axes[0, 1].set_title('Pertumbuhan Following', fontweight='bold')
        axes[0, 1].set_xlabel('Tanggal')
        axes[0, 1].set_ylabel('Jumlah Following')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Grafik Posts
        axes[1, 0].plot(df['date'], df['posts'], marker='o', color='#5B51D8', linewidth=2)
        axes[1, 0].set_title('Jumlah Posts', fontweight='bold')
        axes[1, 0].set_xlabel('Tanggal')
        axes[1, 0].set_ylabel('Total Posts')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Grafik Engagement Rate
        axes[1, 1].plot(df['date'], df['engagement_rate'], marker='o', color='#FD1D1D', linewidth=2)
        axes[1, 1].set_title('Engagement Rate', fontweight='bold')
        axes[1, 1].set_xlabel('Tanggal')
        axes[1, 1].set_ylabel('Engagement Rate (%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        chart_file = f"{self.data_folder}/{username}_growth_chart.png"
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ Grafik disimpan: {chart_file}")
        plt.close()
    
    # ==================== FITUR 3: SCRAPER KOMENTAR & LIKE ====================
    def scrape_post_engagement(self, post_url, max_comments=100, max_likes=100):
        """
        Scrape komentar dan likes dari post tertentu
        """
        print(f"\n🔍 Scraping engagement dari post...")
        
        try:
            # Ekstrak shortcode dari URL
            shortcode = post_url.split('/')[-2] if post_url.endswith('/') else post_url.split('/')[-1]
            
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)
            
            print(f"\n Informasi Post:")
            print(f"  Owner: @{post.owner_username}")
            print(f"  Likes: {post.likes:,}")
            print(f"  Comments: {post.comments:,}")
            print(f"  Date: {post.date_local}")
            
            # Scrape Komentar
            comments_data = []
            print(f"\nMengambil komentar (max {max_comments})...")
            
            for i, comment in enumerate(post.get_comments()):
                if i >= max_comments:
                    break
                
                comments_data.append({
                    'username': comment.owner.username,
                    'text': comment.text,
                    'created_at': comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S"),
                    'likes': comment.likes_count if hasattr(comment, 'likes_count') else 0
                })
                
                if (i + 1) % 20 == 0:
                    print(f"  Progress: {i + 1} komentar...")
            
            # Scrape Likes
            likes_data = []
            print(f"\nMengambil likes (max {max_likes})...")
            
            for i, like in enumerate(post.get_likes()):
                if i >= max_likes:
                    break
                
                likes_data.append({
                    'username': like.username,
                    'full_name': like.full_name
                })
                
                if (i + 1) % 20 == 0:
                    print(f"  Progress: {i + 1} likes...")
            
            # Simpan hasil
            result = {
                'post_info': {
                    'url': post_url,
                    'owner': post.owner_username,
                    'likes_count': post.likes,
                    'comments_count': post.comments,
                    'caption': post.caption[:200] + '...' if len(post.caption) > 200 else post.caption,
                    'date': post.date_local.strftime("%Y-%m-%d %H:%M:%S")
                },
                'comments': comments_data,
                'likes': likes_data,
                'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Simpan ke JSON
            filename = f"{self.data_folder}/post_{shortcode}_engagement.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # Simpan ke Excel
            excel_filename = f"{self.data_folder}/post_{shortcode}_engagement.xlsx"
            with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
                pd.DataFrame(comments_data).to_excel(writer, sheet_name='Comments', index=False)
                pd.DataFrame(likes_data).to_excel(writer, sheet_name='Likes', index=False)
            
            print(f"\n✓ Data berhasil disimpan!")
            print(f"  JSON: {filename}")
            print(f"  Excel: {excel_filename}")
            print(f"\n Ringkasan:")
            print(f"  Total komentar diambil: {len(comments_data)}")
            print(f"  Total likes diambil: {len(likes_data)}")
            
            # Tampilkan sample komentar
            if comments_data:
                print(f"\n Sample Komentar:")
                for comment in comments_data[:5]:
                    print(f"  @{comment['username']}: {comment['text'][:50]}...")
            
            return result
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return None


# ==================== CARA PENGGUNAAN ====================
if __name__ == "__main__":
    print("="*60)
    print("    INSTAGRAM ANALYTICS TOOLS")
    print("="*60)
    
    # Inisialisasi
    tools = InstagramTools("your_username")
    
    # LOGIN (Pilih salah satu cara)
    # Cara 1: Login dengan username & password
    tools.login("username_anda", "password_anda")
    
    # Cara 2: Load session yang sudah ada (setelah login pertama kali)
    # tools.load_session("username_anda")
    
    print("\n" + "="*60)
    print("PILIH FITUR:")
    print("="*60)
    print("1. Follower Tracker - Track followers & temukan unfollowers")
    print("2. Monitor Pertumbuhan - Analisis pertumbuhan akun")
    print("3. Scraper Engagement - Scrape komentar & likes dari post")
    print("="*60)
    
    pilihan = input("\nPilih fitur (1/2/3): ")
    
    if pilihan == "1":
        username = input("Masukkan username target: ")
        tools.track_followers(username)
        
    elif pilihan == "2":
        username = input("Masukkan username target: ")
        tools.monitor_growth(username)
        
    elif pilihan == "3":
        post_url = input("Masukkan URL post Instagram: ")
        max_comments = int(input("Max komentar (default 100): ") or 100)
        max_likes = int(input("Max likes (default 100): ") or 100)
        tools.scrape_post_engagement(post_url, max_comments, max_likes)
    
    else:
        print("Pilihan tidak valid!")
    
    print("\n✓ Selesai!")
