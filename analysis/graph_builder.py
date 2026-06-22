import pandas as pd
import networkx as nx
import os

def load_cdr(filepath='data/mock_cdr.csv'):
    df = pd.read_csv(filepath)
    df['caller_number'] = df['caller_number'].astype(str)
    df['receiver_number'] = df['receiver_number'].astype(str)
    return df

def build_call_graph(df):
    print("=== Graph Builder Started ===")

    G = nx.DiGraph()

    # Add edges for each call
    call_pairs = df.groupby(['caller_number', 'receiver_number']).agg(
        call_count=('call_duration_secs', 'count'),
        total_duration=('call_duration_secs', 'sum')
    ).reset_index()

    for _, row in call_pairs.iterrows():
        G.add_edge(
            row['caller_number'],
            row['receiver_number'],
            weight=row['call_count'],
            total_duration=row['total_duration']
        )

    print(f"Total nodes in graph: {G.number_of_nodes()}")
    print(f"Total edges in graph: {G.number_of_edges()}")

    return G

def analyze_graph(G):
    # Calculate degree centrality
    degree_centrality = nx.degree_centrality(G)
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())

    # Build results dataframe
    nodes_df = pd.DataFrame({
        'phone_number': list(degree_centrality.keys()),
        'degree_centrality': list(degree_centrality.values()),
        'in_degree': [in_degree.get(n, 0) for n in degree_centrality.keys()],
        'out_degree': [out_degree.get(n, 0) for n in degree_centrality.keys()]
    })

    nodes_df['degree_centrality'] = nodes_df['degree_centrality'].round(4)
    nodes_df = nodes_df.sort_values('degree_centrality', ascending=False)

    print(f"\nTop 10 most connected numbers:")
    print(nodes_df.head(10)[['phone_number', 'degree_centrality', 'out_degree', 'in_degree']].to_string())

    return nodes_df

def identify_mastermind(nodes_df):
    mastermind = nodes_df.iloc[0]
    print(f"\n*** SUSPECTED MASTERMIND ***")
    print(f"Phone Number  : {mastermind['phone_number']}")
    print(f"Centrality    : {mastermind['degree_centrality']}")
    print(f"Calls Made    : {mastermind['out_degree']}")
    print(f"Calls Received: {mastermind['in_degree']}")
    return mastermind

def run_graph_analysis(filepath='data/mock_cdr.csv'):
    df = load_cdr(filepath)
    G = build_call_graph(df)
    nodes_df = analyze_graph(G)
    mastermind = identify_mastermind(nodes_df)

    os.makedirs('data', exist_ok=True)
    nodes_df.to_csv('data/graph_analysis_result.csv', index=False)

    print("\nResults saved to data/graph_analysis_result.csv")
    print("=== Graph Analysis Complete ===")

    return G, nodes_df, mastermind

if __name__ == '__main__':
    run_graph_analysis()
