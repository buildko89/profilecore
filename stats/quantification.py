import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from profilecore.core.module import AnalysisModule

class QuantificationModule(AnalysisModule):
    """
    Implements Hayashi's Quantification Method Type I & II.
    Type I: Regression (Continuous Target)
    Type II: Discriminant Analysis (Categorical Target)
    """
    
    def run_type_1(self, input_key: str, target_col: str, feature_cols: list):
        df = self.context.get_data(input_key)
        if df is None: return
        
        self.log(f"Running Quantification Method Type I on {target_col}")
        
        # Proper One-hot Encoding (Gemini style)
        X = pd.get_dummies(df[feature_cols], drop_first=True)
        y = df[target_col]
        
        model = LinearRegression()
        model.fit(X, y)
        
        results = pd.DataFrame({
            'Category': X.columns,
            'Coefficient': model.coef_
        })
        results.loc[len(results)] = ['(Intercept)', model.intercept_]
        
        self.context.set_data(f"quant1_{target_col}", results)
        self.log(f"Type I complete. R-squared: {model.score(X, y):.4f}")
        return results

    def run_type_2(self, input_key: str, target_col: str, feature_cols: list):
        """
        Simplified Quantification Type II using Logistic Regression.
        """
        from sklearn.linear_model import LogisticRegression
        
        df = self.context.get_data(input_key)
        if df is None: return
        
        self.log(f"Running Quantification Method Type II on {target_col}")
        
        X = pd.get_dummies(df[feature_cols], drop_first=True)
        y = df[target_col]
        
        # Removed multi_class='auto' for compatibility with newer sklearn
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)
        
        # Capture scores for each class
        if len(model.classes_) <= 2:
            # Binary case
            results = pd.DataFrame(model.coef_.T, columns=[model.classes_[1]], index=X.columns)
        else:
            # Multi-class case
            results = pd.DataFrame(model.coef_.T, columns=model.classes_, index=X.columns)
        
        self.context.set_data(f"quant2_{target_col}", results)
        self.log("Type II complete.")
        return results
