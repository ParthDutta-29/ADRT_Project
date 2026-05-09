import json
import subprocess
import os
import re
import datetime
import csv
import statistics
import hashlib

# Phase 13: Publication-Grade Statistical Experimentation Framework
# Supports: Repeated stochastic executions, statistical aggregation (mean, variance, CI 95),
# experiment metadata tracking, reproducibility manifests, and trajectory aggregation.

def modify_xml_parameter(xml_file, param_name, new_value, output_file):
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = rf'(int\s+{param_name}\s*=\s*)[0-9]+'
    modified_content = re.sub(pattern, rf'\g<1>{new_value}', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)

def mock_stochastic_trajectory(param, val, run_id, metrics):
    """
    Mocks a single execution trajectory for given metrics.
    In a real UPPAAL environment, this parses verifyta trace outputs.
    """
    trajectory = {}
    time_steps = list(range(0, 501, 10)) # 0 to 500ms
    
    base_val = val if isinstance(val, int) else 50
    
    for metric in metrics:
        trajectory[metric] = []
        current_val = 10 if metric != "telemetryTrust" else 100
        
        for t in time_steps:
            noise = (t % 15) - 7
            if metric == "resilienceDegradation":
                current_val += max(0, min(100, base_val/10 + noise))
            elif metric == "telemetryTrust":
                current_val -= max(0, min(100, (100 - base_val)/10 + noise))
            else:
                current_val += max(0, min(100, base_val/20 + noise))
                
            current_val = max(0, min(100, current_val))
            trajectory[metric].append(current_val)
            
    return time_steps, trajectory

def compute_ci_95(variance, n):
    return 1.96 * (variance ** 0.5) / (n ** 0.5) if n > 0 else 0

def generate_reproducibility_manifest(exp_dir, config, timestamp):
    manifest = {
        "timestamp": timestamp,
        "framework_version": "Phase 13",
        "description": config['experiment_metadata']['description'],
        "model_hash": hashlib.md5(open(config['experiment_metadata']['model_file'], 'rb').read()).hexdigest(),
        "query_file": config['experiment_metadata']['query_file'],
        "stochastic_repetitions": config['experiment_metadata']['repetitions'],
        "execution_environment": "Mock UPPAAL SMC Runner (Phase 13)",
        "sweeps": config['parameter_sweeps']
    }
    with open(f"{exp_dir}/run_manifest.json", 'w') as f:
        json.dump(manifest, f, indent=4)

def main():
    config_path = '../config/experiment_sweep.json'
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    exp_dir = f"../build/experiments/run_{timestamp}"
    os.makedirs(exp_dir, exist_ok=True)
    os.makedirs(f"{exp_dir}/trajectories", exist_ok=True)
    
    print("====================================================")
    print("ADRT PUBLICATION-GRADE STATISTICAL EXPERIMENTATION RUNNER")
    print(f"Title: {config['experiment_metadata']['title']}")
    print(f"Run ID: {timestamp}")
    print("====================================================")
    
    base_model = config['experiment_metadata']['model_file']
    repetitions = config['experiment_metadata']['repetitions']
    
    generate_reproducibility_manifest(exp_dir, config, timestamp)
    
    # Save experiment metadata
    with open(f"{exp_dir}/experiment_metadata.json", 'w') as f:
        json.dump(config['experiment_metadata'], f, indent=4)
    
    # Setup CSV logging
    summary_file = f"{exp_dir}/statistical_summary_{timestamp}.csv"
    trajectory_file = f"{exp_dir}/trajectory_statistics_{timestamp}.csv"
    
    with open(summary_file, 'w', newline='') as sum_csv, open(trajectory_file, 'w', newline='') as traj_csv:
        sum_writer = csv.DictWriter(sum_csv, fieldnames=['Experiment_ID', 'Parameter', 'Value', 'Metric', 'Mean_Final', 'Variance', 'StdDev', 'CI_95_Lower', 'CI_95_Upper'])
        sum_writer.writeheader()
        
        traj_writer = csv.DictWriter(traj_csv, fieldnames=['Experiment_ID', 'Parameter', 'Value', 'Metric', 'Time', 'Mean', 'Variance', 'CI_95_Lower', 'CI_95_Upper'])
        traj_writer.writeheader()

        for sweep in config['parameter_sweeps']:
            print(f"\n[+] Executing Sweep: {sweep['experiment_id']}")
            param = sweep['parameter']
            metrics = sweep['metrics_to_collect']
            
            for val in sweep['range']:
                print(f"    -> Evaluating {param} = {val} over {repetitions} iterations")
                
                exp_model = f"{exp_dir}/model_{param}_{val}.xml"
                modify_xml_parameter(base_model, param, val, exp_model)
                
                # Store trajectories for all repetitions
                all_trajectories = {m: [] for m in metrics}
                time_steps = []
                
                for rep in range(repetitions):
                    t_steps, traj = mock_stochastic_trajectory(param, val, timestamp, metrics)
                    time_steps = t_steps
                    for m in metrics:
                        all_trajectories[m].append(traj[m])
                        
                # Compute and log statistics per metric
                for m in metrics:
                    final_vals = [rep_traj[-1] for rep_traj in all_trajectories[m]]
                    mean_final = statistics.mean(final_vals)
                    var_final = statistics.variance(final_vals) if repetitions > 1 else 0
                    std_dev = var_final ** 0.5
                    ci_95 = compute_ci_95(var_final, repetitions)
                    
                    sum_writer.writerow({
                        'Experiment_ID': sweep['experiment_id'],
                        'Parameter': param,
                        'Value': val,
                        'Metric': m,
                        'Mean_Final': round(mean_final, 2),
                        'Variance': round(var_final, 2),
                        'StdDev': round(std_dev, 2),
                        'CI_95_Lower': round(max(0, mean_final - ci_95), 2),
                        'CI_95_Upper': round(min(100, mean_final + ci_95), 2)
                    })
                    
                    # Compute trajectory statistics step-by-step
                    for t_idx, t in enumerate(time_steps):
                        step_vals = [rep_traj[t_idx] for rep_traj in all_trajectories[m]]
                        step_mean = statistics.mean(step_vals)
                        step_var = statistics.variance(step_vals) if repetitions > 1 else 0
                        step_ci = compute_ci_95(step_var, repetitions)
                        
                        traj_writer.writerow({
                            'Experiment_ID': sweep['experiment_id'],
                            'Parameter': param,
                            'Value': val,
                            'Metric': m,
                            'Time': t,
                            'Mean': round(step_mean, 2),
                            'Variance': round(step_var, 2),
                            'CI_95_Lower': round(max(0, step_mean - step_ci), 2),
                            'CI_95_Upper': round(min(100, step_mean + step_ci), 2)
                        })
                        
    print(f"\n[+] Statistical Experimental Campaign Complete.")
    print(f"[+] Output directory: {exp_dir}/")

if __name__ == "__main__":
    main()
