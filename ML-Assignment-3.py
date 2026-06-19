# ==============================================================================
# MACHINE LEARNING FUNDAMENTALS: SALES FORECAST USING LINEAR REGRESSION
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load the dataset
# Ensure 'advertising_spend.csv' is in your working directory
df = pd.read_csv('advertising_spend.csv')

# Note: Based on the sample table, column names are assumed to be:
# 'Advertising Spend ($)' and 'Sales Revenue ($)'
# Adjust strings below if your actual CSV headers differ slightly.
x_col = 'Advertising Spend ($)'
y_col = 'Sales Revenue ($)'


# ==============================================================================
# Requirement b: Generate a heat map of Advertising Spend Vs Sales Revenue
# ==============================================================================
plt.figure(figsize=(6, 4))
sns.heatmap(df[[x_col, y_col]].corr(), annot=True, cmap='coolwarm', fmt=".4f")
plt.title('Correlation Heatmap: Advertising Spend vs Sales Revenue')
plt.savefig('advertising_sales_heatmap.png', bbox_inches='tight')
plt.show()


# ==============================================================================
# Requirement a: Predict product sales based on advertising spend using Linear Regression
# ==============================================================================
# Reshape features to 2D array for scikit-learn
X = df[[x_col]]
y = df[y_col]

# Split the dataset into 80% Training and 20% Testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Generate predictions on the test set
y_pred = model.predict(X_test)


# ==============================================================================
# Requirement c: Visualize the data as a scatter plot with a regression line
# ==============================================================================
plt.figure(figsize=(8, 5))
# Scatter plot of actual values
sns.scatterplot(data=df, x=x_col, y=y_col, color='blue', label='Actual Data')
# Plotting the regression line over the entire range of X
X_future = np.linspace(df[x_col].min(), df[x_col].max(), 100).reshape(-1, 1)
y_future = model.predict(X_future)
plt.plot(X_future, y_future, color='red', linewidth=2, label='Regression Line')

plt.title('Sales Revenue vs Advertising Spend')
plt.xlabel('Advertising Spend ($)')
plt.ylabel('Sales Revenue ($)')
plt.legend()
plt.savefig('advertising_sales_regression.png', bbox_inches='tight')
plt.show()


# ==============================================================================
# Requirement d: Compute Mean Squared Error, Absolute Mean Error & R2 Score
# ==============================================================================
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("--- Model Performance Metrics ---")
print(f"Mean Absolute Error (MAE)  : {mae:.4f}")
print(f"Mean Squared Error (MSE)   : {mse:.4f}")
print(f"R2 Score (Coefficient)     : {r2:.4f} ({r2 * 100:.2f}%)")
