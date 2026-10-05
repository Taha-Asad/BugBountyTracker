import math
import re
import sys
import os

# FIRST.org CVSS v3.1 Base Metric Weight Tables (Specification Document Section 7.1)
AV_WEIGHTS = {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.20}
AC_WEIGHTS = {'L': 0.77, 'H': 0.44}
PR_WEIGHTS_UNCHANGED = {'N': 0.85, 'L': 0.62, 'H': 0.27}
PR_WEIGHTS_CHANGED = {'N': 0.85, 'L': 0.68, 'H': 0.50}
UI_WEIGHTS = {'N': 0.85, 'R': 0.62}
IMP_WEIGHTS = {'N': 0.0, 'L': 0.22, 'H': 0.56}

MANDATORY_METRICS = ('AV', 'AC', 'PR', 'UI', 'S', 'C', 'I', 'A')

ALLOWED_VALUES = {
    'AV': set(AV_WEIGHTS.keys()),
    'AC': set(AC_WEIGHTS.keys()),
    'PR': {'N', 'L', 'H'},
    'UI': set(UI_WEIGHTS.keys()),
    'S': {'U', 'C'},
    'C': set(IMP_WEIGHTS.keys()),
    'I': set(IMP_WEIGHTS.keys()),
    'A': set(IMP_WEIGHTS.keys())
}

def roundup(val):
    """FIRST.org Appendix A Floating-Point Roundup Algorithm.
    The Roundup function returns the smallest number, specified to 1 decimal place,
    that is greater than or equal to the input.
    """
    val = round(val, 9)
    return round(math.ceil(val * 10) / 10, 1)

def parse_cvss31_vector(vec):
    """Strict CVSS 3.1 Vector String Parser.
    Rejects malformed strings, duplicate metric keys, missing mandatory metrics,
    and unknown metric values.
    """
    if not isinstance(vec, str):
        raise ValueError("Vector must be a string")
        
    prefix = "CVSS:3.1/"
    if not vec.startswith(prefix):
        raise ValueError(f"Vector must start with '{prefix}', got: {vec[:15]}")
        
    metric_part = vec[len(prefix):]
    segments = metric_part.split('/')
    if not segments or segments == ['']:
        raise ValueError("Vector contains no metric components")
        
    metrics = {}
    seen_keys = set()
    
    for seg in segments:
        if ':' not in seg:
            raise ValueError(f"Malformed metric segment (missing ':'): '{seg}'")
        k, v = seg.split(':', 1)
        k = k.strip()
        v = v.strip()
        
        if k in seen_keys:
            raise ValueError(f"Duplicate metric key detected: '{k}' in vector '{vec}'")
        seen_keys.add(k)
        
        if k not in ALLOWED_VALUES:
            raise ValueError(f"Unknown metric key: '{k}'")
            
        if v not in ALLOWED_VALUES[k]:
            raise ValueError(f"Invalid value '{v}' for metric '{k}'. Allowed: {sorted(ALLOWED_VALUES[k])}")
            
        metrics[k] = v
        
    missing = [m for m in MANDATORY_METRICS if m not in metrics]
    if missing:
        raise ValueError(f"Missing mandatory Base metrics: {missing}")
        
    return metrics

def cvss31_score(vec):
    """Calculates CVSS 3.1 Base Score following FIRST.org equations with coefficient 8.22."""
    m = parse_cvss31_vector(vec)
    
    scope_changed = (m['S'] == 'C')
    if scope_changed:
        pr_weights = PR_WEIGHTS_CHANGED
    else:
        pr_weights = PR_WEIGHTS_UNCHANGED
        
    # Impact Sub-Score (ISS)
    iss = 1.0 - ((1.0 - IMP_WEIGHTS[m['C']]) * (1.0 - IMP_WEIGHTS[m['I']]) * (1.0 - IMP_WEIGHTS[m['A']]))
    if iss <= 0:
        return 0.0
        
    # Impact equation
    if not scope_changed:
        impact = 6.42 * iss
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * ((iss - 0.02) ** 15)
        
    # Exploitability equation: Official FIRST.org CVSS 3.1 coefficient is 8.22
    exploitability = 8.22 * AV_WEIGHTS[m['AV']] * AC_WEIGHTS[m['AC']] * pr_weights[m['PR']] * UI_WEIGHTS[m['UI']]
    
    # Final Base Score with Roundup
    if scope_changed:
        score = roundup(min(1.08 * (impact + exploitability), 10.0))
    else:
        score = roundup(min(impact + exploitability, 10.0))
    return score

def run_parser_rejection_tests():
    """Validates that the parser strictly rejects malformed vectors and duplicates."""
    rejection_cases = [
        # Duplicate metric key
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/AV:L", "Duplicate metric key"),
        # Missing mandatory metric
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N", "Missing mandatory"),
        # Invalid prefix
        ("CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N", "Vector must start with"),
        # Unknown metric key
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/ZZ:X", "Unknown metric key"),
        # Invalid metric value
        ("CVSS:3.1/AV:X/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N", "Invalid value"),
        # Malformed colon
        ("CVSS:3.1/AVN/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N", "missing ':'"),
    ]
    
    for vec, expected_err in rejection_cases:
        try:
            parse_cvss31_vector(vec)
            raise AssertionError(f"Expected failure for vector '{vec}', but parser succeeded!")
        except ValueError as e:
            if expected_err.lower() not in str(e).lower():
                raise AssertionError(f"Expected error containing '{expected_err}', got '{str(e)}'")
    return len(rejection_cases)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fixtures_path = os.path.join(script_dir, 'CVSS_TEST_FIXTURES.md')
    
    # 1. Run parser rejection suite
    rejected_count = run_parser_rejection_tests()
    print(f"Parser Rejection Tests: {rejected_count} negative cases passed (duplicates, invalid syntax rejected)")
    
    # 2. Evaluate all 45 test fixtures
    with open(fixtures_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    lines = text.splitlines()
    mismatches = []
    vectors_parsed = []
    
    for line in lines:
        if line.strip().startswith('| **') and 'CVSS:3.1' in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            idx = parts[0].replace('*', '').strip()
            if not idx.isdigit():
                continue
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
        print("SUCCESS: 100% mathematical parity across all CVSS 3.1 test vectors using official 8.22 coefficient!")
        sys.exit(0)

if __name__ == '__main__':
    main()
