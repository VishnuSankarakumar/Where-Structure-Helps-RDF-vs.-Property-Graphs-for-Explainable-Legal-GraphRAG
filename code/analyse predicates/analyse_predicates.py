#Group predicates by verb stem to inform mapping decisions
import json
import sys
from collections import defaultdict, Counter


def load_relationships(filepath):
    #load relationships from neo4j dump
    relationships = []
    with open(filepath, 'r') as f:
        for line in f:
            item = json.loads(line.strip())
            if item['type'] == 'relationship':
                relationships.append(item)
    return relationships


def filter_semantic(relationships):
    #keep only semantic relationships
    skip = {'SIMILAR', 'NEXT_CHUNK', 'HAS_ENTITY', 'PART_OF', 'FIRST_CHUNK'}
    semantic_rels = []
    for rel in relationships:
        if rel['label'] not in skip:
            semantic_rels.append(rel)
    return semantic_rels


def group_by_verb_stem(relationships):
    #group predicates by first word and count
    pred_counts = Counter()
    for rel in relationships:
        predicate_label = rel['label']
        pred_counts[predicate_label] = pred_counts[predicate_label] + 1
        #pred_counts = [predicate1:count, predicate2:count, ...]
    
    stem_groups = defaultdict(list)
    for pred in pred_counts:
        stem = pred.split('_')[0]
        count = pred_counts[pred]
        stem_groups[stem].append((pred, count))
        #stem_groups in the dict form 'stem': [('stem_variation', count), ...]
        #it a dictionary: key = stem and each value is list of tuples
    
    stem_totals = {}
    for stem in stem_groups: #for each stem
        preds = stem_groups[stem] #get the list of tuples for that stem
        total = 0
        for _, count in preds: #sum the counts for each predicate
            total += count
        stem_totals[stem] = total #append the stem and total count for that stem
    
    return stem_groups, stem_totals


def main():    
    filepath = "graph_dump_robust.json"
    relationships = load_relationships(filepath)
    semantic_relations = filter_semantic(relationships)
    stem_groups, stem_totals = group_by_verb_stem(semantic_relations)
    
    print("VERB STEM GROUPS\n")    
    sorted_stems = sorted(stem_totals.items(), key=lambda x: -x[1]) #AI assistance used here (lambda sorting)
    for stem, stem_total in sorted_stems:
        print(stem + " (" + str(stem_total) + "):")
        sorted_preds = sorted(stem_groups[stem], key=lambda x: -x[1]) #AI assistance used here (lambda sorting)
        for pred, count in sorted_preds:
            print("    " + pred + ": " + str(count))
        print("")


if __name__ == '__main__':
    main()
