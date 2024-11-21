import os
import json
import random
# Define root path for 'Stimuli' directory 
root_path = os.getcwd()

# Define conditions & their paths
conditions = {
    "EXEMPLAR": os.path.join(root_path, 'Stimuli', 'EXEMPLAR'),
    "STATE": os.path.join(root_path, 'Stimuli', 'STATE')
}

# Function to get image pairs for EXEMPLAR and STATE
def get_image_pairs_exemplar_state(condition_path, condition_name):
    pairs = []
    subdirs = ['USED', 'UNUSED']
    for subdir in subdirs:
        subdir_path = os.path.join(condition_path, subdir)
        if os.path.exists(subdir_path):
            
            # Get all image files in subdirectory, excluding 'Thumbs.db'
            files = [f for f in os.listdir(subdir_path) if f.lower().endswith('.jpg') and not f.startswith('Thumbs.db')]
            files.sort()  # Ensure pairs are sequentially organized
            base_names = {}
            for f in files:
                base = f[:-5]
                if base not in base_names:
                    base_names[base] = []
                base_names[base].append(os.path.join('Stimuli', condition_name, subdir, f))
            for images in base_names.values():
                if len(images) == 2:
                    pairs.append({'image1': images[0], 'image2': images[1]})
    
    # Print initial total pairs found
    initial_pair_count = len(pairs)
    print(f"Total pairs initially found for {condition_name} condition: {initial_pair_count}")

    # Limit to 50 pairs if more are found
    final_pairs = random.sample(pairs, min(75, initial_pair_count))
    print(f"Total pairs selected for {condition_name} condition (limited to 75): {len(final_pairs)}")
# Collect & sample image pairs for each condition
all_pairs = {
    'EXEMPLAR': get_image_pairs_exemplar_state(conditions['EXEMPLAR'], 'EXEMPLAR'),
    'STATE': get_image_pairs_exemplar_state(conditions['STATE'], 'STATE')
}

# Preparing JSON structure
json_data = []
for condition, pairs in all_pairs.items():
    for pair in pairs:
        json_data.append({
            'condition': condition,
            'image1': pair['image1'],
            'image2': pair['image2']
        })

# Output JSON file
with open('stimuli_pairs.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=2)

print('Generated stimuli_pairs.json with pairs for each condition.')