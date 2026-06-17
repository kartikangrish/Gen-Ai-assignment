# ==============================================================================
# MACHINE LEARNING FUNDAMENTALS: STUDENT RESULT PREDICTION
# ==============================================================================

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# 1. Load the dataset
# Replace 'Student_data.csv' with your actual file path if located in a different directory
df = pd.read_csv('Student_data.csv')

# 2. Separate Features (X) and Target Variable (y)
# Features: Attendance, Assignment, MidExam, StudyHours, GPA, Participation
# Target: Result
X = df[['Attendance', 'Assignment', 'MidExam', 'StudyHours', 'GPA', 'Participation']]
y = df['Result']

# 3. Split the data into Training and Testing sets (e.g., 80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==============================================================================
# Requirement a: Predict student Result using Decision Tree classifier
# ==============================================================================
# Initialize the Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42, max_depth=4)

# Train the model on training data
clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = clf.predict(X_test)


# ==============================================================================
# Requirement c: Compute the accuracy score of the model
# ==============================================================================
accuracy = accuracy_score(y_test, y_pred)
print("--- Model Performance Metrics ---")
print(f"Accuracy Score: {accuracy * 100:.2f}%")
print("\n")


# ==============================================================================
# Requirement b: Visualize the data as a decision tree
# ==============================================================================
plt.figure(figsize=(15, 10))
plot_tree(
    clf, 
    feature_names=X.columns, 
    class_names=sorted(y.unique().astype(str)), 
    filled=True, 
    rounded=True,
    fontsize=10
)
plt.title("Decision Tree Visualization for Student Result Prediction")

# Save the visualization figure to the directory
plt.savefig('student_decision_tree.png', bbox_inches='tight', dpi=300)
print("Decision tree visualization has been saved as 'student_decision_tree.png'.")

# Display the plot
plt.show()

