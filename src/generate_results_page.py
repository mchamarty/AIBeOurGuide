import pandas as pd
import os

def generate_results_page(features_df: pd.DataFrame, explanation: str):
    """
    Generate an HTML results page using a template and extracted features.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_path, 'results_template.html')
    output_path = os.path.join(base_path, '../output/results.html')
    
    # Load the HTML template
    with open(template_path, 'r') as file:
        template = file.read()
    
    # Generate rows for the table
    rows = ""
    for _, row in features_df.iterrows():
        rows += f"""
        <tr>
            <td>{row.get('department_name', 'N/A')}</td>
            <td>{row['task_repetition_score']}</td>
            <td>{row['workflow_complexity']}</td>
            <td>{row['data_structure_score']}</td>
            <td>{row['communication_frequency']}</td>
            <td>{row['average_sentiment']:.2f}</td>
            <td>{row['stakeholder_dependency']:.2f}</td>
            <td>{row['time_spread']}</td>
        </tr>
        """
    
    # Replace placeholders
    final_html = template.replace('{{ROWS}}', rows).replace('{{EXPLANATION}}', explanation)
    
    # Save the final HTML file
    with open(output_path, 'w') as file:
        file.write(final_html)
    
    print(f"✅ Results page generated successfully at: {output_path}")
