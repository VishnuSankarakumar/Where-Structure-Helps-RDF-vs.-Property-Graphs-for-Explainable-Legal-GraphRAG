#analyse entity labels in Neo4j graph dump to inform ontology design decisions
#Outputs:
#effective duplicates (AI_System vs AISystem), 
#occurrence patterns

import json
from collections import defaultdict, Counter


def load_nodes(filepath):
    nodes = []
    with open(filepath, 'r') as file_handle:
        for line in file_handle:
            item = json.loads(line.strip())
            if item['type'] == 'node':
                nodes.append(item)
    return nodes


def filter_entity_nodes(nodes):
    #filter out chunk nodes, keep only entity nodes
    entity_nodes = []    
    for node in nodes:
        labels = node.get('labels', [])
        if '__Entity__' in labels and 'Chunk' not in labels:
            entity_nodes.append(node)
    return entity_nodes


def count_labels(entity_nodes):
    #count occurrences of each unique node label (except Entity)
    all_labels = []
    for node in entity_nodes:
        for label in node['labels']:
            if label != '__Entity__':
                all_labels.append(label)
    return Counter(all_labels)


def find_formatting_variants(label_counts):
    #find labels that are formatting variants of each other
    normalised_groups = defaultdict(list)
    
    for label in label_counts:
        normalised = label.lower().replace(' ', '').replace('_', '')
        normalised_groups[normalised].append(label)
    
    #only keep groups with multiple variants
    formatting_variants = {}
    for normalised_form, variant_list in normalised_groups.items():
        if len(variant_list) > 1:
            formatting_variants[normalised_form] = variant_list
    
    return formatting_variants


def print_report(entity_nodes, label_counts, formatting_variants): 
    print("LABEL REPORT")
    print("")
    print("Total entity nodes: " + str(len(entity_nodes)))
    print("Total distinct labels: " + str(len(label_counts)))
    
    #frequency distribution
    high_freq = 0
    medium_freq = 0
    low_freq = 0
    singleton_count = 0
    for count in label_counts.values():
        if count >= 100:
            high_freq = high_freq + 1
        elif count >= 10:
            medium_freq = medium_freq + 1
        elif count >= 2:
            low_freq = low_freq + 1
        else:
            singleton_count = singleton_count + 1
    

    print("\nFREQUENCY DISTRIBUTION:")
    print("Labels with 100+ uses: " + str(high_freq))
    print("Labels with 10-99 uses: " + str(medium_freq))
    print("Labels with 2-9 uses: " + str(low_freq))
    print("Labels with 1 use: " + str(singleton_count))
    
    #top 30 labels
    print("")
    print("LABELS BY FREQUENCY:")
    for label, count in label_counts.most_common():
        print(label + ": " + str(count))
    
    #formatting variants
    print("\nFORMATTING VARIANTS:")
    for normalised_form in sorted(formatting_variants.keys()):
        variants = formatting_variants[normalised_form]
        print("'" + normalised_form + "':")
        for variant in variants:
            print("  - " + variant + ": " + str(label_counts[variant]))
    
    #singleton labels
    singletons = []
    for label, count in label_counts.items():
        if count == 1:
            singletons.append(label)
    sorted_singletons = sorted(singletons)
    
    print("\nSINGLETON LABELS (" + str(len(singletons)) + " labels with 1 use):")
    for label in sorted_singletons:
        print(label)



def main():       
    filepath = "graph_dump_robust.json"
    print("Loading: " + filepath)
    
    nodes = load_nodes(filepath)
    print(str(len(nodes)) + " nodes")
    
    entity_nodes = filter_entity_nodes(nodes)
    label_counts = count_labels(entity_nodes)
    formatting_variants = find_formatting_variants(label_counts)
    
    print_report(entity_nodes, label_counts, formatting_variants)


if __name__ == '__main__':
    main()
