# ==============================================================================
# MACHINE LEARNING FUNDAMENTALS: LOAN DEFAULTER ANALYSIS & PREDICTION
# ==============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# Load the dataset
df = pd.read_csv('Loan_default_data.csv')

# ==============================================================================
# Requirement a: Analyse the credit score distribution using a histogram
# ==============================================================================
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='CreditScore', kde=True, color='skyblue')
plt.title('Credit Score Distribution')
plt.xlabel('Credit Score')
plt.ylabel('Frequency')
plt.savefig('credit_score_distribution.png', bbox_inches='tight')
plt.show()


# ==============================================================================
# Requirement b: Analyse how credit scores differ between defaulters and non-defaulters using a box plot
# ==============================================================================
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Default', y='CreditScore', palette='Set2')
plt.title('Credit Score by Loan Default Status')
plt.xlabel('Default Status (0 = Non-Defaulter, 1 = Defaulter)')
plt.ylabel('Credit Score')
plt.savefig('credit_score_boxplot.png', bbox_inches='tight')
plt.show()


# ==============================================================================
# Requirement c: Predict whether a borrower is likely to default using Logistic Regression
# ==============================================================================
# Separate features (X) and target label (y)
# Adjust features selection as per columns available in your specific dataset
X = df.drop(columns=['Default']) 
y = df['Default']

# Split the dataset into 80% Training and 20% Testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Logistic Regression Model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Generate predictions on the test set
y_pred = model.predict(X_test)


# ==============================================================================
# Requirement d: Generate Confusion matrix
# ==============================================================================
cm = confusion_matrix(y_test, y_pred)
print("--- Confusion Matrix ---")
print(cm)
print("\n")


# ==============================================================================
# Requirement e: Compute Accuracy Score of the model
# ==============================================================================
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy Score: {accuracy:.4f} ({accuracy * 100:.2f}%)")
print("\n")


# ==============================================================================
# Requirement f: Generate a Classification report (Precision, Recall & F1-score)
# ==============================================================================
report = classification_report(y_test, y_pred)
print("--- Classification Report ---")
print(report)
