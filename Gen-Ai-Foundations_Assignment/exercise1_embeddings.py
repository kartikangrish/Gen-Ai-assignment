from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def main():
    sentences = [
        "GenAI is transforming software development",
        "Artificial Intelligence is changing how developers work",
        "I love playing cricket on weekends"
    ]

    print("=" * 70)
    print("Exercise 1: Text Embeddings & Similarity Comparison")
    print("=" * 70)
    print()

    print("Loading Sentence Transformer model: all-MiniLM-L6-v2")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Model loaded successfully")
    print()

    print("Generating embeddings for sentences:")
    print("-" * 70)
    embeddings = model.encode(sentences, show_progress_bar=False)

    for i, (sentence, embedding) in enumerate(zip(sentences, embeddings), 1):
        print(f"Sentence {i}: {sentence}")
        print(f"  First 5 dimensions: {embedding[:5]}")
        print(f"  Embedding shape: {embedding.shape}")
        print()

    print("=" * 70)
    print("Similarity Score Matrix (Cosine Similarity)")
    print("=" * 70)
    print()

    similarity_matrix = cosine_similarity(embeddings)

    print(f"{'Sentence':<50} Similarity Scores")
    print("-" * 70)

    for i, sent in enumerate(sentences):
        scores = " | ".join([f"{similarity_matrix[i][j]:.4f}" for j in range(len(sentences))])
        print(f"S{i+1}: {sent[:46]:<46} {scores}")

    print()
    print("Detailed Similarity Pairs:")
    print("-" * 70)

    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            similarity = similarity_matrix[i][j]
            print(f"Pair ({i+1},{j+1}): {similarity:.4f}")
            print(f"  '{sentences[i]}'")
            print(f"  '{sentences[j]}'")
            print()

    print("=" * 70)
    print("Interpretation:")
    print("=" * 70)
    print("• Scores range from 0 (dissimilar) to 1 (identical)")
    print("• Sentences 1 and 2 should have higher similarity (both about AI/development)")
    print("• Sentence 3 is about cricket, so lower similarity with others")
    print()

if __name__ == "__main__":
    main()
