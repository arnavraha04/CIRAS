import pandas as pd
import os

def load_cdr(filepath='data/mock_cdr.csv'):
    df = pd.read_csv(filepath)
    df['caller_number'] = df['caller_number'].astype(str)
    df['imei'] = df['imei'].astype(str)
    return df

def analyze_imei(df):
    print("=== IMEI Analysis Started ===")
    imei_sims = df.groupby('imei').agg(
        unique_sims=('caller_number', 'nunique'),
        total_calls=('caller_number', 'count'),
        sim_numbers=('caller_number', lambda x: list(x.unique()))
    ).reset_index()
    imei_sims['multi_sim_flag'] = imei_sims['unique_sims'] > 1
    number_imeis = df.groupby('caller_number').agg(
        unique_imeis=('imei', 'nunique'),
        imei_list=('imei', lambda x: list(x.unique()))
    ).reset_index()
    number_imeis['multi_device_flag'] = number_imeis['unique_imeis'] > 1
    print(f"Total unique IMEIs found: {len(imei_sims)}")
    print(f"Multi-SIM IMEIs found: {imei_sims['multi_sim_flag'].sum()}")
    print(f"Numbers using multiple devices: {number_imeis['multi_device_flag'].sum()}")
    return imei_sims, number_imeis

def get_suspicious_imeis(imei_sims, number_imeis):
    suspicious_imeis = imei_sims[imei_sims['multi_sim_flag'] == True].copy()
    suspicious_imeis = suspicious_imeis.sort_values('unique_sims', ascending=False)
    suspicious_numbers = number_imeis[number_imeis['multi_device_flag'] == True].copy()
    suspicious_numbers = suspicious_numbers.sort_values('unique_imeis', ascending=False)
    print(f"\nTop suspicious IMEIs:")
    print(suspicious_imeis[['imei', 'unique_sims', 'total_calls']].head(5).to_string())
    print(f"\nTop suspicious numbers (multi device):")
    print(suspicious_numbers[['caller_number', 'unique_imeis']].head(5).to_string())
    return suspicious_imeis, suspicious_numbers

def run_imei_analysis(filepath='data/mock_cdr.csv'):
    df = load_cdr(filepath)
    imei_sims, number_imeis = analyze_imei(df)
    suspicious_imeis, suspicious_numbers = get_suspicious_imeis(imei_sims, number_imeis)
    os.makedirs('data', exist_ok=True)
    imei_sims.to_csv('data/imei_analysis_result.csv', index=False)
    suspicious_numbers.to_csv('data/suspicious_numbers_imei.csv', index=False)
    print("\nResults saved to data/imei_analysis_result.csv")
    print("=== IMEI Analysis Complete ===")
    return imei_sims, number_imeis, suspicious_imeis, suspicious_numbers

if __name__ == '__main__':
    run_imei_analysis()
