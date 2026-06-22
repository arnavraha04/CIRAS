import pandas as pd
from pyvis.network import Network
import os

def build_network_graph(cdr_path='data/mock_cdr.csv', risk_path='data/risk_scores.csv'):
    print("=== Network Graph Builder Started ===")

    df = pd.read_csv(cdr_path)
    df['caller_number'] = df['caller_number'].astype(str)
    df['receiver_number'] = df['receiver_number'].astype(str)

    # Load risk levels
    mastermind = []
    critical = []
    high = []

    if os.path.exists(risk_path):
        risk_df = pd.read_csv(risk_path)
        mastermind = list(risk_df[risk_df['risk_level'] == 'MASTERMIND']['caller_number'].astype(str))
        critical = list(risk_df[risk_df['risk_level'] == 'CRITICAL']['caller_number'].astype(str))
        high = list(risk_df[risk_df['risk_level'] == 'HIGH']['caller_number'].astype(str))

    # Focus on top suspects only for clean graph
    top_suspects = mastermind[:3] + critical[:5] + high[:5]
    top_suspects = list(set(top_suspects))

    print(f"Building graph for {len(top_suspects)} top suspects")

    # Get calls made by top suspects only
    suspect_calls = df[df['caller_number'].isin(top_suspects)]

    # Limit to top 15 victims per suspect
    limited = []
    for num in top_suspects:
        calls = suspect_calls[suspect_calls['caller_number'] == num]
        top_victims = calls.groupby('receiver_number').agg(
            call_count=('call_duration_secs', 'count'),
            total_duration=('call_duration_secs', 'sum')
        ).reset_index().nlargest(15, 'call_count')
        top_victims['caller_number'] = num
        limited.append(top_victims)

    # Also add calls between suspects
    suspect_to_suspect = df[
        df['caller_number'].isin(top_suspects) &
        df['receiver_number'].isin(top_suspects)
    ].groupby(['caller_number','receiver_number']).agg(
        call_count=('call_duration_secs','count'),
        total_duration=('call_duration_secs','sum')
    ).reset_index()

    if limited:
        filtered = pd.concat([
            pd.concat(limited),
            suspect_to_suspect
        ]).drop_duplicates(subset=['caller_number','receiver_number'])
    else:
        filtered = suspect_to_suspect

    print(f"Total edges: {len(filtered)}")

    # Create network
    net = Network(
        height='620px',
        width='100%',
        bgcolor='#1a1a2e',
        font_color='white',
        directed=True
    )

    net.barnes_hut(
        gravity=-3000,
        central_gravity=0.3,
        spring_length=120,
        spring_strength=0.08,
        damping=0.09
    )

    # Add all nodes
    all_nodes = set(
        filtered['caller_number'].tolist() +
        filtered['receiver_number'].tolist()
    )

    for node in all_nodes:
        if node in mastermind:
            color = '#8B0000'
            size = 55
            label = f"💀 {node}"
            title = f"<b>MASTERMIND</b><br>Phone: {node}"
            font_size = 16
        elif node in critical:
            color = '#FF0000'
            size = 40
            label = f"🔴 {node}"
            title = f"<b>CRITICAL</b><br>Phone: {node}"
            font_size = 14
        elif node in high:
            color = '#FF8C00'
            size = 30
            label = f"🟠 {node}"
            title = f"<b>HIGH RISK</b><br>Phone: {node}"
            font_size = 13
        else:
            color = '#3a3a5c'
            size = 12
            label = f"...{node[-4:]}"
            title = f"Victim: {node}"
            font_size = 10

        net.add_node(
            node,
            label=label,
            color=color,
            size=size,
            title=title,
            font={'size': font_size, 'color': 'white'},
            borderWidth=2
        )

    # Add edges
    for _, row in filtered.iterrows():
        caller = str(row['caller_number'])
        receiver = str(row['receiver_number'])
        count = int(row['call_count'])

        if caller in top_suspects and receiver in top_suspects:
            edge_color = '#FFD700'
            width = 4
            title = f"Inter-suspect calls: {count}"
        elif caller in top_suspects:
            edge_color = '#FF4444'
            width = max(1, min(count, 5))
            title = f"Scam calls: {count}"
        else:
            edge_color = '#444466'
            width = 1
            title = f"Calls: {count}"

        net.add_edge(
            caller, receiver,
            width=width,
            color=edge_color,
            title=title,
            arrows='to'
        )

    net.set_options("""
    var options = {
        "nodes": {
            "shadow": true
        },
        "edges": {
            "smooth": {
                "type": "curvedCW",
                "roundness": 0.2
            },
            "shadow": true
        },
        "physics": {
            "barnesHut": {
                "gravitationalConstant": -3000,
                "centralGravity": 0.3,
                "springLength": 120
            },
            "minVelocity": 5,
            "stabilization": {
                "enabled": true,
                "iterations": 100,
                "updateInterval": 10,
                "fit": true
            }
        }
    }
    """)

    os.makedirs('data', exist_ok=True)
    output_path = 'data/network_graph.html'
    net.save_graph(output_path)

    print(f"Network graph saved to {output_path}")
    print("=== Network Graph Complete ===")

    return output_path

if __name__ == '__main__':
    build_network_graph()
