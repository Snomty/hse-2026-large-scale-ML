import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

def parse_training_log(log_file_path: str) -> pd.DataFrame:
    data = []
    
    with open(log_file_path, 'r') as f:
        for line in f:
            if 'INFO:' in line and '{' in line:
                try:
                    # Извлекаем JSON-подобный словарь
                    dict_str = re.search(r'\{.*\}', line)
                    if dict_str:
                        metrics = eval(dict_str.group())
                        data.append({
                            'step': metrics.get('global_step'),
                            'loss': metrics.get('running_loss'),
                            'throughput': metrics.get('tokens_per_s'),
                            'lr': metrics.get('lr'),
                            'peak_memory_gb': metrics.get('peak_alloc_gb'),
                            'epoch': metrics.get('epoch'),
                        })
                except Exception as e:
                    print(f"Error parsing line: {e}")
                    continue
    
    return pd.DataFrame(data)


def get_final_results(log_file_path: str) -> Dict[str, float]:
    results = {}
    
    with open(log_file_path, 'r') as f:
        content = f.read()
        
        # Perplexity
        ppl_match = re.search(r'perplexity:\s*([0-9.]+)', content)
        if ppl_match:
            results['val_ppl'] = float(ppl_match.group(1))
        
        # Peak memory
        mem_matches = re.findall(r"peak_alloc_gb['\"]?\s*:\s*([0-9.]+)", content)
        if mem_matches:
            results['peak_memory_gb'] = float(mem_matches[-1])

    return results


def load_all_experiments(base_path: str) -> Dict[str, Dict]:
    base_path = Path(base_path)
    experiments = ['fp32', 'bf16', 'bf16_ckpt']
    results = {}
    
    for exp in experiments:
        log_file = base_path / f'{exp}.log'
        if log_file.exists():
            print(f"Parsing {exp}...")
            results[exp] = {
                'metrics': parse_training_log(log_file),
                'final': get_final_results(log_file)
            }
        else:
            print(f"Warning: {log_file} not found")
    
    return results
