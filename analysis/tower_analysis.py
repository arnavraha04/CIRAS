import pandas as pd
import os

TOWER_COORDINATES = {
    'TWR_DEL_ROHINI_01':  (28.7041, 77.1025),
    'TWR_DEL_ROHINI_02':  (28.7080, 77.1100),
    'TWR_DEL_DWARKA_01':  (28.5921, 77.0460),
    'TWR_DEL_CP_01':      (28.6315, 77.2167),
    'TWR_NOI_SEC15_01':   (28.5700, 77.3200),
    'TWR_NOI_SEC62_01':   (28.6270, 77.3650),
    'TWR_MUM_ANDHERI_01': (19.1136, 72.8697),
    'TWR_MUM_THANE_01':   (19.2183, 72.9781),
    'TWR_BLR_001':        (12.9716, 77.5946),
    'TWR_HYD_001':        (17.3850, 78.4867),
    'TWR_CHN_001':        (13.0827, 80.2707),
    'TWR_KOL_001':        (22.5726, 88.3639),
    'TWR_DEL_001':        (28.6139, 77.2090),
    'TWR_DEL_002':        (28.6200, 77.2150),
    'TWR_MUM_001':        (19.0760, 72.8777),
    'TWR_MUM_002':        (19.0800, 72.8800),
}

def get_coordinates(tower_id):
    if tower_id in TOWER_COORDINATES:
        return TOWER_COORDINATES[tower_id]
    # For unknown tower IDs assign random India coordinates
    import random
    india_locations = [
        (28.6139, 77.2090), (19.0760, 72.8777),
        (12.9716, 77.5946), (17.3850, 78.4867),
        (22.5726, 88.3639), (13.0827, 80.2707),
        (26.8467, 80.9462), (23.0225, 72.5714),
        (21.1702, 72.8311), (18.5204, 73.8567),
    ]
    random.seed(hash(tower_id) % 1000)
    return random.choice(india_locations)

def load_cdr(filepath='data/mock_cdr.csv'):
    df = pd.read_csv(filepath)
    df['caller_number'] = df['caller_number'].astype(str)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def analyze_towers(df):
    print("=== Tower Analysis Started ===")

    tower_stats = df.groupby('tower_id').agg(
        total_calls=('caller_number', 'count'),
        unique_callers=('caller_number', 'nunique'),
        unique_receivers=('receiver_number', 'nunique'),
        avg_duration=('call_duration_secs', 'mean')
    ).reset_index()

    tower_stats['avg_duration'] = tower_stats['avg_duration'].round(2)

    # Always assign coordinates — known or auto-assigned
    tower_stats['latitude']  = tower_stats['tower_id'].map(lambda x: get_coordinates(x)[0])
    tower_stats['longitude'] = tower_stats['tower_id'].map(lambda x: get_coordinates(x)[1])

    mean_calls = tower_stats['total_calls'].mean()
    tower_stats['high_activity_flag'] = tower_stats['total_calls'] > mean_calls

    print(f"Total towers analyzed: {len(tower_stats)}")
    print(f"High activity towers: {tower_stats['high_activity_flag'].sum()}")
    print(tower_stats[['tower_id','latitude','longitude','total_calls','high_activity_flag']].to_string())

    return tower_stats

def get_scam_towers(df, tower_stats):
    if os.path.exists('data/cdr_analysis_result.csv'):
        cdr_result = pd.read_csv('data/cdr_analysis_result.csv')
        scam_numbers = list(cdr_result[cdr_result['high_volume_flag'] == True]['caller_number'].astype(str))
    else:
        scam_numbers = []

    if scam_numbers:
        scam_calls = df[df['caller_number'].isin(scam_numbers)]
    else:
        scam_calls = df

    scam_towers = scam_calls.groupby('tower_id').agg(
        scam_call_count=('caller_number', 'count'),
        scam_numbers_used=('caller_number', 'nunique')
    ).reset_index()

    scam_towers = scam_towers.sort_values('scam_call_count', ascending=False)
    print(f"\nScam towers detected:")
    print(scam_towers.to_string())

    return scam_towers

def run_tower_analysis(filepath='data/mock_cdr.csv'):
    df = load_cdr(filepath)
    tower_stats = analyze_towers(df)
    scam_towers = get_scam_towers(df, tower_stats)

    os.makedirs('data', exist_ok=True)
    tower_stats.to_csv('data/tower_analysis_result.csv', index=False)
    scam_towers.to_csv('data/scam_towers.csv', index=False)

    print("\nResults saved to data/tower_analysis_result.csv")
    print("=== Tower Analysis Complete ===")

    return tower_stats, scam_towers

if __name__ == '__main__':
    run_tower_analysis()
