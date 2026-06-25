from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
import numpy as np


def load_model(model_name="all-MiniLM-L6-v2"):
    """Load a pre-trained sentence transformer model."""
    model = SentenceTransformer(model_name)
    return model


def get_embeddings(model, texts):
    """Convert texts to embeddings."""
    embeddings = model.encode(texts, convert_to_tensor=False)
    return embeddings


def compute_cosine_similarity(embedding1, embedding2):
    """Compute cosine similarity between two embeddings."""
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    return similarity


def compute_euclidean_distance(embedding1, embedding2):
    """Compute Euclidean distance between two embeddings."""
    distance = euclidean(embedding1, embedding2)
    return distance


def compute_dot_product(embedding1, embedding2):
    """Compute dot product between two embeddings."""
    dot_product = np.dot(embedding1, embedding2)
    return dot_product


def print_first_n_dimensions(embedding, n=5):
    """Print the first n dimensions of an embedding."""
    return embedding[:n]


def main():
    # Sample statements for comparison
    statements = [
        "The cat is sitting on the mat.",
        "A feline is resting on the rug.",
        "The dog is playing in the park.",
        "The weather is beautiful today.",
        "Today is a sunny day with clear skies."
    ]

    # Load the model
    print("Loading sentence transformer model...")
    model = load_model()

    # Generate embeddings for all statements
    print("\nGenerating embeddings...")
    embeddings = get_embeddings(model, statements)

    # Print first five dimensions of each embedding
    print("\n" + "="*70)
    print("FIRST FIVE DIMENSIONS OF EMBEDDINGS")
    print("="*70)
    for i, (statement, embedding) in enumerate(zip(statements, embeddings)):
        first_five = print_first_n_dimensions(embedding, n=5)
        print(f"\nStatement {i+1}: {statement}")
        print(f"First 5 dimensions: {first_five}")

    # Compare similarity between statements
    print("\n" + "="*70)
    print("SIMILARITY SCORES BETWEEN STATEMENTS")
    print("="*70)

    # Compare first statement with all others
    print(f"\nComparing '{statements[0]}' with other statements:\n")
    for j in range(1, len(statements)):
        cosine_sim = compute_cosine_similarity(embeddings[0], embeddings[j])
        euclidean_dist = compute_euclidean_distance(embeddings[0], embeddings[j])
        dot_prod = compute_dot_product(embeddings[0], embeddings[j])

        print(f"Statement {j+1}: {statements[j]}")
        print(f"  Cosine Similarity:    {cosine_sim:.4f}")
        print(f"  Euclidean Distance:   {euclidean_dist:.4f}")
        print(f"  Dot Product:          {dot_prod:.4f}")
        print()

    # Pairwise similarity matrix for all statements
    print("\n" + "="*70)
    print("PAIRWISE COSINE SIMILARITY MATRIX")
    print("="*70)
    similarity_matrix = cosine_similarity(embeddings)

    print("\n     ", end="")
    for i in range(len(statements)):
        print(f"  S{i+1}   ", end="")
    print()

    for i, row in enumerate(similarity_matrix):
        print(f"S{i+1}: ", end="")
        for val in row:
            print(f"{val:.3f} ", end="")
        print()

    # Embedding statistics
    print("\n" + "="*70)
    print("EMBEDDING STATISTICS")
    print("="*70)
    print(f"Embedding dimension: {embeddings.shape[1]}")
    print(f"Number of statements: {embeddings.shape[0]}")
    print(f"Mean embedding value: {np.mean(embeddings):.4f}")
    print(f"Std embedding value:  {np.std(embeddings):.4f}")


if __name__ == "__main__":
    main()
