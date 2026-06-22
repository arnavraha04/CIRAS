import pandas as pd
import os

def load_individual_cdr(filepath, suspect_number):
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['caller_number'] = df['caller_number'].astype(str)
    df['receiver_number'] = df['receiver_number'].astype(str)
    suspect_number = str(suspect_number)

    outgoing = df[df['caller_number'] == suspect_number].copy()
    incoming = df[df['receiver_number'] == suspect_number].copy()

    print(f"Suspect: {suspect_number}")
    print(f"Outgoing calls: {len(outgoing)}")
    print(f"Incoming calls: {len(incoming)}")

    return df, outgoing, incoming

def analyze_top_contacts(outgoing, incoming):
    out_contacts = outgoing.groupby('receiver_number').agg(
        outgoing_calls=('call_duration_secs', 'count'),
        total_duration=('call_duration_secs', 'sum'),
        avg_duration=('call_duration_secs', 'mean')
    ).reset_index()
    out_contacts.columns = ['contact_number', 'outgoing_calls', 'total_duration', 'avg_duration']

    in_contacts = incoming.groupby('caller_number').agg(
        incoming_calls=('call_duration_secs', 'count')
    ).reset_index()
    in_contacts.columns = ['contact_number', 'incoming_calls']

    contacts = pd.merge(out_contacts, in_contacts, on='contact_number', how='outer').fillna(0)
    contacts['total_calls'] = contacts['outgoing_calls'] + contacts['incoming_calls']
    contacts['avg_duration'] = contacts['avg_duration'].round(2)
    contacts = contacts.sort_values('total_calls', ascending=False)

    print(f"\nTop 5 contacts:")
    print(contacts.head(5)[['contact_number', 'total_calls', 'avg_duration']].to_string())

    return contacts

def analyze_call_timeline(outgoing, incoming):
    outgoing = outgoing.copy()
    incoming = incoming.copy()
    outgoing['direction'] = 'OUTGOING'
    incoming['direction'] = 'INCOMING'
    incoming = incoming.rename(columns={'caller_number': 'other_number'})
    outgoing = outgoing.rename(columns={'receiver_number': 'other_number'})

    timeline = pd.concat([
        outgoing[['timestamp', 'other_number', 'call_duration_secs', 'direction', 'tower_id']],
        incoming[['timestamp', 'other_number', 'call_duration_secs', 'direction', 'tower_id']]
    ]).sort_values('timestamp').reset_index(drop=True)

    return timeline

def analyze_movement(outgoing, incoming):
    all_calls = pd.concat([outgoing, incoming])
    all_calls = all_calls.sort_values('timestamp')

    movement = all_calls.groupby('tower_id').agg(
        total_calls=('call_duration_secs', 'count'),
        first_seen=('timestamp', 'min'),
        last_seen=('timestamp', 'max')
    ).reset_index()

    movement = movement.sort_values('total_calls', ascending=False)

    print(f"\nTowers visited: {len(movement)}")
    print(movement[['tower_id', 'total_calls']].to_string())

    return movement

def analyze_suspicious_hours(outgoing):
    outgoing = outgoing.copy()
    outgoing['hour'] = outgoing['timestamp'].dt.hour
    outgoing['date'] = outgoing['timestamp'].dt.date

    hourly = outgoing.groupby('hour').size().reset_index()
    hourly.columns = ['hour', 'call_count']

    odd_hour_calls = outgoing[outgoing['hour'].isin([22,23,0,1,2,3,4,5,6])]
    odd_pct = len(odd_hour_calls) / len(outgoing) * 100 if len(outgoing) > 0 else 0

    print(f"\nOdd hour calls: {len(odd_hour_calls)} ({odd_pct:.1f}%)")

    return hourly, odd_hour_calls

def analyze_ipdr(filepath):
    if not os.path.exists(filepath):
        return None, None, None

    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    suspicious_sites = [
        'telegram.org', 'protonmail.com', 'nordvpn.com',
        'binance.com', 'localbitcoins.com', 'hawala.com',
        'onion.to', 'tor2web.org'
    ]
    suspicious_apps = ['TeamViewer', 'AnyDesk', 'Telegram', 'Signal']

    df['is_suspicious_site'] = df['site_visited'].isin(suspicious_sites)
    df['is_suspicious_app'] = df['app_used'].isin(suspicious_apps)
    df['is_vpn'] = df['vpn_detected'] == True

    site_counts = df.groupby('site_visited').agg(
        visits=('timestamp', 'count'),
        total_data_mb=('data_used_mb', 'sum'),
        suspicious=('is_suspicious_site', 'first')
    ).reset_index().sort_values('visits', ascending=False)

    app_counts = df.groupby('app_used').agg(
        sessions=('timestamp', 'count'),
        total_data_mb=('data_used_mb', 'sum'),
        suspicious=('is_suspicious_app', 'first')
    ).reset_index().sort_values('sessions', ascending=False)

    vpn_count = df['is_vpn'].sum()
    suspicious_site_count = df['is_suspicious_site'].sum()
    suspicious_app_count = df['is_suspicious_app'].sum()

    print(f"\nIPDR Analysis:")
    print(f"VPN sessions detected: {vpn_count}")
    print(f"Suspicious site visits: {suspicious_site_count}")
    print(f"Suspicious app sessions: {suspicious_app_count}")

    return site_counts, app_counts, df

def run_individual_investigation(cdr_path, suspect_number, ipdr_path=None):
    print("=== Individual Investigation Started ===")
    print(f"Suspect: {suspect_number}")

    df, outgoing, incoming = load_individual_cdr(cdr_path, suspect_number)

    if len(outgoing) == 0 and len(incoming) == 0:
        print(f"No records found for {suspect_number}")
        return None

    contacts = analyze_top_contacts(outgoing, incoming)
    timeline = analyze_call_timeline(outgoing, incoming)
    movement = analyze_movement(outgoing, incoming)
    hourly, odd_calls = analyze_suspicious_hours(outgoing)

    site_counts = None
    app_counts = None
    ipdr_df = None

    if ipdr_path:
        site_counts, app_counts, ipdr_df = analyze_ipdr(ipdr_path)

    os.makedirs('data', exist_ok=True)
    contacts.to_csv('data/individual_contacts.csv', index=False)
    timeline.to_csv('data/individual_timeline.csv', index=False)
    movement.to_csv('data/individual_movement.csv', index=False)
    hourly.to_csv('data/individual_hourly.csv', index=False)

    if site_counts is not None:
        site_counts.to_csv('data/individual_sites.csv', index=False)
        app_counts.to_csv('data/individual_apps.csv', index=False)

    print("\nAll results saved to data/")
    print("=== Individual Investigation Complete ===")

    return {
        'contacts': contacts,
        'timeline': timeline,
        'movement': movement,
        'hourly': hourly,
        'odd_calls': odd_calls,
        'site_counts': site_counts,
        'app_counts': app_counts,
        'ipdr_df': ipdr_df
    }

if __name__ == '__main__':
    run_individual_investigation(
        cdr_path='data/mock_cdr.csv',
        suspect_number='9876543210',
        ipdr_path='data/mock_ipdr.csv'
    )
