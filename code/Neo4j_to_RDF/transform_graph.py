#neo4j to rdf transformation script
#from neo4j export to RDF
#output tbox (ontology) and abox (instances). 2 turtle files

from datetime import datetime
from collections import Counter
import json, re, sys, os
from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, RDFS, OWL, XSD, DC, DCTERMS

from mapping_table import (
    CLASS_HIERARCHY,
    LABEL_MAPPING,
    IGNORE_LABELS,
    PROPERTY_HIERARCHY,
    INVERSE_PROPERTIES,
    get_predicate_mapping, #new get mapping method handles both PREDICATE_MAPPING and VERB_STEM_MAPPING so not needed anymore
)


#NAMESPACE SETUP
#define rdflib namespaces
#at least three namespaces needed:
#ontology schema (tbox schema) - (possible name - ontology)
#entity instances (possible name - resource)
#chunk instances (possible name chunk)
#if chunk/document metadata is being kept, store it in a separate namespace. standard practice to keep as distinct fragment of graph

BASE_URI = "https://euaiact.eu/"
EUAI = Namespace("https://euaiact.eu/ontology#") #schema
EUAI_R = Namespace("https://euaiact.eu/resource/") #entities
EUAI_C = Namespace("https://euaiact.eu/chunk/") #chunks

#POSSIBLE HELPER FUNCTIONS NEEDED
#uri normalisation method 
# -- convert entity names to valid uri fragments
# -- normalise existing labels - strip whitespace, leading/trailing underscores, non-word characters



#sanitise_uri
# -- convert text to a valid uri
# -- neo4j entity names contain spaces/special characters - invalid for uris   



def sanitise_uri(text):
    #convert text to a valid uri
    #neo4j entity names contain spaces/special characters - invalid for uris

    if not text:
        return "error - not text"
    
    
    text = str(text) #convert to string   
    text = re.sub(r'[^\w\-]', '_', text) #replace non word characters but keep hyphens
    text = re.sub(r'_+', '_', text) #remove consecutive underscores
    text = text.strip('_') #remove leading/trailing underscores
    
    #truncate if too long (uri cannot be overly long)
    if len(text) > 100:
        text = text[:100].rstrip('_') #make sure last char is not a _
    
    return text



#load_neo4j_dump 
# -- ingest neo4j json dump (SAME AS IN ANALYSIS SCRIPT)
# -- sort into nodes/relations

def load_neo4j_dump(filepath):
    nodes = []
    relationships = []
    
    print("Ingesting Neo4J dump...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            if item.get('type') == 'node':
                nodes.append(item)
            elif item.get('type') == 'relationship':
                relationships.append(item)
    
    print(f"--- Say hello to {len(nodes)} nodes")
    print(f"--- Say hello to {len(relationships)} relationships")
    
    return nodes, relationships



#categorise_nodes 
# -- separate entities, chunks, documents so that each can be mapped/declared appropriately
# -- instructions for mapping each type explicitly needed in mapping table script

def categorise_nodes(nodes):
    #sort nodes into entity nodes, chunk nodes, document nodes

    entity_nodes = []
    chunk_nodes = []
    document_nodes = []
    
    for node in nodes:
        labels = node.get('labels', []) #returns empty list if labels not found
        
        if 'Chunk' in labels:
            chunk_nodes.append(node)
        elif 'Document' in labels and '__Entity__' not in labels:
            document_nodes.append(node)
        elif '__Entity__' in labels:
            entity_nodes.append(node)
        else: #other nodes (rare)
            document_nodes.append(node)
    
    return entity_nodes, chunk_nodes, document_nodes



#categorise_relationships 
# -- separate semantic, provenance, structural so that each can be mapped/declared appropriately
# -- instructions for mapping each type explicitly needed in mapping table script

def categorise_relationships(relationships):
    #Separate relationships by type.

    #create dict where each key (category) contains the relevant values (relationships)
    #these categories predefined by initial Neo4J graph creation prior!!!!
    categories = {
        'semantic': [], #entity-to-entity IMPORTANT
        'has_entity': [], #chunk-to-entity
        'part_of': [], #chunk-to-document
        'similar': [], #vector similarity TO BE DROPPED
        'next_chunk': [], #sequential info TO BE DROPPED
        'first_chunk': [], #document start TO BE DROPPED
        'other': [], #other
    }
    
    for rel in relationships:
        label = rel.get('label', '') #return '' if label key not found 
        
        #append relation to correct dictionary key
        if label == 'HAS_ENTITY':
            categories['has_entity'].append(rel)
        elif label == 'PART_OF':
            categories['part_of'].append(rel)
        elif label == 'SIMILAR':
            categories['similar'].append(rel)
        elif label == 'NEXT_CHUNK':
            categories['next_chunk'].append(rel)
        elif label == 'FIRST_CHUNK':
            categories['first_chunk'].append(rel)
        else:
            categories['semantic'].append(rel) #anything that doesnt fall into the above categories is a semantic relation
    
    return categories





#TBOX -- create ontology schema. 
# - declare as triples of type ontology. add appropriate metadata
# - declare class hierarchy using instructions (stored as dict) from mapping_table.py.
# - declare relation hierarchy using instructions (stored as dict) from mapping_table.py
# - declare inverse relations using instructions from mapping_table.py
# - declare chunk objects using instructions form mapping_table.py

    #create empty graph
    
    #ONTOLOGY DECLARATION
    #declare ontology uri with label and comment
    
    #CLASS HIERARCHY
    #for each class in class hierarchy from mapping table
    #declare as owl class
    #if has parent, add subclass triple
    
    #PROPERTY HIERARCHY
    #for each property in relations hierarchy
    #declare as owl property
    #if has parent, declare subproperty
    
    #INVERSE PROPERTIES
    #for each pair in inverse relations from mapping table:
    #declare inverse property if not already exists
    #declare with owl inverse property
    
    #declare chunk metadata properties e.g. chunkText, pageNumber, etc    
    #return graph
    
def generate_tbox():
    #generate the tbox (terminological box)
    #contains class hierarchy, property hierarchy, inverse declarations, datatype properties
    
    g = Graph() #create rdf graph structure
    
    #bind prefixes so that triples do not have to be written out completely every time
    #uris for each below already defined. euai is defined above. rest defined in source code.
    #so instead of the graph storing entire triples in full form with full uris
    #it stores the prefix bound shortened versions
    g.bind('euai', EUAI)
    g.bind('owl', OWL)
    g.bind('rdfs', RDFS)
    g.bind('rdf', RDF)
    g.bind('xsd', XSD)
    g.bind('dc', DC)
    g.bind('dcterms', DCTERMS)
    
    #ONTOLOGY DECLARATION
    ontology_uri = URIRef(f"{BASE_URI}ontology")
    #g.add() methods adds an rdf triple to the graph
    #so subject, predicate, object
    
    #declare ontology meta data
    #ALONGSIDE all other data, stored as triples
    #classes and relations are all stored under this top level ontology object
    g.add((ontology_uri, RDF.type, OWL.Ontology))
    g.add((ontology_uri, RDFS.label, Literal("EU AI Act Knowledge Graph Ontology")))
    g.add((ontology_uri, RDFS.comment, Literal("Ontology for the EU AI Act knowledge graph, " "transformed from Neo4j LLM-extracted graph. " "Designed for Graph RAG comparison study.")))
    
    #research-suggested addons
    g.add((ontology_uri, DCTERMS.created, Literal(datetime.now().strftime("%Y-%m-%d"))))
    g.add((ontology_uri, DCTERMS.creator, Literal("Masters Project")))
    
    #CLASS HIERARCHY DECLARATION
    print("Handling class hierarchy...")
    class_count = 0
    
    #class hierarchy is defined in mapping_config.py file
    #as a dictionary where keys are classes, values are that class's parent
    for class_name, parent_name in CLASS_HIERARCHY.items():
        class_uri = EUAI[class_name] #specify prefix to use.
        
        #declare as OWL class
        g.add((class_uri, RDF.type, OWL.Class)) #declare as owl class rather than rdfs class since we declare inverse properties
        g.add((class_uri, RDFS.label, Literal(class_name)))
        
        #declare subclass if parent exists
        #so if LegalEntity: Entity
        #Legal Entity declared as subclass of Entity
        if parent_name:
            parent_uri = EUAI[parent_name]
            g.add((class_uri, RDFS.subClassOf, parent_uri))
        
        class_count += 1
    
    print(f"--- Created {class_count} classes")
    
    #PROPERTY HIERARCHY DECLARATION
    #types of relations sorted into hierarchy
    print("Handling relation property hierarchy...")
    prop_count = 0
    
    
    #similar property/parent structure used here
    for prop_name, parent_name in PROPERTY_HIERARCHY.items():
        prop_uri = EUAI[prop_name]
        
        #declare as OWL ObjectProperty
        #objectproperty links two entities
        #as opposed to datatypeproperty which links an entity to a single value
        g.add((prop_uri, RDF.type, OWL.ObjectProperty))
        g.add((prop_uri, RDFS.label, Literal(prop_name)))
        
        #declare as subclass if parent exists
        if parent_name:
            parent_uri = EUAI[parent_name]
            g.add((prop_uri, RDFS.subPropertyOf, parent_uri))
        
        prop_count += 1
    
    print(f"--- Created {prop_count} object properties")
    
    #INVERSE PROPERTY DECLARATION
    #for bidrectional traversal
    print("Handling inverse properties...")
    inverse_count = 0
    
    #inverses defined in mapping config.
    #keys are properties, values are inverse    
    for prop_name, inverse_name in INVERSE_PROPERTIES.items():
        prop_uri = EUAI[prop_name]
        inverse_uri = EUAI[inverse_name]
        
        #check if inverse property already declared in graph
        #if not create it with same parent as original property
        if (inverse_uri, RDF.type, OWL.ObjectProperty) not in g:
            g.add((inverse_uri, RDF.type, OWL.ObjectProperty))
            g.add((inverse_uri, RDFS.label, Literal(inverse_name)))
            
            #find parent of original property and assign same parent to inverse
            #so if enactedBy is under enactmentRelation, enacts also goes under enactmentRelation
            #line below is open query any parents of the specific URI handled right now
            #it is a for loop because a property could have more than one parent
            #we declare inverse exists as sub class of each existing parent
            for _, _, parent in g.triples((prop_uri, RDFS.subPropertyOf, None)):
                g.add((inverse_uri, RDFS.subPropertyOf, parent))
        
        #declare inverse relationship bidirectionally
        #owl requires both directions to be stated explicitly
        g.add((prop_uri, OWL.inverseOf, inverse_uri))
        g.add((inverse_uri, OWL.inverseOf, prop_uri))
        
        inverse_count += 1
    
    print(f"--- Created {inverse_count} inverse property pairs")
    
    #DATATYPE PROPERTY DECLARATION
    #datatype properties link entities to string/integer values
    #these are specifically for chunk metadata ONLY!!!!
    print("Handling datatype properties...")
    
    #tuples containing property name, description, and xsd datatype
    datatype_properties = [
        ('chunkText', 'Text content of document chunk', XSD.string),
        ('pageNumber', 'Page number of chunk', XSD.integer),
        ('position', 'Position of chunk within document', XSD.integer),
        ('fileName', 'Source file name', XSD.string),
        ('contentOffset', 'Character offset in source document', XSD.integer),
    ]
    
    for prop_name, description, datatype in datatype_properties:
        prop_uri = EUAI[prop_name]
        g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
        g.add((prop_uri, RDFS.label, Literal(prop_name)))
        g.add((prop_uri, RDFS.comment, Literal(description)))
        g.add((prop_uri, RDFS.domain, EUAI['DocumentChunk']))
        g.add((prop_uri, RDFS.range, datatype))
        #domain constrains subject, range constrains object, standard rdf concept
        #domain: why type of entity has this property?
        #range: what type of value does this property hold?
        
    print(f"--- Created {len(datatype_properties)} datatype properties")
    
    #SPECIAL OBJECT PROPERTIES
    #these are object properties that dont fit into the main hierarchy
    #but are needed for graph structure
    #there is a good chance these dont end up being used, 
    #but implementing anyway to cover all bases
    mentioned_uri = EUAI['mentionedInChunk']
    g.add((mentioned_uri, RDF.type, OWL.ObjectProperty))
    g.add((mentioned_uri, RDFS.label, Literal("mentionedInChunk")))
    g.add((mentioned_uri, RDFS.comment, Literal("Links entity to document chunk where it is mentioned")))
    g.add((mentioned_uri, RDFS.range, EUAI['DocumentChunk']))
    g.add((mentioned_uri, RDFS.subPropertyOf, EUAI['relation']))
    
    #chunkOf links chunks to their source document
    chunk_of_uri = EUAI['chunkOf']
    g.add((chunk_of_uri, RDF.type, OWL.ObjectProperty))
    g.add((chunk_of_uri, RDFS.label, Literal("chunkOf")))
    g.add((chunk_of_uri, RDFS.comment, Literal("Links document chunk to source document")))
    g.add((chunk_of_uri, RDFS.domain, EUAI['DocumentChunk']))
    g.add((chunk_of_uri, RDFS.subPropertyOf, EUAI['relation'])) #BUG FIXED - minor typo fixed
    
    print(f"--- TBox complete: {len(g)} triples")
    
    return g






#ABOX -- create instance data
# - process entity nodes 
# --- label mapping (instructions from mapping_table) 
# --- uri minting using helper method to translate existing labels into usable uri names
# --- adding type details
# - process chunk nodes (metadata properties)
# - process semantic relationships 
# --- predicate mapping using instructions from mapping_table.py
# --- direction flipping using inverse properties from mapping_table.py

#def generate_abox(entity_nodes, chunk_nodes, rel_categories):
    #create empty graph
    
    #use some dict to track neo4j id -> rdf uri mappings
    #use some dict to track node/relation counts
    
    #PROCESS ENTITIES
    #for each entity node:
    #    filter out labels to ignore from mapping table
       # map remaining labels to rdf classes using label mappings from mapping table
       # add type triple for each mapped class
    #    add label triple for entity name
      #  add comment from description if exists
    
    #PROCESS CHUNKS
    #for each chunk node:
        #create uri
        #store in uri mapping table
        #add chunk type triple
        #add meta properties: text, pageNumber, position etc
       # declare types for properties e.g. string/integer
    
    #PROCESS SEMANTIC RELATIONSHIPS
    #same as processing entities
    #make sure to declare inverses if any
    
def generate_abox(nodes, relationships):
    #generate the abox (assertion box)
    #abox contains actual instance data - the entities, chunks, and relationships
    #as opposed to tbox which defines the schema/structure
    g = Graph()
    
    #bind prefixes for readablility
    #euai_r for entity resources, euai_c for chunk resources
    g.bind('euai', EUAI)
    g.bind('euai_r', EUAI_R)
    g.bind('euai_c', EUAI_C)
    g.bind('rdfs', RDFS)
    g.bind('rdf', RDF)
    g.bind('xsd', XSD)
    
    #insight tracking - counter objects
    stats = {
        'entities_created': 0,
        'chunks_created': 0,
        'semantic_rels_created': 0,
        'provenance_rels_created': 0,
        'structure_rels_created': 0,
        'rels_flipped': 0,
        'unmapped_labels': Counter(),
        'unmapped_predicates': Counter(),
        'predicate_usage': Counter(),
    }
    
    #uri_map stores neo4j id to rdf uri mapping
    #neo4j internal ids and rdf uris both need to be looked up to process relations
    #using this map
    uri_map = {}
    
    #categorise nodes and relationships using helper functions
    entity_nodes, chunk_nodes, document_nodes = categorise_nodes(nodes)
    rel_categories = categorise_relationships(relationships)
    
    #ENTITY PROCESSING
    print("Handling entities...")
    
    for node in entity_nodes:
        neo4j_id = node['id']
        #filter out system labels like __Entity__ that we dont want in rdf
        #also filter out edges with only one use in neo4j graph
        #list specified in mapping_config
        labels = [l for l in node.get('labels', []) if l not in IGNORE_LABELS]
        props = node.get('properties', {})
        
        #get entity name from id property
        #this is neo4j graph buider default
        entity_name = props.get('id', 'unnamed')
        
        #determine rdf classes from neo4j labels
        #an entity can have multiple types in rdf 
        #no single inheritance constraint
        rdf_classes = []
        primary_class = 'Entity'  #default fallback
        
        for label in labels:
            if label in LABEL_MAPPING:
                mapped_class = LABEL_MAPPING[label]
                rdf_classes.append(mapped_class)
                #use first mapped class as primary for uri construction
                if primary_class == 'Entity':
                    primary_class = mapped_class
            else:
                stats['unmapped_labels'][label] += 1
        
        if not rdf_classes:
            rdf_classes = ['Entity']
        
        #create uri using primary class and sanitised name
        #pattern: https://euaiact.eu/resource/Class/Name
        #including class in uri avoids collisions and improves readability
        uri_local = f"{primary_class}/{sanitise_uri(entity_name)}"
        entity_uri = EUAI_R[uri_local]
        uri_map[neo4j_id] = entity_uri #update map to enable lookup
        
        #add type assertions - one for each mapped class
        for rdf_class in set(rdf_classes):
            g.add((entity_uri, RDF.type, EUAI[rdf_class]))
        
        #add readable label
        g.add((entity_uri, RDFS.label, Literal(entity_name)))
        
        #add description if present in json dump rpoperties
        if 'description' in props:
            g.add((entity_uri, RDFS.comment, Literal(props['description'])))
        
        stats['entities_created'] += 1
    
    print(f"--- Created {stats['entities_created']} entity resources")
    
    #CHUNK PROCESSING
    print("Handling chunks...")
    
    for node in chunk_nodes:
        neo4j_id = node['id']
        props = node.get('properties', {})
        
        #chunks use hashed ids from llm graph builder
        #sanitise and set rdf chunk id the same
        chunk_id = props.get('id', neo4j_id)
        chunk_uri = EUAI_C[sanitise_uri(str(chunk_id))]
        uri_map[neo4j_id] = chunk_uri
        
        #all chunks are documentchunk type
        g.add((chunk_uri, RDF.type, EUAI['DocumentChunk']))
        
        #add present chunk properties
        if 'text' in props:
            g.add((chunk_uri, EUAI['chunkText'], Literal(props['text'])))
        
        if 'page_number' in props:
            try:
                page = int(props['page_number'])
                g.add((chunk_uri, EUAI['pageNumber'], Literal(page, datatype=XSD.integer)))
            except (ValueError, TypeError):
                pass
        
        if 'position' in props:
            try:
                pos = int(props['position'])
                g.add((chunk_uri, EUAI['position'], Literal(pos, datatype=XSD.integer)))
            except (ValueError, TypeError):
                pass
        
        if 'fileName' in props:
            g.add((chunk_uri, EUAI['fileName'], Literal(props['fileName'])))
        
        if 'content_offset' in props:
            try:
                offset = int(props['content_offset'])
                g.add((chunk_uri, EUAI['contentOffset'], Literal(offset, datatype=XSD.integer)))
            except (ValueError, TypeError):
                pass
        
        stats['chunks_created'] += 1
    
    print(f"--- Created {stats['chunks_created']} chunk resources")
    
    #DOCUMENT NODE PROCESSING
    #these are the source document nodes that chunks belong to
    for node in document_nodes:
        neo4j_id = node['id']
        props = node.get('properties', {})
        
        doc_name = props.get('id', props.get('fileName', 'unnamed'))
        doc_uri = EUAI_R[f"Document/{sanitise_uri(doc_name)}"] #BUG FIXED: DOC NAME WAS NOT SANITISED BEFORE PASSING SO THREW AN ERROR
        uri_map[neo4j_id] = doc_uri
        
        g.add((doc_uri, RDF.type, EUAI['LegalDocument']))
        g.add((doc_uri, RDFS.label, Literal(doc_name)))
    
    #SEMANTIC RELATIONSHIP PROCESSING
    #these are the entity-to-entity relationships extracted by the llm
    print("Handling semantic relationships...")
    
    for rel in rel_categories['semantic']:
        start_id = rel['start_id']
        end_id = rel['end_id']
        rel_type = rel['label']
        
        #look up rdf uris from our mapping
        start_uri = uri_map.get(start_id)
        end_uri = uri_map.get(end_id)
        
        #skip if either endpoint not found (shouldnt happen but safety check)
        if not start_uri or not end_uri:
            continue
        
        #get predicate mapping from mapping_config.py
        #returns tuple of (rdf_property, parent_property, should_flip)
        #flip is true for relatios like GOVERNED_BY that need direction reversed
        rdf_prop, parent_prop, flip = get_predicate_mapping(rel_type) #BUG FIXED -- METHOD IMPORT WAS NOT WORKING DUE TO DIRECTORY FORMAT ERROR. NOW FIXED
        
        #track usage
        stats['predicate_usage'][rdf_prop] += 1
        if parent_prop == 'otherRelation':
            stats['unmapped_predicates'][rel_type] += 1
        
        #create property URI
        prop_uri = EUAI[rdf_prop]
        
        #add triple, flipping direction if needed
        if flip:
            g.add((end_uri, prop_uri, start_uri))
            stats['rels_flipped'] += 1
        else:
            g.add((start_uri, prop_uri, end_uri))
        
        stats['semantic_rels_created'] += 1
    
    print(f"--- Created {stats['semantic_rels_created']} semantic relationships")
    print(f"--- Flipped {stats['rels_flipped']} possible inverse relationships")
    
    #PROVENANCE LINK PROCESSING
    #has_entity relations link chunks to entities mentioned in them
    #in neo4j its chunk HAS ENTITY
    #we reverse to ENTITY MENTIONED IN CHUNK
    print("Handling provenance links...")
    
    for rel in rel_categories['has_entity']:
        chunk_id = rel['start_id']
        entity_id = rel['end_id']
        
        chunk_uri = uri_map.get(chunk_id)
        entity_uri = uri_map.get(entity_id)
        
        if chunk_uri and entity_uri:
            g.add((entity_uri, EUAI['mentionedInChunk'], chunk_uri))
            stats['provenance_rels_created'] += 1
    
    print(f"--- Created {stats['provenance_rels_created']} provenance links")
    
    #STRUCTURE LINK PROCESSING
    #part_of relationships link chunks to their source documents
    print("Handling structure links...")
    
    for rel in rel_categories['part_of']:
        chunk_id = rel['start_id']
        doc_id = rel['end_id']
        
        chunk_uri = uri_map.get(chunk_id)
        doc_uri = uri_map.get(doc_id)
        
        if chunk_uri and doc_uri:
            g.add((chunk_uri, EUAI['chunkOf'], doc_uri))
            stats['structure_rels_created'] += 1
    
    print(f"--- Created {stats['structure_rels_created']} structure links")
    

    print(f"ABox complete: {len(g)} triples")
    
    #dropped relationships
    dropped = (len(rel_categories['similar']) + 
               len(rel_categories['next_chunk']) + 
               len(rel_categories['first_chunk']))
    print(f"--  Dropped {dropped} non-semantic relationships (SIMILAR, NEXT_CHUNK, FIRST_CHUNK)")
    
    return g, stats

def generate_report(stats, tbox_size, abox_size, output_path):
    lines = [
        f"triples - tbox: {tbox_size}, abox: {abox_size}, total: {tbox_size + abox_size}",
        f"entities: {stats['entities_created']}, chunks: {stats['chunks_created']}",
        f"rels - semantic: {stats['semantic_rels_created']}, mentionedInChunk: {stats['provenance_rels_created']}, chunkOf: {stats['structure_rels_created']}, flipped: {stats['rels_flipped']}",
        "",
    ]

    if stats['unmapped_labels']:
        lines.append(f"unmapped labels ({len(stats['unmapped_labels'])} created under generic 'entity'):")
        for label, count in stats['unmapped_labels'].items():
            lines.append(f"  {label}: {count}")
        lines.append("")

    if stats['unmapped_predicates']:
        total = sum(stats['unmapped_predicates'].values())
        lines.append(f"unmapped predicates ({total} created under generic 'otherRelation'):")
        for pred, count in stats['unmapped_predicates'].items():
            lines.append(f"  {pred}: {count}")
        lines.append("")

    lines.append("top predicates:")
    for pred, count in stats['predicate_usage'].most_common(20):
        lines.append(f"  euai:{pred}: {count}")

    print("\n".join(lines))


def main():
    if len(sys.argv) < 3:
        print("usage: python transform_graph.py graph_dump_robust [output dir]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    print("loading dump...")
    nodes, relationships = load_neo4j_dump(input_file)

    print("tbox...")
    tbox = generate_tbox()
    tbox_path = os.path.join(output_dir, "euaiact-tbox.ttl")
    tbox.serialize(destination=tbox_path, format='turtle')

    print("abox...")
    abox, stats = generate_abox(nodes, relationships)
    abox_path = os.path.join(output_dir, "euaiact-abox.ttl")
    abox.serialize(destination=abox_path, format='turtle')

    print("report...")
    report_path = os.path.join(output_dir, "transform-report.txt")
    generate_report(stats, len(tbox), len(abox), report_path)

    print(f"\n{len(tbox) + len(abox)} triples written to {output_dir}")


if __name__ == '__main__':
    main()