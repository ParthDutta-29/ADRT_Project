import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import argparse

# Framework Visualizer for Publication-Grade SMC Experimentation
# Converts bounded stochastic verification traces into interpretible robustness curves.

def plot_resilience_degradation_envelope(csv_file, output_path):
    """
    Plots the survivability envelope and resilience degradation over simulated time.
    """
    try:
        data = pd.read_csv(csv_file)
        time = data['Time']
        resilience = data['resilienceDegradation']
        safety = data['safetyMargin']
        
        plt.figure(figsize=(10, 6))
        
        # Bounded probability fills
        plt.plot(time, resilience, label='Resilience Degradation', color='#d62728', linewidth=2)
        plt.plot(time, safety, label='Safety Margin', color='#1f77b4', linewidth=2, linestyle='--')
        
        plt.fill_between(time, resilience, alpha=0.1, color='#d62728')
        plt.fill_between(time, safety, alpha=0.1, color='#1f77b4')
        
        plt.axhline(y=100, color='black', linestyle=':', alpha=0.5, label='Upper Bound (100)')
        plt.axhline(y=0, color='black', linestyle=':', alpha=0.5, label='Lower Bound (0)')
        
        plt.title('SMC Bounded Resilience Envelope over Operational Time', fontsize=14, weight='bold')
        plt.xlabel('Simulated Execution Time (ms)', fontsize=12)
        plt.ylabel('Bounded Metric Level [0,100]', fontsize=12)
        plt.legend(loc='center right')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        plt.savefig(output_path, dpi=300)
        print(f"Generated publication plot: {output_path}")
        
    except FileNotFoundError:
        print(f"Cannot generate plot: Data trace {csv_file} not found. (Run verifyta first)")

def plot_sustainability_tradeoff(data_dir, output_path):
    """
    Plots the tradeoff between carbon/energy cost and mitigation capacity (sweep results).
    """
    # Simulated data generation for framework demonstration
    capacities = [20, 50, 80]
    carbon_costs = [12000, 8500, 5000] # Decreases as capacity increases (shorter attacks)
    maintenance = [3000, 6000, 9500]   # Increases as capacity increases
    
    fig, ax1 = plt.subplots(figsize=(9, 6))

    color = 'tab:red'
    ax1.set_xlabel('Mitigation Capacity Bound [0,100]', fontsize=12)
    ax1.set_ylabel('Carbon Cost / Environmental Overhead', color=color, fontsize=12)
    ax1.plot(capacities, carbon_costs, marker='o', color=color, linewidth=2, label='Carbon Cost')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Maintenance Cost Overhead', color=color, fontsize=12)  
    ax2.plot(capacities, maintenance, marker='s', color=color, linewidth=2, linestyle='--', label='Maintenance Cost')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  
    plt.title('Sustainability Tradeoff vs. Defense Capacity', fontsize=14, weight='bold')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.savefig(output_path, dpi=300)
    print(f"Generated sustainability tradeoff plot: {output_path}")

if __name__ == "__main__":
    if not os.path.exists('../build/plots'):
        os.makedirs('../build/plots')
    
    # Generate mock plots for demonstration
    plot_sustainability_tradeoff('../build/experiments/', '../build/plots/sustainability_tradeoff.png')
