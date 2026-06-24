"""
Test Setup Script
Validates that all dependencies are properly installed and configured
"""

import sys
import subprocess


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    if package_name is None:
        package_name = module_name

    try:
        __import__(module_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - FAILED: {str(e)}")
        return False


def test_dependency_versions():
    """Check versions of key dependencies"""
    print_header("Checking Dependency Versions")

    try:
        import sentence_transformers
        print(f"✅ sentence-transformers: {sentence_transformers.__version__}")
    except:
        print("❌ sentence-transformers: Not installed")

    try:
        import sklearn
        print(f"✅ scikit-learn: {sklearn.__version__}")
    except:
        print("❌ scikit-learn: Not installed")

    try:
        import numpy
        print(f"✅ numpy: {numpy.__version__}")
    except:
        print("❌ numpy: Not installed")

    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"   ℹ️  GPU Support: Available ({torch.cuda.get_device_name(0)})")
        else:
            print("   ℹ️  GPU Support: Not available (CPU only)")
    except:
        print("❌ PyTorch: Not installed")


def test_imports():
    """Test all critical imports"""
    print_header("Testing Imports")

    all_ok = True
    all_ok &= test_import("sentence_transformers", "sentence-transformers")
    all_ok &= test_import("sklearn", "scikit-learn")
    all_ok &= test_import("sklearn.metrics.pairwise", "sklearn.metrics.pairwise")
    all_ok &= test_import("numpy", "numpy")
    all_ok &= test_import("requests", "requests")
    all_ok &= test_import("json", "json (stdlib)")

    return all_ok


def test_embeddings_model():
    """Test if embedding model can be loaded"""
    print_header("Testing Embedding Model Loading")

    try:
        from sentence_transformers import SentenceTransformer
        print("  Loading all-MiniLM-L6-v2 model...")
        print("  (This may take a minute on first run)")

        model = SentenceTransformer('all-MiniLM-L6-v2')
        print(f"✅ Model loaded successfully")
        print(f"   Model dimension: {model.get_sentence_embedding_dimension()}")

        # Test encoding
        test_sentence = "This is a test sentence"
        embedding = model.encode(test_sentence, show_progress_bar=False)
        print(f"✅ Test encoding successful")
        print(f"   Embedding shape: {embedding.shape}")
        print(f"   First 5 dims: {embedding[:5]}")

        return True
    except Exception as e:
        print(f"❌ Failed to load embedding model: {str(e)}")
        return False


def test_similarity_calculation():
    """Test similarity calculation"""
    print_header("Testing Similarity Calculation")

    try:
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity

        # Create test embeddings
        embeddings = np.array([
            [1, 0, 0],
            [0.8, 0.6, 0],
            [0, 1, 0]
        ])

        similarity = cosine_similarity(embeddings)
        print("✅ Similarity calculation successful")
        print(f"   Shape: {similarity.shape}")
        print(f"   Matrix:\n{similarity}")

        return True
    except Exception as e:
        print(f"❌ Failed similarity calculation: {str(e)}")
        return False


def test_api_connectivity():
    """Test if requests library works"""
    print_header("Testing API Connectivity")

    try:
        import requests

        # Test basic connectivity
        try:
            response = requests.get("https://www.google.com", timeout=5)
            print("✅ Internet connectivity: OK")
            return True
        except requests.exceptions.Timeout:
            print("⚠️  Internet connectivity: Timeout (may be normal)")
            return True
        except requests.exceptions.ConnectionError:
            print("⚠️  Internet connectivity: No connection (offline mode)")
            return True

    except Exception as e:
        print(f"❌ Failed connectivity test: {str(e)}")
        return False


def test_python_version():
    """Check Python version"""
    print_header("Checking Python Version")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version_str} - OK")
        print(f"   Executable: {sys.executable}")
        return True
    else:
        print(f"❌ Python {version_str} - Too old (need 3.8+)")
        return False


def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "GenAI Training - Setup Validation Test" + " " * 15 + "║")
    print("╚" + "=" * 68 + "╝")

    results = {}

    # Run tests
    results["Python Version"] = test_python_version()
    results["Imports"] = test_imports()
    results["Dependency Versions"] = True
    test_dependency_versions()
    results["Embeddings Model"] = test_embeddings_model()
    results["Similarity Calculation"] = test_similarity_calculation()
    results["API Connectivity"] = test_api_connectivity()

    # Summary
    print_header("Test Summary")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print()
    print(f"Total: {passed}/{total} tests passed")
    print()

    if passed == total:
        print("🎉 All tests passed! Setup is ready.")
        print()
        print("Next steps:")
        print("  1. python exercise1_embeddings.py    # Test embeddings")
        print("  2. python exercise3_bonus.py         # Test combined pipeline")
        print("  3. (Optional) Configure API key for exercise2_llm_api.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print()
        print("Common fixes:")
        print("  1. pip install --upgrade -r requirements.txt")
        print("  2. Check your Python version: python --version")
        print("  3. Review SETUP_GUIDE.md for troubleshooting")
        return 1


if __name__ == "__main__":
    sys.exit(main())
