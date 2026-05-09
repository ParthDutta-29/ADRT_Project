import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import argparse
import glob

# Phase 13: Publication-Grade Visualizer
# Generates bounds, statistical envelopes (CI 95%), and comparative survivability curves.

def plot_trajectory_envelope(csv_file, output_dir):
    """
    Plots the statistical survivability envelope with 95% Confidence Intervals.
    """
    try:
        data = pd.read_csv(csv_file)
        
        # Group by Metric and Experiment
        for exp_id in data['Experiment_ID'].unique():
            exp_data = data[data['Experiment_ID'] == exp_id]
            
            for metric in exp_data['Metric'].unique():
                metric_data = exp_data[exp_data['Metric'] == metric]
                
                plt.figure(figsize=(10, 6))
                
                for val in metric_data['Value'].unique():
                    val_data = metric_data[metric_data['Value'] == val]
                    time = val_data['Time']
                    mean = val_data['Mean']
                    ci_lower = val_data['CI_95_Lower']
                    ci_upper = val_data['CI_95_Upper']
                    
                    p = plt.plot(time, mean, label=f'Value: {val}', linewidth=2)
                    plt.fill_between(time, ci_lower, ci_upper, alpha=0.2, color=p[0].get_color())
                
                plt.axhline(y=100, color='black', linestyle=':', alpha=0.5, label='Upper Bound (100)')
                plt.axhline(y=0, color='black', linestyle=':', alpha=0.5, label='Lower Bound (0)')
                
                plt.title(f'SMC Bounded Envelope: {metric}\n({exp_id})', fontsize=14, weight='bold')
                plt.xlabel('Simulated Execution Time (ms)', fontsize=12)
                plt.ylabel('Bounded Metric Level [0,100]', fontsize=12)
                plt.legend(loc='best')
                plt.grid(True, linestyle='--', alpha=0.6)
                plt.tight_layout()
                
                out_path = os.path.join(output_dir, f"{exp_id}_{metric}_trajectory.png")
                plt.savefig(out_path, dpi=300)
                plt.close()
                print(f"Generated publication plot: {out_path}")
                
    except FileNotFoundError:
        print(f"Cannot generate plot: Data trace {csv_file} not found.")

def main():
    parser = argparse.ArgumentParser(description='Phase 13 Plot Generation')
    parser.add_argument('--exp_dir', type=str, required=True, help='Path to the experiment run directory')
    args = parser.parse_args()
    
    plots_dir = os.path.join(args.exp_dir, 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    
    # Find trajectory CSV
    traj_csvs = glob.glob(os.path.join(args.exp_dir, 'trajectory_statistics_*.csv'))
    
    if traj_csvs:
        for csv_file in traj_csvs:
            print(f"Processing trajectory data: {csv_file}")
            plot_trajectory_envelope(csv_file, plots_dir)
    else:
        print(f"No trajectory_statistics CSV found in {args.exp_dir}")

if __name__ == "__main__":
    main()
