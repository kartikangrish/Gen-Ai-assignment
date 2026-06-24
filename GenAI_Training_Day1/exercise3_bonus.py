from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

class EmbeddingLLMPipeline:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"Loading Sentence Transformer model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("✓ Model loaded successfully\n")

    def find_best_matching_prompt(self, prompts, reference):
        all_texts = prompts + [reference]
        embeddings = self.model.encode(all_texts, show_progress_bar=False)

        reference_embedding = embeddings[-1]
        prompt_embeddings = embeddings[:-1]

        similarities = cosine_similarity([reference_embedding], prompt_embeddings)[0]

        best_idx = np.argmax(similarities)
        best_prompt = prompts[best_idx]
        best_similarity = similarities[best_idx]

        return best_prompt, best_similarity, best_idx

    def process_pipeline(self, prompts, reference):
        print("=" * 70)
        print("STEP 1: Generating Embeddings")
        print("=" * 70)
        print(f"Reference prompt: '{reference}'")
        print(f"Candidate prompts: {len(prompts)}")
        print()

        all_texts = prompts + [reference]
        embeddings = self.model.encode(all_texts, show_progress_bar=False)

        for i, text in enumerate(all_texts):
            label = "[REFERENCE]" if i == len(all_texts) - 1 else f"[Candidate {i+1}]"
            print(f"{label} {text[:40]:<40}")
            print(f"  First 5 dims: {embeddings[i][:5]}")

        print()
        print("=" * 70)
        print("STEP 2: Finding Best Matching Prompt")
        print("=" * 70)

        best_prompt, similarity, idx = self.find_best_matching_prompt(prompts, reference)

        print(f"✓ Best match found!")
        print(f"  Prompt: '{best_prompt}'")
        print(f"  Similarity: {similarity:.4f}")
        print(f"  Index: {idx + 1}")
        print()

        print("Similarity with all candidates:")
        reference_embedding = embeddings[-1]
        prompt_embeddings = embeddings[:-1]
        similarities = cosine_similarity([reference_embedding], prompt_embeddings)[0]

        for i, (prompt, sim) in enumerate(zip(prompts, similarities)):
            marker = "★ BEST" if i == idx else "  "
            print(f"{marker} [{i+1}] {sim:.4f} - {prompt}")

        print()
        print("=" * 70)
        print("STEP 3: Ready to Send to LLM")
        print("=" * 70)
        print(f"Selected prompt for LLM: '{best_prompt}'")
        print("(In production, this would be sent to the LLM API)")
        print()

        return {
            "reference": reference,
            "candidates": prompts,
            "best_match": best_prompt,
            "similarity_score": float(similarity),
            "index": idx,
            "embeddings": {
                "reference": embeddings[-1][:5].tolist(),
                "best_match": embeddings[idx][:5].tolist()
            }
        }


def main():
    print("=" * 70)
    print("Bonus Exercise: Combined Embeddings + LLM")
    print("=" * 70)
    print()

    pipeline = EmbeddingLLMPipeline()

    reference_prompt = "How does machine learning improve software development?"

    candidate_prompts = [
        "What is machine learning and its applications?",
        "Can AI enhance developer productivity?",
        "Tell me about natural language processing",
        "How do we build better recommendation systems?"
    ]

    results = pipeline.process_pipeline(candidate_prompts, reference_prompt)

    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    print(json.dumps({
        "reference": results["reference"],
        "best_match": results["best_match"],
        "similarity": results["similarity_score"],
        "candidate_count": len(results["candidates"])
    }, indent=2))

    print()
    print("✓ Pipeline complete!")
    print("  The best matching prompt would now be sent to the LLM API.")


if __name__ == "__main__":
    main()
