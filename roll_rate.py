import numpy as np
import pandas as pd

# Define roll rates
roll_rates = {'C': {'C': 0.9, 'DQ1': 0.03, 'DQ2':0, 'DQ3':0.00, 'PO':0.07, 'CO': 0},
              'DQ1':{'C': 0.1, 'DQ1': 0.5, 'DQ2':0.30, 'DQ3':0.05, 'PO':0.05, 'CO': 0},
              'DQ2':{'C': 0.03, 'DQ1': 0.03, 'DQ2':0.3, 'DQ3':0.6, 'PO':0.04, 'CO': 0},
              'DQ3':{'C': 0.01, 'DQ1': 0.02, 'DQ2':0.02, 'DQ3':0.15, 'PO':0.05, 'CO': 0.75}
             }

def time_pass(current_status, pct, roll_rates=roll_rates):
    roll_rate = roll_rates[current_status]
    result = {}
    for next_status in roll_rate:
        result[next_status] = round(pct * roll_rate[next_status],2)
    return result

def simulate(current_status, sim_period, 
             roll_rates=roll_rates):
    """
    Function takes 
        (1) one current_status as a dictionary specify current portfolio composition, e.g. {'C': 60, 'DQ1':20, 'DQ2': 14. 'DQ':3}
        (2) simulation period
        (3) roll rates dictionary
    Returns: a pandas dataframe with loan count/pct evolving through time and a csv file
    
    """
    i = 0
    final_result = {}
    active_status = ['C', 'DQ1', 'DQ2', 'DQ3']
    all_status = active_status + ['CO', 'PO']
    while i < sim_period:
        if i ==0:
            result = current_status.copy()
        
        _result_list = []
        for c_status in result:
            # only active loans can go to next period
            if c_status in active_status:
                _result = time_pass(c_status, result[c_status], roll_rates)
                _result_list.append(_result)
        # combining loan/pct in the same next period
        result = pd.DataFrame(_result_list).sum().to_dict()
            
        i+=1
        final_result[i] = result
    final_result[0] = current_status
    final_result = pd.DataFrame(final_result).T.fillna(0)
    final_result.index.name = 'period'
    final_result.to_csv('./simulate {p} with status {c}.csv'.format(p=sim_period, c=current_status))
    final_result = final_result[['C', 'DQ1', 'DQ2', 'DQ3', 'PO', 'CO']]
    return final_result


# Using Example
current_portfolio_composition={'C':100, 'DQ1':30, 'DQ2':10, 'DQ3':4}
sim_period = 12
roll_rates_assumption = roll_rates
result = simulate(current_portfolio_composition, sim_period, roll_rates_assumption)

