import pandas as pd
import os

CHUNK_SIZE = 10000

def load_cdr(filepath='data/mock_cdr.csv'):
    total_rows = sum(1 for _ in open(filepath)) - 1
    print(f"Total rows: {total_rows}")

    if total_rows <= CHUNK_SIZE:
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['caller_number'] = df['caller_number'].astype(str)
        df['receiver_number'] = df['receiver_number'].astype(str)
        print(f"Loaded {len(df)} CDR records (direct)")
        return df
    else:
        print(f"Large file detected — loading in chunks of {CHUNK_SIZE}")
        chunks = []
        for chunk in pd.read_csv(filepath, chunksize=CHUNK_SIZE):
            chunk['timestamp'] = pd.to_datetime(chunk['timestamp'])
            chunk['caller_number'] = chunk['caller_number'].astype(str)
            chunk['receiver_number'] = chunk['receiver_number'].astype(str)
            chunks.append(chunk)
        df = pd.concat(chunks, ignore_index=True)
        print(f"Loaded {len(df)} CDR records (chunked)")
        return df

def analyze_call_frequency(df):
    outgoing = df.groupby('caller_number').agg(
        total_outgoing_calls=('receiver_number', 'count'),
        unique_victims_called=('receiver_number', 'nunique'),
        avg_call_duration=('call_duration_secs', 'mean'),
        total_call_duration=('call_duration_secs', 'sum')
    ).reset_index()

    incoming = df.groupby('receiver_number').agg(
        total_incoming_calls=('caller_number', 'count')
    ).reset_index()
    incoming.columns = ['caller_number', 'total_incoming_calls']

    result = pd.merge(outgoing, incoming, on='caller_number', how='left')
    result['avg_call_duration'] = result['avg_call_duration'].round(2)

    threshold = result['total_outgoing_calls'].quantile(0.95)
    result['high_volume_flag'] = result['total_outgoing_calls'] > threshold

    print(f"Analyzed {len(result)} unique numbers")
    print(f"High volume numbers found: {result['high_volume_flag'].sum()}")
    return result

def analyze_time_patterns(df):
    df = df.copy()
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['date'] = df['timestamp'].dt.date

    peak_hours = df.groupby(['caller_number', 'hour']).size().reset_index()
    peak_hours.columns = ['caller_number', 'hour', 'call_count']
    peak_hours = peak_hours.loc[peak_hours.groupby('caller_number')['call_count'].idxmax()]
    peak_hours = peak_hours.rename(columns={'hour': 'peak_calling_hour'})

    odd_hours = df[df['hour'].isin([22, 23, 0, 1, 2, 3, 4, 5, 6])]
    odd_hour_callers = odd_hours.groupby('caller_number').size().reset_index()
    odd_hour_callers.columns = ['caller_number', 'odd_hour_calls']
    odd_hour_callers['odd_hours_flag'] = odd_hour_callers['odd_hour_calls'] > 5

    print(f"Numbers active during odd hours: {odd_hour_callers['odd_hours_flag'].sum()}")
    return peak_hours, odd_hour_callers

def run_cdr_analysis(filepath='data/mock_cdr.csv'):
    print("=== CDR Analysis Started ===")
    df = load_cdr(filepath)
    freq_analysis = analyze_call_frequency(df)
    peak_hours, odd_hour_callers = analyze_time_patterns(df)

    result = pd.merge(freq_analysis,
                      peak_hours[['caller_number', 'peak_calling_hour']],
                      on='caller_number', how='left')
    result = pd.merge(result,
                      odd_hour_callers[['caller_number', 'odd_hour_calls', 'odd_hours_flag']],
                      on='caller_number', how='left')
    result['odd_hour_calls'] = result['odd_hour_calls'].fillna(0)
    result['odd_hours_flag'] = result['odd_hours_flag'].fillna(False)

    os.makedirs('data', exist_ok=True)
    result.to_csv('data/cdr_analysis_result.csv', index=False)
    print(f"Analysis complete. {len(result)} numbers analyzed")
    print(f"Results saved to data/cdr_analysis_result.csv")
    print("=== CDR Analysis Complete ===")
    return df, result

if __name__ == '__main__':
    run_cdr_analysis()
