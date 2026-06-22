import pandas as pd
import random
from datetime import datetime, timedelta

def generate_ipdr(suspect_number, num_records=500):
    start_date = datetime(2024, 3, 1)
    
    suspicious_sites = [
        'telegram.org', 'protonmail.com', 'nordvpn.com',
        'binance.com', 'localbitcoins.com', 'hawala.com',
        'onion.to', 'tor2web.org'
    ]
    
    normal_sites = [
        'google.com', 'youtube.com', 'facebook.com',
        'instagram.com', 'whatsapp.com', 'amazon.in',
        'flipkart.com', 'hotstar.com', 'twitter.com'
    ]
    
    apps = [
        'WhatsApp', 'Telegram', 'Signal', 'Chrome',
        'YouTube', 'Instagram', 'PhonePe', 'GPay',
        'Paytm', 'BHIM', 'TeamViewer', 'AnyDesk'
    ]
    
    suspicious_apps = ['TeamViewer', 'AnyDesk', 'Telegram', 'Signal']
    
    records = []
    
    for _ in range(num_records):
        timestamp = start_date + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        is_suspicious = random.random() < 0.3
        
        if is_suspicious:
            site = random.choice(suspicious_sites)
            app = random.choice(suspicious_apps)
            data_mb = random.uniform(10, 500)
        else:
            site = random.choice(normal_sites)
            app = random.choice(apps)
            data_mb = random.uniform(0.1, 50)
        
        records.append({
            'phone_number':     suspect_number,
            'timestamp':        timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'site_visited':     site,
            'app_used':         app,
            'data_used_mb':     round(data_mb, 2),
            'session_duration': random.randint(1, 120),
            'vpn_detected':     random.random() < 0.2,
            'ip_address':       f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        })
    
    df = pd.DataFrame(records)
    df.to_csv('data/mock_ipdr.csv', index=False)
    print(f"Generated {len(df)} IPDR records for {suspect_number}")
    return df

if __name__ == '__main__':
    generate_ipdr('9876543210')
