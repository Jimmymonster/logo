import os

def reformat_labels(labels_folder, output_folder, classes_file):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Mapping of old index to new index and category name to new category names
    index_mapping = {}
    category_mapping = {}
    new_index_counter = 0

    # Read files and organize by category and index
    for filename in os.listdir(labels_folder):
        if filename.endswith('.txt'):
            category_name = filename.rsplit('_', 1)[0]
            file_path = os.path.join(labels_folder, filename)

            if category_name not in category_mapping:
                category_mapping[category_name] = {}

            with open(file_path, 'r') as file:
                lines = file.readlines()

            for line in lines:
                parts = line.strip().split()
                old_index = int(parts[0])

                # Assign new index if necessary
                if old_index not in category_mapping[category_name]:
                    category_mapping[category_name][old_index] = new_index_counter
                    new_index_counter += 1

                new_index = category_mapping[category_name][old_index]
                index_mapping[(category_name, old_index)] = new_index

    # Rename categories with multiple indices
    final_category_mapping = {}
    new_categories = {}
    for category_name, indices in category_mapping.items():
        if len(indices) > 1:
            for old_index, new_index in indices.items():
                new_category_name = f"{category_name}{old_index + 1}"
                final_category_mapping[(category_name, old_index)] = new_index
                new_categories[new_index] = new_category_name
        else:
            new_category_name = category_name
            for old_index, new_index in indices.items():
                final_category_mapping[(category_name, old_index)] = new_index
                new_categories[new_index] = new_category_name

    # Write new label files
    for filename in os.listdir(labels_folder):
        if filename.endswith('.txt'):
            category_name = filename.rsplit('_', 1)[0]
            file_path = os.path.join(labels_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            with open(output_file_path, 'w') as file:
                for line in lines:
                    parts = line.strip().split()
                    old_index = int(parts[0])
                    new_index = final_category_mapping[(category_name, old_index)]
                    file.write(f"{new_index} {' '.join(parts[1:])}\n")

    # Write classes.txt
    with open(classes_file, 'w') as file:
        for index in sorted(new_categories):
            file.write(f"{new_categories[index]}\n")

# Example usage
labels_folder = "logo-train/labels"
output_folder = "logo-train/new_labels"
classes_file = "logo-train/classes.txt"
reformat_labels(labels_folder, output_folder, classes_file)
