import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker('en_IN')
random.seed(42)


# Generate phone number pools
scam_numbers = [
    '9876543210', '9876543211', '9876543212',
    '9876543213', '9876543214'
]

victim_numbers = [fake.numerify('9#########') for _ in range(200)]

normal_numbers = [fake.numerify('9#########') for _ in range(500)]

agencies = ['CBI', 'RBI', 'Customs', 'Police', 'ED', 'Income Tax']

towers = ['TWR_DEL_001', 'TWR_DEL_002', 'TWR_MUM_001', 
          'TWR_MUM_002', 'TWR_BLR_001', 'TWR_HYD_001',
          'TWR_CHN_001', 'TWR_KOL_001']

imei_pool = [fake.numerify('35######tattooine########') for _ in range(10)]


# Generate CDR data
def generate_cdr(num_records=1500):
    records = []
    start_date = datetime(2024, 1, 1)
    
    for _ in range(num_records):
        # 60% chance of scam call, 40% normal call
        if random.random() < 0.6:
            caller = random.choice(scam_numbers)
            receiver = random.choice(victim_numbers)
            duration = random.randint(300, 3600)
            tower = random.choice(towers[:4])
            imei = random.choice(imei_pool[:3])
        else:
            caller = random.choice(normal_numbers)
            receiver = random.choice(normal_numbers)
            duration = random.randint(10, 600)
            tower = random.choice(towers)
            imei = random.choice(imei_pool)
        
        timestamp = start_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(8, 20),
            minutes=random.randint(0, 59)
        )
        
        records.append({
            'caller_number': caller,
            'receiver_number': receiver,
            'call_duration_secs': duration,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'tower_id': tower,
            'imei': imei
        })
    
    return pd.DataFrame(records)



# Generate complaint data
def generate_complaints(num_records=200):
    records = []
    start_date = datetime(2024, 1, 1)
    
    for _ in range(num_records):
        # Pick mostly from victim numbers
        if random.random() < 0.8:
            victim = random.choice(victim_numbers)
        else:
            victim = fake.numerify('9#########')
        
        scammer = random.choice(scam_numbers)
        agency = random.choice(agencies)
        amount = random.choice([
            random.randint(10000, 50000),
            random.randint(50000, 200000),
            random.randint(200000, 1000000)
        ])
        
        complaint_date = start_date + timedelta(
            days=random.randint(0, 180)
        )
        
        records.append({
            'victim_number': victim,
            'scammer_number': scammer,
            'complaint_date': complaint_date.strftime('%Y-%m-%d'),
            'amount_lost_inr': amount,
            'agency_impersonated': agency,
            'complaint_status': random.choice(['Open', 'Under Investigation', 'Closed'])
        })
    
    return pd.DataFrame(records)




# Main function to generate and save data
def main():
    print("Generating CDR data...")
    cdr_df = generate_cdr(1500)
    
    print("Generating complaint data...")
    complaints_df = generate_complaints(200)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    cdr_df.to_csv('data/mock_cdr.csv', index=False)
    complaints_df.to_csv('data/mock_complaints.csv', index=False)
    
    print("CDR data saved to data/mock_cdr.csv")
    print("Complaints data saved to data/mock_complaints.csv")
    print(f"Total CDR records: {len(cdr_df)}")
    print(f"Total complaint records: {len(complaints_df)}")
    print("Done!")

if __name__ == '__main__':
    main()
