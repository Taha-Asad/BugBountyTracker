import math, re, sys, os

def roundup(val):
    # FIRST.org specification rounding: smallest number, specified to one decimal place, >= input
    val = round(val, 9)
    return round(math.ceil(val * 10) / 10, 1)

def cvss31_score(vec):
    m = dict(item.split(':') for item in vec.replace('CVSS:3.1/', '').split('/'))
    av_weights = {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.20}
    ac_weights = {'L': 0.77, 'H': 0.44}
    ui_weights = {'N': 0.85, 'R': 0.62}
    imp_weights = {'N': 0.0, 'L': 0.22, 'H': 0.56}
    
    scope_changed = (m['S'] == 'C')
    if scope_changed:
        pr_weights = {'N': 0.85, 'L': 0.68, 'H': 0.50}
    else:
        pr_weights = {'N': 0.85, 'L': 0.62, 'H': 0.27}
        
    iss = 1.0 - ((1.0 - imp_weights[m['C']]) * (1.0 - imp_weights[m['I']]) * (1.0 - imp_weights[m['A']]))
    if iss <= 0:
        return 0.0
        
    if not scope_changed:
        impact = 6.42 * iss
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * ((iss - 0.02) ** 15)
        
    exploitability = 8.2252 * av_weights[m['AV']] * ac_weights[m['AC']] * pr_weights[m['PR']] * ui_weights[m['UI']]
    
    if scope_changed:
        score = roundup(min(1.08 * (impact + exploitability), 10.0))
    else:
        score = roundup(min(impact + exploitability, 10.0))
    return score

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fixtures_path = os.path.join(script_dir, 'CVSS_TEST_FIXTURES.md')
    
    with open(fixtures_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    lines = text.splitlines()
    mismatches = []
    vectors_parsed = []
    
    for line in lines:
        if line.strip().startswith('| **') and 'CVSS:3.1' in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            idx = parts[0].replace('*', '')
            name = parts[1]
            vec = parts[2].replace('`', '')
            exp_score = float(parts[3].replace('*', ''))
            calc_score = cvss31_score(vec)
            vectors_parsed.append(vec)
            
            if abs(exp_score - calc_score) > 0.001:
                mismatches.append((idx, name, vec, exp_score, calc_score))
                
    print(f"Total fixtures evaluated: {len(vectors_parsed)}")
    print(f"Unique vectors: {len(set(vectors_parsed))}")
    
    if mismatches:
        print(f"FAILED: {len(mismatches)} score mismatches found:")
        for m in mismatches:
            print(f"  Index {m[0]} ({m[1]}): expected {m[3]}, computed {m[4]} | {m[2]}")
        sys.exit(1)
    else:
        print("SUCCESS: 100% mathematical parity across all CVSS 3.1 test vectors!")
        sys.exit(0)

if __name__ == '__main__':
    main()
