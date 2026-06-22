import pandas as pd
import os

def load_all_results(use_complaints=False):
    cdr = pd.read_csv('data/cdr_analysis_result.csv')
    imei = pd.read_csv('data/suspicious_numbers_imei.csv')
    graph = pd.read_csv('data/graph_analysis_result.csv')
    cdr['caller_number'] = cdr['caller_number'].astype(str)
    imei['caller_number'] = imei['caller_number'].astype(str)
    graph['phone_number'] = graph['phone_number'].astype(str)
    complaints = None
    if use_complaints and os.path.exists('data/mock_complaints.csv'):
        complaints = pd.read_csv('data/mock_complaints.csv')
        complaints['scammer_number'] = complaints['scammer_number'].astype(str)
    return cdr, imei, graph, complaints

def calculate_risk_scores(use_complaints=False):
    print("=== Risk Scoring Started ===")
    cdr, imei, graph, complaints = load_all_results(use_complaints)

    total_numbers = len(cdr)
    total_calls = cdr['total_outgoing_calls'].sum()
    avg_calls = cdr['total_outgoing_calls'].mean()
    top_1pct = cdr['total_outgoing_calls'].quantile(0.99)
    top_5pct = cdr['total_outgoing_calls'].quantile(0.95)

    print(f"Dataset size: {total_numbers} numbers, {total_calls} calls")
    print(f"Avg calls per number: {avg_calls:.1f}")
    print(f"Top 1% threshold: {top_1pct:.0f} calls")
    print(f"Top 5% threshold: {top_5pct:.0f} calls")

    scores = cdr[['caller_number', 'total_outgoing_calls',
                   'unique_victims_called', 'high_volume_flag']].copy()

    # Rule 1 - Call volume relative to dataset
    def score_volume(calls):
        if calls >= top_1pct:
            return 30
        elif calls >= top_5pct:
            return 20
        elif calls >= avg_calls * 3:
            return 10
        return 0

    scores['score_high_volume'] = scores['total_outgoing_calls'].apply(score_volume)

    # Rule 2 - Unique victims relative to dataset
    top_victims_1pct = cdr['unique_victims_called'].quantile(0.99)
    top_victims_5pct = cdr['unique_victims_called'].quantile(0.95)

    def score_victims(victims):
        if victims >= top_victims_1pct:
            return 25
        elif victims >= top_victims_5pct:
            return 15
        elif victims >= cdr['unique_victims_called'].mean() * 3:
            return 8
        return 0

    scores['score_unique_victims'] = scores['unique_victims_called'].apply(score_victims)

    # Rule 3 - Multi SIM IMEI
    multi_sim_numbers = set(imei['caller_number'].tolist())
    scores['score_multi_sim'] = scores['caller_number'].apply(
        lambda x: 25 if x in multi_sim_numbers else 0)

    # Rule 4 - Graph centrality relative to dataset
    graph_scores = graph[['phone_number', 'degree_centrality']].copy()
    graph_scores.columns = ['caller_number', 'degree_centrality']
    scores = pd.merge(scores, graph_scores, on='caller_number', how='left')
    scores['degree_centrality'] = scores['degree_centrality'].fillna(0)
    top_centrality = scores['degree_centrality'].quantile(0.99)

    def score_centrality(c):
        if c >= top_centrality:
            return 20
        elif c >= top_centrality * 0.5:
            return 10
        return 0

    scores['score_centrality'] = scores['degree_centrality'].apply(score_centrality)

    # Rule 5 - Complaints
    if complaints is not None:
        complaint_numbers = set(complaints['scammer_number'].tolist())
        scores['score_in_complaints'] = scores['caller_number'].apply(
            lambda x: 30 if x in complaint_numbers else 0)
        max_score = 130
    else:
        scores['score_in_complaints'] = 0
        max_score = 100

    scores['total_risk_score'] = (
        scores['score_high_volume'] +
        scores['score_unique_victims'] +
        scores['score_multi_sim'] +
        scores['score_centrality'] +
        scores['score_in_complaints']
    )

    scores['max_possible_score'] = max_score

    # Prioritization tiers
    scores = scores.sort_values('total_risk_score', ascending=False).reset_index(drop=True)

    def assign_tier(row):
        rank = row.name
        score = row['total_risk_score']
        max_s = row['max_possible_score']
        pct = score / max_s * 100

        if rank == 0:
            return 'MASTERMIND'
        elif rank <= 2 and pct >= 70:
            return 'MASTERMIND'
        elif rank <= 10 and pct >= 55:
            return 'CRITICAL'
        elif rank <= 30 and pct >= 35:
            return 'HIGH'
        elif pct >= 20:
            return 'MEDIUM'
        else:
            return 'LOW'

    scores['risk_level'] = scores.apply(assign_tier, axis=1)

    print(f"\nPrioritization Summary:")
    print(f"MASTERMIND : {len(scores[scores['risk_level'] == 'MASTERMIND'])}")
    print(f"CRITICAL   : {len(scores[scores['risk_level'] == 'CRITICAL'])}")
    print(f"HIGH       : {len(scores[scores['risk_level'] == 'HIGH'])}")
    print(f"MEDIUM     : {len(scores[scores['risk_level'] == 'MEDIUM'])}")
    print(f"LOW        : {len(scores[scores['risk_level'] == 'LOW'])}")

    top = scores.iloc[0]
    print(f"\n*** SUSPECTED MASTERMIND ***")
    print(f"Number     : {top['caller_number']}")
    print(f"Risk Score : {top['total_risk_score']}/{max_score}")
    print(f"Risk Level : {top['risk_level']}")

    return scores

def run_risk_scoring(use_complaints=False):
    scores = calculate_risk_scores(use_complaints)
    os.makedirs('data', exist_ok=True)
    scores.to_csv('data/risk_scores.csv', index=False)
    print(f"\nResults saved to data/risk_scores.csv")
    print("=== Risk Scoring Complete ===")
    return scores

if __name__ == '__main__':
    import sys
    use_complaints = '--with-complaints' in sys.argv
    run_risk_scoring(use_complaints)
