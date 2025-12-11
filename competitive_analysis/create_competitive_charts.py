#!/usr/bin/env python3
"""
Create competitive comparison charts for LinkedIn and Twitter

Generates professional visualizations comparing H²Q performance vs competitors
(IBM 156Q, IBM Advanced, Google Willow, IonQ).

Output formats optimized for social media:
- LinkedIn: 1200x627px (recommended)
- Twitter: 1200x675px (recommended)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from competitive_analysis import CompetitiveAnalyzer
import os

# Set style for professional appearance
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 14  # Increased for mobile readability
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.labelsize'] = 15  # Larger axis labels
plt.rcParams['axes.titlesize'] = 18  # Larger titles
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13

# Social media dimensions
LINKEDIN_SIZE = (12, 6.27)  # 1200x627px at 100 DPI
TWITTER_SIZE = (12, 6.75)   # 1200x675px at 100 DPI

# Color scheme (professional, colorblind-friendly)
# Using ColorBrewer Set2 palette for better accessibility
H2Q_COLOR = '#2E86AB'      # Blue (good contrast)
IBM_COLOR = '#8B4C9F'      # Purple (better contrast, colorblind-friendly)
IBM_ADV_COLOR = '#F18F01'  # Orange (excellent for colorblind)
GOOGLE_COLOR = '#E74C3C'   # Red-orange (better than pure red)
IONQ_COLOR = '#16A085'     # Teal (colorblind-friendly alternative to green)
COMPETITOR_COLORS = [IBM_COLOR, IBM_ADV_COLOR, GOOGLE_COLOR, IONQ_COLOR]

# Patterns for colorblind accessibility (backup differentiation)
PATTERNS = ['', '///', '...', 'xxx', '+++']  # Solid, diagonal, dots, cross, plus


def create_overall_value_score_chart(analyzer, output_dir='competitive_analysis'):
    """Create overall value score comparison chart"""
    comparisons = analyzer.compare_all()
    
    systems = []
    scores = []
    colors = []
    
    # Exclude IonQ (trapped-ion, different technology platform)
    for name, comp in analyzer.competitors.items():
        if 'IonQ' in comp.name:
            continue  # Skip IonQ - different technology platform
        
        # Better label wrapping for y-axis (horizontal bar chart)
        label = comp.name
        if 'IBM 156-Qubit (Standard' in label:
            label = 'IBM 156Q\nStandard'
        elif 'IBM 156-Qubit (Advanced' in label:
            label = 'IBM 156Q\nAdvanced'
        elif 'Google Willow' in label:
            label = 'Google\nWillow'
        else:
            # Generic wrapping for long names
            words = label.split()
            if len(words) > 2:
                mid = len(words) // 2
                label = ' '.join(words[:mid]) + '\n' + ' '.join(words[mid:])
        systems.append(label)
        scores.append(comparisons[name].overall_value_score)
        # Adjust color index to skip IonQ
        comp_names = [n for n in analyzer.competitors.keys() if 'IonQ' not in analyzer.competitors[n].name]
        colors.append(COMPETITOR_COLORS[comp_names.index(name)])
    
    # Add H²Q for reference
    systems.insert(0, 'H²Q\nBaseline')
    scores.insert(0, 100.0)  # H²Q is the baseline (100%)
    colors.insert(0, H2Q_COLOR)
    
    fig, ax = plt.subplots(figsize=LINKEDIN_SIZE, dpi=100)
    
    bars = ax.barh(systems, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add patterns for colorblind accessibility
    for i, (bar, pattern) in enumerate(zip(bars, [''] + PATTERNS[:len(bars)-1])):
        if pattern:  # Skip pattern for H²Q (first bar)
            bar.set_hatch(pattern)
    
    # Add value labels on bars
    for i, (bar, score) in enumerate(zip(bars, scores)):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f'{score:.1f}', ha='left', va='center', fontweight='bold', fontsize=14)
    
    ax.set_xlabel('Overall Value Score', fontsize=14, fontweight='bold')
    ax.set_title('H²Q Competitive Performance: Superconducting Systems Error Mitigation Index', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0, 110)  # Ensure starts at zero for accurate representation
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Legend removed per user request - H²Q bar is self-explanatory
    
    # Add score explanation in open space (upper right) with small font
    score_explanation = ('Score: 0-100 weighted composite\n'
                        '(Fidelity 30%, Coherence 20%,\n'
                        'Errors 30%, FP Reduction 20%)\n'
                        '\n'
                        'Comparison: Superconducting\n'
                        'systems only (IBM, Google)')
    ax.text(0.98, 0.98, score_explanation, 
            transform=ax.transAxes, fontsize=8,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='gray', linewidth=0.5))
    
    plt.tight_layout()
    
    # Save for LinkedIn
    plt.savefig(f'{output_dir}/competitive_value_score_linkedin.png', 
                dpi=100, bbox_inches='tight', facecolor='white')
    print(f"✓ Created: {output_dir}/competitive_value_score_linkedin.png")
    
    # Resize for Twitter
    fig.set_size_inches(TWITTER_SIZE)
    plt.savefig(f'{output_dir}/competitive_value_score_twitter.png', 
                dpi=100, bbox_inches='tight', facecolor='white')
    print(f"✓ Created: {output_dir}/competitive_value_score_twitter.png")
    
    plt.close()


def create_metric_comparison_chart(analyzer, output_dir='competitive_analysis'):
    """Create side-by-side metric comparison chart"""
    comparisons = analyzer.compare_all()
    
    metrics = ['False Positive\nReduction', 'Logical Error\nReduction', 
               'T2 Coherence\nImprovement', '1Q Fidelity\nImprovement']
    
    # Get improvements vs IBM 156Q Standard (primary competitor)
    ibm_comp = comparisons['IBM_156Q_Standard']
    improvements = [
        ibm_comp.false_positive_reduction,
        ibm_comp.logical_error_reduction,
        ibm_comp.coherence_improvement_t2,
        ibm_comp.fidelity_improvement_1q
    ]
    
    fig, ax = plt.subplots(figsize=LINKEDIN_SIZE, dpi=100)
    
    bars = ax.bar(metrics, improvements, color=H2Q_COLOR, alpha=0.8, 
                  edgecolor='black', linewidth=1.5)
    
    # Ensure y-axis starts at zero
    ax.set_ylim(0, max(improvements) * 1.2)
    
    # Add value labels
    for bar, val in zip(bars, improvements):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'+{val:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=12)
    
    ax.set_ylabel('Improvement (%)', fontsize=14, fontweight='bold')
    ax.set_title('H²Q Superconducting Systems Error Mitigation: Improvements vs IBM 156Q', 
                 fontsize=16, fontweight='bold', pad=20)
    # Already set above - ensure starts at zero
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.axhline(y=0, color='black', linewidth=0.8)
    
    plt.tight_layout()
    
    # Save for LinkedIn
    plt.savefig(f'{output_dir}/competitive_metrics_linkedin.png', 
                dpi=100, bbox_inches='tight', facecolor='white')
    print(f"✓ Created: {output_dir}/competitive_metrics_linkedin.png")
    
    # Resize for Twitter
    fig.set_size_inches(TWITTER_SIZE)
    plt.savefig(f'{output_dir}/competitive_metrics_twitter.png', 
                dpi=100, bbox_inches='tight', facecolor='white')
    print(f"✓ Created: {output_dir}/competitive_metrics_twitter.png")
    
    plt.close()


def create_false_positive_comparison(analyzer, output_dir='competitive_analysis'):
    """Create false positive rate comparison (key differentiator)"""
    h2q_fpr = analyzer.h2qec.false_positive_rate * 100
    
    competitors = []
    fprs = []
    colors = []
    
    # Exclude IonQ (trapped-ion, different technology platform)
    for name, comp in analyzer.competitors.items():
        if 'IonQ' in comp.name:
            continue  # Skip IonQ - different technology platform
        
        # Better label wrapping for x-axis
        label = comp.name
        if 'IBM 156-Qubit (Standard' in label:
            label = 'IBM\n156Q\nStandard'
        elif 'IBM 156-Qubit (Advanced' in label:
            label = 'IBM\n156Q\nAdvanced'
        elif 'Google Willow' in label:
            label = 'Google\nWillow'
        else:
            # Generic wrapping for long names
            words = label.split()
            if len(words) > 2:
                mid = len(words) // 2
                label = ' '.join(words[:mid]) + '\n' + ' '.join(words[mid:])
        competitors.append(label)
        fprs.append(comp.false_positive_rate * 100)
        # Adjust color index to skip IonQ
        comp_names = [n for n in analyzer.competitors.keys() if 'IonQ' not in analyzer.competitors[n].name]
        colors.append(COMPETITOR_COLORS[comp_names.index(name)])
    
    # Add H²Q
    competitors.insert(0, 'H²Q')
    fprs.insert(0, h2q_fpr)
    colors.insert(0, H2Q_COLOR)
    
    fig, ax = plt.subplots(figsize=LINKEDIN_SIZE, dpi=100)
    
    bars = ax.bar(competitors, fprs, color=colors, alpha=0.8, 
                  edgecolor='black', linewidth=1.5)
    
    # Set x-axis labels with proper wrapping - use set_xticks first to avoid warning
    ax.set_xticks(range(len(competitors)))
    ax.set_xticklabels(competitors, rotation=0, ha='center', fontsize=11)
    
    # Add patterns for colorblind accessibility
    for i, (bar, pattern) in enumerate(zip(bars, [''] + PATTERNS[:len(bars)-1])):
        if pattern:  # Skip pattern for H²Q (first bar)
            bar.set_hatch(pattern)
    
    # Add value labels
    for bar, val in zip(bars, fprs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{val:.2f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=12)
    
    ax.set_ylabel('False Positive Rate (%)', fontsize=14, fontweight='bold')
    ax.set_title('False Positive Rate: Superconducting Systems Error Mitigation Comparison', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, max(fprs) * 1.15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Highlight H²Q advantage - positioned higher above the bar
    ax.text(0, h2q_fpr + max(fprs) * 0.15, '79.7% Reduction\nvs IBM 156Q', 
            ha='center', va='bottom', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Adjust layout to accommodate wrapped labels
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # Leave extra space at bottom
    
    # Save for LinkedIn
    plt.savefig(f'{output_dir}/competitive_false_positive_linkedin.png', 
                dpi=100, bbox_inches='tight', facecolor='white')
    print(f"✓ Created: {output_dir}/competitive_false_positive_linkedin.png")
    
    # Resize for Twitter
    fig.set_size_inches(TWITTER_SIZE)
    plt.savefig(f'{output_dir}/competitive_false_positive_twitter.png', 
                dpi=100, bbox_inches='tight', facecolor='white')
    print(f"✓ Created: {output_dir}/competitive_false_positive_twitter.png")
    
    plt.close()


def create_radar_chart(analyzer, output_dir='competitive_analysis'):
    """Create radar chart comparing multiple metrics"""
    comparisons = analyzer.compare_all()
    ibm_comp = comparisons['IBM_156Q_Standard']
    
    # Normalize metrics to 0-100 scale for radar chart
    categories = ['False Positive\nReduction', 'Logical Error\nReduction',
                 'T2 Coherence\nImprovement', '1Q Fidelity\nImprovement',
                 'Effective\nQubit Gain', 'Circuit Depth\nImprovement']
    
    h2q_values = [100, 100, 100, 100, 100, 100]  # H²Q is baseline
    
    ibm_values = [
        min(100, max(0, ibm_comp.false_positive_reduction)),
        min(100, max(0, ibm_comp.logical_error_reduction)),
        min(100, max(0, ibm_comp.coherence_improvement_t2)),
        min(100, max(0, ibm_comp.fidelity_improvement_1q * 10)),  # Scale up
        min(100, max(0, ibm_comp.effective_qubit_gain / 2)),  # Scale down
        min(100, max(0, ibm_comp.effective_circuit_depth * 10))  # Scale
    ]
    
    # Number of variables
    N = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    # Add values
    h2q_values += h2q_values[:1]
    ibm_values += ibm_values[:1]
    
    # Create figure with more padding to make hexagon appear smaller relative to labels
    fig = plt.figure(figsize=(10, 10), dpi=100)
    ax = fig.add_subplot(111, projection='polar')
    
    # Plot H²Q
    ax.plot(angles, h2q_values, 'o-', linewidth=2, label='H²Q (Baseline)', 
            color=H2Q_COLOR, markersize=8)
    ax.fill(angles, h2q_values, alpha=0.25, color=H2Q_COLOR)
    
    # Plot IBM 156Q
    ax.plot(angles, ibm_values, 'o-', linewidth=2, label='IBM 156Q Standard', 
            color=IBM_COLOR, markersize=8)
    ax.fill(angles, ibm_values, alpha=0.15, color=IBM_COLOR)
    
    # Add category labels - increased font size for readability
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    # Keep ylim at 0-100 for statistical correctness (values go up to 100)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
    ax.grid(True, alpha=0.3)
    
    ax.set_title('H²Q Superconducting Systems Error Mitigation Profile\nvs IBM 156Q Standard (All Metrics Normalized)', 
                 fontsize=13, fontweight='bold', pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=10)
    
    # Add padding around subplot to make hexagon appear smaller and give labels more space
    plt.subplots_adjust(left=0.15, right=0.85, top=0.9, bottom=0.1)
    
    # Save square format (good for both platforms)
    plt.savefig(f'{output_dir}/competitive_radar_chart.png', 
                dpi=100, bbox_inches='tight', facecolor='white')
    print(f"✓ Created: {output_dir}/competitive_radar_chart.png")
    
    plt.close()


def main():
    """Generate all competitive comparison charts"""
    print("Generating competitive comparison charts for LinkedIn and Twitter...")
    print("=" * 70)
    
    # Create output directory for charts
    output_dir = 'competitive_analysis/charts'
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize analyzer
    analyzer = CompetitiveAnalyzer()
    
    # Generate charts
    print("\n1. Overall Value Score Chart...")
    create_overall_value_score_chart(analyzer, output_dir)
    
    print("\n2. Metric Comparison Chart...")
    create_metric_comparison_chart(analyzer, output_dir)
    
    print("\n3. False Positive Rate Comparison...")
    create_false_positive_comparison(analyzer, output_dir)
    
    print("\n4. Radar Chart...")
    create_radar_chart(analyzer, output_dir)
    
    print("\n" + "=" * 70)
    print("✓ All charts generated successfully!")
    print(f"\nCharts saved in: {output_dir}/")
    print("\nFiles created:")
    print("  - competitive_value_score_linkedin.png (1200x627px)")
    print("  - competitive_value_score_twitter.png (1200x675px)")
    print("  - competitive_metrics_linkedin.png (1200x627px)")
    print("  - competitive_metrics_twitter.png (1200x675px)")
    print("  - competitive_false_positive_linkedin.png (1200x627px)")
    print("  - competitive_false_positive_twitter.png (1200x675px)")
    print("  - competitive_radar_chart.png (1000x1000px)")
    print("\nReady for social media sharing! 🚀")


if __name__ == '__main__':
    main()
