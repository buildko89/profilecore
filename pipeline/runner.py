import pandas as pd
from profilecore.core.context import ProfileCoreContext
from profilecore.text.analyzer import TextAnalyzer
from profilecore.stats.quantification import QuantificationModule
from profilecore.io.exporter import ReportExporter

class ProfileCorePipeline:
    def __init__(self):
        self.context = ProfileCoreContext()
        
    def run_survey_analysis(self, df: pd.DataFrame, text_col: str, 
                            q1_target: str, q1_features: list,
                            q2_target: str, q2_features: list):
        # 1. Load Data
        self.context.set_data("raw_data", df)
        
        # 2. Text Analysis (Clean + Sudachi)
        text_mod = TextAnalyzer(self.context)
        text_mod.run("raw_data", text_col)
        
        # 3. Stats: Quantification Type I
        stat_mod = QuantificationModule(self.context)
        stat_mod.run_type_1("raw_data", q1_target, q1_features)
        
        # 4. Stats: Quantification Type II
        stat_mod.run_type_2("raw_data", q2_target, q2_features)
        
        # 5. Export Results
        exporter = ReportExporter(self.context)
        exporter.export_markdown("profilecore_analysis_report.md")
        
        return self.context
