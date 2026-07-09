
#NOTE: LABEL AND PREDICATE MAPPINGS BUILT VIA HUMAN-IN-THE-LOOP WORKFLOW. LLM SUGGESTED VAGUE SEMANTIC ASSOCIATIONS TO REDUCE TEDIUM, BUT EVERY SINGLE MAPPING/HIERARCHY WAS MANUALLY REVIEWED AND APPROVED/CORRECTED BY ME.

#mapping configuration for neo4j to rdf transformation
#contains all label and predicate mappings
#this file is imported by the transformation script (03_transform.py)

#class and relation hierarchies below are for tbox (ontology/schema)

#CLASS HIERARCHY
#rdf triple store subclass like [GovernmentBody -> subclassof -> Government]
#using dict we can represent similarly GovernmentBody (key): Government (value)
#key value pairs should be best way to automate ingestion/creation of class hierarchy ontology
#O(1) time
CLASS_HIERARCHY = {
    #top-level
    'Entity': None,
    
    #legal entity branch 
    'LegalEntity': 'Entity',
    'LegalInstrument': 'LegalEntity',
    'Regulation': 'LegalInstrument',
    'Directive': 'LegalInstrument',
    'Treaty': 'LegalInstrument',
    'LegalProvision': 'LegalEntity',
    'Article': 'LegalProvision',
    'Section': 'LegalProvision',
    'Chapter': 'LegalProvision',
    'Annex': 'LegalProvision',
    'Recital': 'LegalProvision',
    'LegalConcept': 'LegalEntity',
    'LegalDocument': 'LegalEntity',
    'Publication': 'LegalDocument',
    
    #actor branch - people, organisations, stakeholders
    'Actor': 'Entity',
    'Organization': 'Actor',
    'GovernmentBody': 'Organization',
    'Company': 'Organization',
    'Person': 'Actor',
    'Group': 'Person',
    'Stakeholder': 'Actor',
    'MarketActor': 'Actor',
    
    #system branch
    'System': 'Entity',
    'AISystem': 'System',
    'AIComponent': 'AISystem',
    'ITSystem': 'System',
    'SystemComponent': 'System',
    
    #technical standalone classes
    'AIModel': 'Entity',
    'Model': 'Entity',
    'Algorithm': 'Entity',
    'Technology': 'Entity',
    
    #process branch
    'Process': 'Entity',
    'Activity': 'Process',
    'Procedure': 'Process',
    'Method': 'Process',
    
    #data branch
    'Data': 'Entity',
    'Database': 'Data',
    
    #product branch
    'Product': 'Entity',
    'Service': 'Product',
    
    #requirement branch
    'Requirement': 'Entity',
    'Obligation': 'Requirement',
    'Standard': 'Requirement',
    'Constraint': 'Requirement',
    
    #right branch
    'Right': 'Entity',
    'FundamentalRight': 'Right',
    
    #interest branch
    'Interest': 'Entity',
    'ProtectedInterest': 'Interest',
    'PublicInterest': 'Interest',
    
    #other legal concepts
    'Consent': 'Entity',
    'Access': 'Entity',
    
    #risk branch
    'Risk': 'Entity',
    'Harm': 'Risk',
    'HarmType': 'Harm',
    'Threat': 'Risk',
    'Hazard': 'Threat',
    'Attack': 'Threat',
    'RiskArea': 'Risk',
    'RiskCategory': 'Risk',
    'RiskLevel': 'Risk',
    'RiskClassification': 'Risk',
    'Vulnerability': 'Risk',
    
    #characteristic branch
    'Characteristic': 'Entity',
    'Role': 'Characteristic',
    'LegalRole': 'Role',
    
    #concept branch
    'Concept': 'Entity',
    'Policy': 'Concept',
    'Principle': 'Concept',
    'Objective': 'Concept',
    'Sector': 'Concept',
    'Guidance': 'Concept',
    
    #location branch
    'Location': 'Entity',
    'Country': 'Location',
    'Region': 'Location',
    
    'Infrastructure': 'Entity',
    'Jurisdiction': 'Entity',
    
    #event branch
    'Event': 'Entity',
    'Decision': 'Event',
    'Incident': 'Event',
    
    'Lifecycle': 'Entity',
    'Development': 'Entity',
    
    #special class for chunks
    'DocumentChunk': 'Entity',
}

#PROPERTY HIERARCHY i.e. RELATION HIERARCHY
#format: [Relation: ParentRelation] or None for top-level
#this data will be used to declare rdfs:subPropertyOf relationships in tbox, enabling internal inference ability
PROPERTY_HIERARCHY = {
    #top-level property - all semantic relationships are subproperties of this
    'relation': None,
    
    #24 parent properties
    'enactmentRelation': 'relation',
    'modificationRelation': 'relation',
    'regulatoryRelation': 'relation',
    'applicationRelation': 'relation',
    'requirementRelation': 'relation',
    'structuralRelation': 'relation',
    'usageRelation': 'relation',
    'provisionRelation': 'relation',
    'supportRelation': 'relation',
    'effectRelation': 'relation',
    'protectionRelation': 'relation',
    'associationRelation': 'relation',
    'referenceRelation': 'relation',
    'classificationRelation': 'relation',
    'establishmentRelation': 'relation',
    'actionRelation': 'relation',
    'cooperationRelation': 'relation',
    'targetingRelation': 'relation',
    'involvementRelation': 'relation',
    'derivationRelation': 'relation',
    'scopeRelation': 'relation',
    'considerationRelation': 'relation',
    'assessmentRelation': 'relation',
    'assignmentRelation': 'relation',
    'otherRelation': 'relation',  #fall back option for unmapped ones
    
    #leaf properties under enactmentRelation
    'enactedBy': 'enactmentRelation',
    'issuedBy': 'enactmentRelation',
    'adoptedBy': 'enactmentRelation',
    'publishedIn': 'enactmentRelation',
    
    #leaf properties under modificationRelation - how laws change
    'amends': 'modificationRelation',
    'amendedBy': 'modificationRelation',
    'repeals': 'modificationRelation',
    'repealedBy': 'modificationRelation',
    
    #leaf properties under regulatoryRelation
    'regulates': 'regulatoryRelation',
    'regulatedBy': 'regulatoryRelation',
    'prohibits': 'regulatoryRelation',
    'restricts': 'regulatoryRelation',
    'allows': 'regulatoryRelation',
    
    #leaf properties under applicationRelation
    'appliesTo': 'applicationRelation',
    'appliedIn': 'applicationRelation',
    
    #leaf properties under requirementRelation
    'requires': 'requirementRelation',
    'requiredBy': 'requirementRelation',
    'mustComplyWith': 'requirementRelation',
    'compliesWith': 'requirementRelation',
    'subjectTo': 'requirementRelation',
    'hasObligation': 'requirementRelation',
    'hasRequirement': 'requirementRelation',
    
    #leaf properties under structuralRelation
    'includes': 'structuralRelation',
    'includedIn': 'structuralRelation',
    'comprises': 'structuralRelation',
    'has': 'structuralRelation',
    'hasCharacteristic': 'structuralRelation',
    'hasRisk': 'structuralRelation',
    'hasRight': 'structuralRelation',
    'hasIdentifier': 'structuralRelation',
    'hasPurpose': 'structuralRelation',
    'hasObjective': 'structuralRelation',
    'partOf': 'structuralRelation',
    'integratedInto': 'structuralRelation',
    
    #leaf properties under usageRelation
    'uses': 'usageRelation',
    'usedBy': 'usageRelation',
    'usedFor': 'usageRelation',
    'usedIn': 'usageRelation',
    'intendedFor': 'usageRelation',
    
    #leaf properties under provisionRelation
    'provides': 'provisionRelation',
    'providedBy': 'provisionRelation',
    'ensures': 'provisionRelation',
    'enables': 'provisionRelation',
    
    #leaf properties under supportRelation
    'supports': 'supportRelation',
    'supportedBy': 'supportRelation',
    'facilitates': 'supportRelation',
    'promotes': 'supportRelation',
    'contributesTo': 'supportRelation',
    
    #leaf properties under effectRelation
    'affects': 'effectRelation',
    'affectedBy': 'effectRelation',
    'leadsTo': 'effectRelation',
    'causes': 'effectRelation',
    'produces': 'effectRelation',
    
    #leaf properties under protectionRelation
    'protects': 'protectionRelation',
    'protectedBy': 'protectionRelation',
    'threatens': 'protectionRelation',
    
    #leaf properties under associationRelation - generic connections
    'relatedTo': 'associationRelation',
    'associatedWith': 'associationRelation',
    'about': 'associationRelation',
    
    #leaf properties under referenceRelation
    'definedIn': 'referenceRelation',
    'listedIn': 'referenceRelation',
    'mentionedIn': 'referenceRelation',
    'setOutIn': 'referenceRelation',
    'refersTo': 'referenceRelation',
    'describes': 'referenceRelation',
    
    #leaf properties under classificationRelation
    'isA': 'classificationRelation',
    'classifiedAs': 'classificationRelation',
    'belongsTo': 'classificationRelation',
    'resembles': 'classificationRelation',
    
    #leaf properties under establishmentRelation
    'establishes': 'establishmentRelation',
    'establishedBy': 'establishmentRelation',
    'establishedIn': 'establishmentRelation',
    'designates': 'establishmentRelation',
    
    #leaf properties under actionRelation
    'performs': 'actionRelation',
    'carriesOut': 'actionRelation',
    'implements': 'actionRelation',
    'develops': 'actionRelation',
    'operates': 'actionRelation',
    
    #leaf properties under cooperationRelation
    'cooperatesWith': 'cooperationRelation',
    'consults': 'cooperationRelation',
    'reportsTo': 'cooperationRelation',
    
    #leaf properties under targetingRelation
    'targets': 'targetingRelation',
    'aimsTo': 'targetingRelation',
    'for': 'targetingRelation',
    'addresses': 'targetingRelation',
    
    #leaf properties under involvementRelation
    'involves': 'involvementRelation',
    'involvedIn': 'involvementRelation',
    'participatesIn': 'involvementRelation',
    
    #leaf properties under derivationRelation
    'basedOn': 'derivationRelation',
    'derivedFrom': 'derivationRelation',
    'pursuantTo': 'derivationRelation',
    'inAccordanceWith': 'derivationRelation',
    'under': 'derivationRelation',
    'withoutPrejudiceTo': 'derivationRelation',
    
    #leaf properties under scopeRelation
    'covers': 'scopeRelation',
    'excludes': 'scopeRelation',
    'placedOn': 'scopeRelation',
    
    #leaf properties under considerationRelation
    'considers': 'considerationRelation',
    'takesIntoAccount': 'considerationRelation',
    'recognizes': 'considerationRelation',
    
    #leaf properties under assessmentRelation
    'identifies': 'assessmentRelation',
    'evaluates': 'assessmentRelation',
    'assesses': 'assessmentRelation',
    'monitors': 'assessmentRelation',
    
    #leaf properties under assignmentRelation
    'chargedWith': 'assignmentRelation',
    'assigns': 'assignmentRelation',
    'assignedTo': 'assignmentRelation',
}

#INVERSE PROPERTIES

#format: [relationship: inverse relationship]
#use this to declare owl:inverseOf relationships
#enables automatic inference of bidirectional relationships
#only need to declare one direction then reasoner can infers the other
INVERSE_PROPERTIES = {
    'enactedBy': 'enacts',
    'issuedBy': 'issues',
    'adoptedBy': 'adopts',
    'amends': 'amendedBy',
    'repeals': 'repealedBy',
    'regulates': 'regulatedBy',
    'requires': 'requiredBy',
    'provides': 'providedBy',
    'affects': 'affectedBy',
    'establishes': 'establishedBy',
    'includes': 'includedIn',
    'involves': 'involvedIn',
    'supports': 'supportedBy',
    'protects': 'protectedBy',
    'uses': 'usedBy',
}



#rest of this script is for abox (instances)

#LABEL MAPPING
#maps 298 EXISTING neo4j labels to 66 declared classes above
#maps stored as dict also. key value pairs structure can avoid needing some kind of lookup table or hashing method AND its cheap
#format: [neo4j label: target class]
#many to one mapping: multiple labels can map to same class
LABEL_MAPPING = {
    #legal instrument variants
    'Law': 'LegalInstrument',
    'Regulation': 'Regulation',
    'Directive': 'Directive',
    'Treaty': 'Treaty',
    'LegalAct': 'LegalInstrument',
    'Legal Act': 'LegalInstrument',
    'Legal_Act': 'LegalInstrument',
    'LegalInstrument': 'LegalInstrument',
    'Legal_Instrument': 'LegalInstrument',
    'Legal Instrument': 'LegalInstrument',
    'Legislation': 'LegalInstrument',
    'LawType': 'LegalInstrument',
    
    #legal provision - structural parts of legal documents (potentially to use to classify source doc parts?)
    'LegalProvision': 'LegalProvision',
    'Legal Provision': 'LegalProvision',
    'Legal_Provision': 'LegalProvision',
    'Provision': 'LegalProvision',
    'Article': 'Article',
    'Legal_Article': 'Article',
    'Section': 'Section',
    'Chapter': 'Chapter',
    'Annex': 'Annex',
    'Recital': 'Recital',
    'DocumentSection': 'LegalProvision',
    
    #legal concept - abstract legal ideas
    'LegalConcept': 'LegalConcept',
    'Legal Concept': 'LegalConcept',
    'Legal_Concept': 'LegalConcept',
    'LegalFramework': 'LegalConcept',
    'Legal Framework': 'LegalConcept',
    'LegalPrinciple': 'LegalConcept',
    'Legal Principle': 'LegalConcept',
    'LegalRequirement': 'LegalConcept',
    'LegalObligation': 'LegalConcept',
    'LegalRemedy': 'LegalConcept',
    'Remedy': 'LegalConcept',
    'LegalDoctrine': 'LegalConcept',
    'Definition': 'LegalConcept',
    'RegulatoryFramework': 'LegalConcept',
    'Legal Scope': 'LegalConcept',
    'Exception': 'LegalConcept',
    'Infringement': 'LegalConcept',
    'Offence': 'LegalConcept',
    'LegalIssue': 'LegalConcept',
    'Violation': 'LegalConcept',
    'LegalDomain': 'LegalConcept',
    'Power': 'LegalConcept',
    'Legal Role': 'LegalRole',
    'LegalViolation': 'LegalConcept',
    'LegalPower': 'LegalConcept',
    
    #legal document
    'Document': 'LegalDocument',
    'LegalDocument': 'LegalDocument',
    'Legal Document': 'LegalDocument',
    'Publication': 'Publication',
    'Report': 'LegalDocument',
    'PublicationSeries': 'LegalDocument',
    'PublicationReference': 'LegalDocument',
    'RegulatoryList': 'LegalDocument',
    'Regulatory_List': 'LegalDocument',
    'List': 'LegalDocument',
    'URL': 'LegalDocument',
    
    #organization - bodies, agencies, companies
    #original llm graph builder used is american and gneerated using american, so i had to stick with the american spelling
    'Organization': 'Organization',
    'Company': 'Company',
    'GovernmentBody': 'GovernmentBody',
    'Government Body': 'GovernmentBody',
    'GovernmentAgency': 'GovernmentBody',
    'Government': 'GovernmentBody',
    'Authority': 'GovernmentBody',
    'Government_Authority': 'GovernmentBody',
    'Agency': 'GovernmentBody',
    'Court': 'GovernmentBody',
    'Committee': 'Organization',
    'PublicEntity': 'Organization',
    'OrganizationType': 'Organization',
    
    #person
    'Person': 'Person',
    'Group': 'Group',
    'PersonGroup': 'Group',
    'Person_Group': 'Group',
    'StakeholderGroup': 'Group',
    'Profession': 'Characteristic',
    'Stakeholder': 'Stakeholder',
    'Actor': 'Actor',
    'MarketActor': 'MarketActor',
    
    #systems, components
    'System': 'System',
    'AISystem': 'AISystem',
    'AI System': 'AISystem',
    'AI_System': 'AISystem',
    'AI System/Model': 'AISystem',
    'AIComponent': 'AIComponent',
    'ITSystem': 'ITSystem',
    'IT System': 'ITSystem',
    'SystemComponent': 'SystemComponent',
    
    #technical
    'AIModel': 'AIModel',
    'AI Model': 'AIModel',
    'AI_System_Category': 'AIModel',
    'Model': 'Model',
    'Algorithm': 'Algorithm',
    'Technology': 'Technology',
    'Technique': 'Technology',
    'Method': 'Method',
    'Methodology': 'Method',
    'Approach': 'Method',
    
    #process, activity
    'Process': 'Process',
    'Activity': 'Activity',
    'Action': 'Activity',
    'Task': 'Activity',
    'Regulatory Activity': 'Activity',
    'RegulatoryAction': 'Activity',
    'Procedure': 'Procedure',
    'Assessment': 'Procedure',
    'Investigation': 'Procedure',
    'Practice': 'Process',
    'Treatment': 'Process',
    'Measure': 'Process',
    'EnforcementMeasure': 'Process',
    'Work': 'Process',
    'Initiative': 'Process',
    'Request': 'Process',
    'Complaint': 'Process',
    'Mechanism': 'Process',
    'Movement': 'Process',
    
    #data
    'Data': 'Data',
    'Information': 'Data',
    'Database': 'Database',
    'Dataset': 'Database',
    'Repository': 'Database',
    'Archive': 'Database',
    'DataCollection': 'Database',
    'Data Source': 'Data',
    'ConfidentialInformation': 'Data',
    
    #product
    'Product': 'Product',
    'Service': 'Service',
    'Platform': 'Product',
    'Component': 'Product',
    'Application': 'Product',
    'Device': 'Product',
    'Tool': 'Product',
    'Vehicle': 'Product',
    'Product Component': 'Product',
    'Instrument': 'Product',
    'Material': 'Product',
    'Object': 'Product',
    'Asset': 'Product',
    'Channel': 'Product',
    'Distribution Channel': 'Product',
    'Website': 'Product',
    'Artifact': 'Product',
    'Resource': 'Product',
    'Output': 'Product',
    'Deliverable': 'Product',
    'Digital_Service': 'Product',
    'Solution': 'Product',
    
    #requirement - obligations, standards, constraints
    'Requirement': 'Requirement',
    'Obligation': 'Obligation',
    'Standard': 'Standard',
    'Certification': 'Standard',
    'Constraint': 'Constraint',
    'Condition': 'Constraint',
    'Specification': 'Requirement',
    'Safeguard': 'Requirement',
    'Rule': 'Requirement',
    'Responsibility': 'Requirement',
    'Penalty': 'Requirement',
    'SecurityMeasure': 'Requirement',
    
    #legal terms below
    'Right': 'Right',
    'FundamentalRight': 'FundamentalRight',

    'Interest': 'Interest',
    'ProtectedInterest': 'ProtectedInterest',
    'PublicInterest': 'PublicInterest',

    'Consent': 'Consent',
    'Access': 'Access',
    
    #risk
    'Risk': 'Risk',
    'Harm': 'Harm',
    'HarmType': 'HarmType',
    'Threat': 'Threat',
    'Hazard': 'Hazard',
    'Attack': 'Attack',
    'RiskArea': 'RiskArea',
    'RiskCategory': 'RiskCategory',
    'RiskLevel': 'RiskLevel',
    'Risk Level': 'RiskLevel',
    'RiskClassification': 'RiskClassification',
    'Vulnerability': 'Vulnerability',
    
    #characteristic
    'Characteristic': 'Characteristic',
    'Attribute': 'Characteristic',
    'PersonalAttribute': 'Characteristic',
    'Capability': 'Characteristic',
    'Skill': 'Characteristic',
    'ModelAttribute': 'Characteristic',
    'Feature': 'Characteristic',
    'BiometricIdentifier': 'Characteristic',
    'VoiceCharacteristic': 'Characteristic',
    'Property': 'Characteristic',
    'Competency': 'Characteristic',
    'Emotion': 'Characteristic',
    'Identifier': 'Characteristic',
    'Language': 'Characteristic',
    'Metric': 'Characteristic',
    'Gesture': 'Characteristic',
    'ExpressionType': 'Characteristic',
    'PhysicalState': 'Characteristic',
    'Expression': 'Characteristic',
    'FacialExpression': 'Characteristic',
    'MedicalCondition': 'Characteristic',
    'Status': 'Characteristic',
    'Functionality': 'Characteristic',
    'Parameter': 'Characteristic',
    'Factor': 'Characteristic',
    'Indicator': 'Characteristic',
    'Experience': 'Characteristic',
    'Role': 'Role',
    'LegalRole': 'LegalRole',
    
    #concept - more abstract
    'Concept': 'Concept',
    'Policy': 'Policy',
    'Principle': 'Principle',
    'Objective': 'Objective',
    'Goal': 'Objective',
    'Sector': 'Sector',
    'Industry': 'Sector',
    'Guidance': 'Guidance',
    'Guideline': 'Guidance',
    'Domain': 'Concept',
    'Purpose': 'Concept',
    'Topic': 'Concept',
    'Field': 'Concept',
    'Context': 'Concept',
    'Category': 'Concept',
    'Value': 'Concept',
    'Scope': 'Concept',
    'Classification': 'Concept',
    'Area': 'Concept',
    'Content': 'Concept',
    'ContentType': 'Concept',
    'Content_Type': 'Concept',
    'UseCase': 'Concept',
    'Use Case': 'Concept',
    'Agreement': 'Concept',
    'Program': 'Concept',
    'Benefit': 'Concept',
    'Framework': 'Concept',
    'Effect': 'Concept',
    'Impact': 'Concept',
    'Market': 'Concept',
    'Knowledge': 'Concept',
    'PolicyArea': 'Concept',
    'SocialIssue': 'Concept',
    'AdministrativeLevel': 'Concept',
    'SecurityDomain': 'Concept',
    'Consideration': 'Concept',
    'Ecosystem': 'Concept',
    'Funding': 'Concept',
    'Cost': 'Concept',
    'Society': 'Concept',
    'Example': 'Concept',
    'Strategy': 'Concept',
    'Governance': 'Concept',
    'Relationship': 'Concept',
    
    #location
    'Location': 'Location',
    'Place': 'Location',
    'Country': 'Country',
    'Region': 'Region',
    'Space': 'Location',
    'Facility': 'Location',
    'Environment': 'Location',
    'Infrastructure': 'Infrastructure',
    'Jurisdiction': 'Jurisdiction',
    
    #event
    'Event': 'Event',
    'Decision': 'Decision',
    'LegalDecision': 'Decision',
    'Incident': 'Incident',
    'Issue': 'Incident',
    'Proceeding': 'Event',
    'Phase': 'Event',
    'Situation': 'Event',
    'Outcome': 'Event',
    'Award': 'Event',
    'Transaction': 'Event',
    'Alert': 'Event',
    'Lifecycle': 'Lifecycle',
    'Development': 'Development',
    'TimePeriod': 'Event',
}

#labels to ignore completely
#these are either system labels (__Entity__) or singleton labels with <2 edges
#singletons with few connections are likely llm extraction noise, not meaningful types
IGNORE_LABELS = {
    '__Entity__',
    'Commitment', 'WorkingCondition', 'Disease', 'Media', 'GovernanceMechanism',
    'Behavior', 'Interaction', 'BusinessCase', 'BusinessConcept', 'Claim', 'Form',
    'Concern', 'Need', 'Format', 'Communication', 'Mission', 'Expertise',
    'Barrier', 'Regulatory_Condition', 'Structure',
}


#PREDICATE MAPPING
#format: [NEO4J PREDICATE: (rdf Property, parent property, flippable direction?)]
#maps neo4j relationships to rdf properties
PREDICATE_MAPPING = {
    #enactment
    'ENACTED_BY': ('enactedBy', 'enactmentRelation', False),
    'ENACTED': ('enactedBy', 'enactmentRelation', False),
    'ISSUED_BY': ('issuedBy', 'enactmentRelation', False),
    'ISSUED': ('issuedBy', 'enactmentRelation', False),
    'ADOPTED_BY': ('adoptedBy', 'enactmentRelation', False),
    'ADOPTS': ('adoptedBy', 'enactmentRelation', False),
    'PUBLISHED_IN': ('publishedIn', 'enactmentRelation', False),
    'PUBLISHES': ('publishedIn', 'enactmentRelation', False),
    
    #modification
    'AMENDS': ('amends', 'modificationRelation', False),
    'AMENDED_BY': ('amendedBy', 'modificationRelation', True),  #flip: B amendedBy A -> A amends B
    'REPEALS': ('repeals', 'modificationRelation', False),
    'REPEALED_BY': ('repealedBy', 'modificationRelation', True),
    
    #regulatory
    'REGULATES': ('regulates', 'regulatoryRelation', False),
    'GOVERNS': ('regulates', 'regulatoryRelation', False),  #maps to same property
    'GOVERNED_BY': ('regulatedBy', 'regulatoryRelation', True),  #flip direction
    'PROHIBITS': ('prohibits', 'regulatoryRelation', False),
    'RESTRICTS': ('restricts', 'regulatoryRelation', False),
    'ALLOWS': ('allows', 'regulatoryRelation', False),
    'LEGISLATES': ('regulates', 'regulatoryRelation', False),
    
    #application
    'APPLIES_TO': ('appliesTo', 'applicationRelation', False),
    'APPLIED_TO': ('appliesTo', 'applicationRelation', False),
    'APPLIED_IN': ('appliedIn', 'applicationRelation', False),
    'APPLIES_IN': ('appliedIn', 'applicationRelation', False),
    
    #requirement
    'REQUIRES': ('requires', 'requirementRelation', False),
    'SUBJECT_TO': ('subjectTo', 'requirementRelation', False),
    'MUST_COMPLY_WITH': ('mustComplyWith', 'requirementRelation', False),
    'COMPLIES_WITH': ('compliesWith', 'requirementRelation', False),
    'HAS_OBLIGATION': ('hasObligation', 'requirementRelation', False),
    'HAS_REQUIREMENT': ('hasRequirement', 'requirementRelation', False),
    'SHOULD_BE_PROHIBITED': ('prohibits', 'regulatoryRelation', False),
    
    #structural
    'INCLUDES': ('includes', 'structuralRelation', False),
    'INCLUDE': ('includes', 'structuralRelation', False),
    'COMPRISES': ('comprises', 'structuralRelation', False),
    'CONTAINS': ('includes', 'structuralRelation', False),
    'HAS_CHARACTERISTIC': ('hasCharacteristic', 'structuralRelation', False),
    'HAS_PURPOSE': ('hasPurpose', 'structuralRelation', False),
    'HAS_OBJECTIVE': ('hasObjective', 'structuralRelation', False),
    'HAS_RISK': ('hasRisk', 'structuralRelation', False),
    'HAS_RIGHT': ('hasRight', 'structuralRelation', False),
    'HAS_IDENTIFIER': ('hasIdentifier', 'structuralRelation', False),
    'INTEGRATED_INTO': ('integratedInto', 'structuralRelation', False),
    
    #usage
    'USES': ('uses', 'usageRelation', False),
    'USED_FOR': ('usedFor', 'usageRelation', False),
    'USED_IN': ('usedIn', 'usageRelation', False),
    'USED_BY': ('usedBy', 'usageRelation', False),
    'INTENDED_FOR': ('intendedFor', 'usageRelation', False),
    
    #provision
    'PROVIDES': ('provides', 'provisionRelation', False),
    'PROVIDE': ('provides', 'provisionRelation', False),
    'PROVIDED_BY': ('providedBy', 'provisionRelation', True),
    'ENSURES': ('ensures', 'provisionRelation', False),
    'ENSURE': ('ensures', 'provisionRelation', False),
    'ENABLES': ('enables', 'provisionRelation', False),
    'ENABLE': ('enables', 'provisionRelation', False),
    
    #support
    'SUPPORTS': ('supports', 'supportRelation', False),
    'FACILITATES': ('facilitates', 'supportRelation', False),
    'PROMOTES': ('promotes', 'supportRelation', False),
    'CONTRIBUTES_TO': ('contributesTo', 'supportRelation', False),
    
    #effect
    'AFFECTS': ('affects', 'effectRelation', False),
    'AFFECTED_BY': ('affectedBy', 'effectRelation', True),
    'HAS_IMPACT_ON': ('affects', 'effectRelation', False),
    'LEADS_TO': ('leadsTo', 'effectRelation', False),
    'MAY_LEAD_TO': ('leadsTo', 'effectRelation', False),  #flattened
    'CAUSES': ('causes', 'effectRelation', False),
    
    #protection
    'PROTECTS': ('protects', 'protectionRelation', False),
    'ENSURES_PROTECTION_OF': ('protects', 'protectionRelation', False),
    'THREATENS': ('threatens', 'protectionRelation', False),
    'POSES_RISK_TO': ('threatens', 'protectionRelation', False),
    
    #association - generic
    'RELATED_TO': ('relatedTo', 'associationRelation', False),
    'RELATES_TO': ('relatedTo', 'associationRelation', False),
    'RELEVANT_TO': ('relatedTo', 'associationRelation', False),
    'ASSOCIATED_WITH': ('associatedWith', 'associationRelation', False),
    'ABOUT': ('about', 'associationRelation', False),
    'CONCERNS': ('about', 'associationRelation', False),
    'REGARDING': ('about', 'associationRelation', False),
    
    #reference
    'DEFINED_IN': ('definedIn', 'referenceRelation', False),
    'LISTED_IN': ('listedIn', 'referenceRelation', False),
    'MENTIONED_IN': ('mentionedIn', 'referenceRelation', False),
    'SET_OUT_IN': ('setOutIn', 'referenceRelation', False),
    'ENSHRINED_IN': ('definedIn', 'referenceRelation', False),
    
    #classification
    'IS_A': ('isA', 'classificationRelation', False),
    'CAN_BE': ('classifiedAs', 'classificationRelation', False),
    'CLASSIFIED_AS': ('classifiedAs', 'classificationRelation', False),
    'BELONGS_TO': ('belongsTo', 'classificationRelation', False),
    'APPRECIABLY_RESEMBLES': ('resembles', 'classificationRelation', False),
    
    #establishment
    'ESTABLISHES': ('establishes', 'establishmentRelation', False),
    'ESTABLISHED_BY': ('establishedBy', 'establishmentRelation', True),
    'ESTABLISHED_IN': ('establishedIn', 'establishmentRelation', False),
    'DESIGNATES': ('designates', 'establishmentRelation', False),
    
    #action
    'PERFORMS': ('performs', 'actionRelation', False),
    'CARRIES_OUT': ('carriesOut', 'actionRelation', False),
    'CARRY_OUT': ('carriesOut', 'actionRelation', False),
    'IMPLEMENTS': ('implements', 'actionRelation', False),
    'DEVELOPS': ('develops', 'actionRelation', False),
    
    #cooperation
    'COOPERATES_WITH': ('cooperatesWith', 'cooperationRelation', False),
    'CONSULTS': ('consults', 'cooperationRelation', False),
    'REPORTS_TO': ('reportsTo', 'cooperationRelation', False),
    
    #targeting
    'TARGETS': ('targets', 'targetingRelation', False),
    'AIMS_TO': ('aimsTo', 'targetingRelation', False),
    'FOR': ('for', 'targetingRelation', False),
    
    #involvement
    'INVOLVES': ('involves', 'involvementRelation', False),
    'PARTICIPATES_IN': ('participatesIn', 'involvementRelation', False),
    
    #derivation
    'BASED_ON': ('basedOn', 'derivationRelation', False),
    'DERIVED_FROM': ('derivedFrom', 'derivationRelation', False),
    'PURSUANT_TO': ('pursuantTo', 'derivationRelation', False),
    'IN_ACCORDANCE_WITH': ('inAccordanceWith', 'derivationRelation', False),
    'WITHOUT_PREJUDICE_TO': ('withoutPrejudiceTo', 'derivationRelation', False),
    
    #scope
    'COVERS': ('covers', 'scopeRelation', False),
    'EXCLUDES': ('excludes', 'scopeRelation', False),
    'PLACED_ON': ('placedOn', 'scopeRelation', False),
    
    #consideration
    'CONSIDERS': ('considers', 'considerationRelation', False),
    'TAKES_INTO_ACCOUNT': ('takesIntoAccount', 'considerationRelation', False),
    'RECOGNIZES': ('recognizes', 'considerationRelation', False),
    
    #assessment
    'IDENTIFIES': ('identifies', 'assessmentRelation', False),
    
    #assignment
    'CHARGED_WITH_TASKS_IN': ('chargedWith', 'assignmentRelation', False),
}

#VERB STEM MAPPING
#automatic mapping of any predicates not in PREDICATE_MAPPING
#extracts first word of predicate and looks up here to find closest match
#achieves 81.8% coverage of all relationships automatically, but only ever used as a fallback
VERB_STEM_MAPPING = {
    'ENACTED': ('enactedBy', 'enactmentRelation'),
    'ISSUED': ('issuedBy', 'enactmentRelation'),
    'ADOPTED': ('adoptedBy', 'enactmentRelation'),
    'PUBLISHED': ('publishedIn', 'enactmentRelation'),
    'AMENDS': ('amends', 'modificationRelation'),
    'AMENDED': ('amendedBy', 'modificationRelation'),
    'REPEALS': ('repeals', 'modificationRelation'),
    'REGULATES': ('regulates', 'regulatoryRelation'),
    'GOVERNS': ('regulates', 'regulatoryRelation'),
    'GOVERNED': ('regulatedBy', 'regulatoryRelation'),
    'PROHIBITS': ('prohibits', 'regulatoryRelation'),
    'RESTRICTS': ('restricts', 'regulatoryRelation'),
    'ALLOWS': ('allows', 'regulatoryRelation'),
    'APPLIES': ('appliesTo', 'applicationRelation'),
    'APPLIED': ('appliesTo', 'applicationRelation'),
    'REQUIRES': ('requires', 'requirementRelation'),
    'SUBJECT': ('subjectTo', 'requirementRelation'),
    'MUST': ('requires', 'requirementRelation'),
    'SHOULD': ('requires', 'requirementRelation'),
    'MAY': ('allows', 'regulatoryRelation'),
    'CAN': ('allows', 'regulatoryRelation'),
    'INCLUDES': ('includes', 'structuralRelation'),
    'COMPRISES': ('comprises', 'structuralRelation'),
    'CONTAINS': ('includes', 'structuralRelation'),
    'HAS': ('has', 'structuralRelation'),
    'USES': ('uses', 'usageRelation'),
    'USED': ('usedFor', 'usageRelation'),
    'INTENDED': ('intendedFor', 'usageRelation'),
    'PROVIDES': ('provides', 'provisionRelation'),
    'PROVIDED': ('providedBy', 'provisionRelation'),
    'ENSURES': ('ensures', 'provisionRelation'),
    'ENABLES': ('enables', 'provisionRelation'),
    'SUPPORTS': ('supports', 'supportRelation'),
    'FACILITATES': ('facilitates', 'supportRelation'),
    'PROMOTES': ('promotes', 'supportRelation'),
    'CONTRIBUTES': ('contributesTo', 'supportRelation'),
    'AFFECTS': ('affects', 'effectRelation'),
    'AFFECTED': ('affectedBy', 'effectRelation'),
    'IMPACTS': ('affects', 'effectRelation'),
    'LEADS': ('leadsTo', 'effectRelation'),
    'CAUSES': ('causes', 'effectRelation'),
    'PROTECTS': ('protects', 'protectionRelation'),
    'THREATENS': ('threatens', 'protectionRelation'),
    'RELATED': ('relatedTo', 'associationRelation'),
    'RELATES': ('relatedTo', 'associationRelation'),
    'ASSOCIATED': ('associatedWith', 'associationRelation'),
    'ABOUT': ('about', 'associationRelation'),
    'CONCERNS': ('about', 'associationRelation'),
    'DEFINED': ('definedIn', 'referenceRelation'),
    'LISTED': ('listedIn', 'referenceRelation'),
    'MENTIONED': ('mentionedIn', 'referenceRelation'),
    'ESTABLISHES': ('establishes', 'establishmentRelation'),
    'ESTABLISHED': ('establishedBy', 'establishmentRelation'),
    'CREATES': ('establishes', 'establishmentRelation'),
    'PERFORMS': ('performs', 'actionRelation'),
    'CARRIES': ('carriesOut', 'actionRelation'),
    'IMPLEMENTS': ('implements', 'actionRelation'),
    'DEVELOPS': ('develops', 'actionRelation'),
    'COOPERATES': ('cooperatesWith', 'cooperationRelation'),
    'CONSULTS': ('consults', 'cooperationRelation'),
    'REPORTS': ('reportsTo', 'cooperationRelation'),
    'TARGETS': ('targets', 'targetingRelation'),
    'AIMS': ('aimsTo', 'targetingRelation'),
    'INVOLVES': ('involves', 'involvementRelation'),
    'PARTICIPATES': ('participatesIn', 'involvementRelation'),
    'BASED': ('basedOn', 'derivationRelation'),
    'DERIVED': ('derivedFrom', 'derivationRelation'),
    'COVERS': ('covers', 'scopeRelation'),
    'EXCLUDES': ('excludes', 'scopeRelation'),
    'CONSIDERS': ('considers', 'considerationRelation'),
    'RECOGNIZES': ('recognizes', 'considerationRelation'),
    'IDENTIFIES': ('identifies', 'assessmentRelation'),
    'ASSESSES': ('assesses', 'assessmentRelation'),
    'MONITORS': ('monitors', 'assessmentRelation'),
}

#extra logic needed to retrieve predicate mapping for relationships
#every unique label was mapped, but there are ~1800 unique relationship types that cannot all indiviudlaly be mapped
#therefore we need a way to handle all of those relationships that were NOT explicitly mapped
#relationships also can be invertible (passive), therefore extra information needs to be returned when relationship mapping is retrieved

#so we chain 4 strategies to make sure every single relationship is processed properly
#1 try explicit mapping listed above
#2 see if verb stem of first word is listed in verb stem mapping. if yes use that
#3 see if verb stem of second word is listed in verb stem mapping. if yes use that
#4 IF ALL ELSE FAILS: create a NEW unique relation under the otherRelation leaf hierarchy
def get_predicate_mapping(neo4j_predicate):
    #OPTION 1 BASIC RETRIEVAL
    #basic rdf mapping retrieval for neo4j predicate (SAME AS BASIC LABEL MAPPING LOOKUP)
    
    #check explicit mapping first
    if neo4j_predicate in PREDICATE_MAPPING:
        return PREDICATE_MAPPING[neo4j_predicate]
    
    #try verb stem of first word
    #e.g should_be_allowed -> should
    #is 'should' in the verb stem mapping above? if yes use that
    stem = neo4j_predicate.split('_')[0]
    if stem in VERB_STEM_MAPPING:
        prop, parent = VERB_STEM_MAPPING[stem]
        return (prop, parent, False)
    
    #try second word if first didn't match
    #e.g is_regulated_by -> regulated
    parts = neo4j_predicate.split('_')
    if len(parts) > 1 and parts[1] in VERB_STEM_MAPPING:
        prop, parent = VERB_STEM_MAPPING[parts[1]]
        return (prop, parent, False)
    
    #fallback: normalise label and declare under otherRelation
    #e.g. some_random_relationship -> someRandomRelationship
    camel = ''.join(word.capitalize() for word in neo4j_predicate.split('_'))
    camel = camel[0].lower() + camel[1:] if camel else neo4j_predicate.lower()
    return (camel, 'otherRelation', False)




