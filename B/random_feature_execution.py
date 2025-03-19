import os
import random
import subprocess

def get_feature_files(directory):
    """Retrieve a list of all feature files in the specified directory."""
    feature_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".feature"):
                feature_files.append(os.path.join(root, file))
    return feature_files

def run_features_in_random_order(directory):
    """Shuffle and run feature files in random order, tracking passed/failed counts."""
    feature_files = get_feature_files(directory)
    random.shuffle(feature_files)  # Randomize order

    passed_count = 0
    failed_count = 0

    for feature in feature_files:
        print(f"Running: {feature}")
        result = subprocess.run(["behave", feature], capture_output=True, text=True)
        print(result.stdout)  # Print the behave output

        if result.returncode == 0:
            print(f"✅ Test passed for: {feature}\n")
            passed_count += 1
        else:
            print(f"❌ Test failed for: {feature}\n")
            failed_count += 1

    print("=" * 50)
    print(f"🎯 Test Summary: {passed_count} PASSED | {failed_count} FAILED")
    print("=" * 50)

if __name__ == "__main__":
    # Set the directory containing your feature files
    features_directory = os.path.dirname(os.path.abspath(__file__))
    run_features_in_random_order(features_directory)