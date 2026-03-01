import os
import pandas as pd
from datetime import datetime

class ReportExporter:
    """
    Automates analysis report generation in Markdown.
    Inspired by Copilot's reporting concepts.
    """
    def __init__(self, context):
        self.context = context

    def export_markdown(self, filename: str = "report.md"):
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# ProfileCore Analysis Report\n")
            f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 1. Analysis Logs\n")
            for log in self.context.get_logs():
                f.write(f"- {log}\n")
            f.write("\n")
            
            f.write("## 2. Results Summary\n\n")
            for key, df in self.context.data.items():
                if key == "raw_data": continue
                f.write(f"### {key}\n")
                f.write(df.head(20).to_markdown())
                f.write("\n\n")
        
        print(f"Report exported to: {output_path}")
