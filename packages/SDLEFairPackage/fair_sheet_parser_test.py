import pytest
import csv
from rdflib import Namespace
from fair_sheet_parser import FairSheetParser
from rdflib import Graph as rdfGraph
import graphviz

# Define sample data for testing
ontology_info_data = [
    ["Ontology Name", "TestOntology"],
    ["Ontology URI", "http://example.com/ontology#"],
    ["Ontology Version", "1.0"],
    ["Ontology Author(s)", "John Doe, Jane Smith"],
    ["Ontology Description", "A test ontology"]
]

namespace_data = [
    {"Prefix Name": "test", "Ontology URL": "http://example.com/test#", "Ontology Info": "" },
    {"Prefix Name": "owl", "Ontology URL": "http://www.w3.org/2002/07/owl#", "Ontology Info": "" },
    {"Prefix Name": "PMDCo", "Ontology URL": "https://w3id.org/pmd/co/", "Ontology Info": "" }
]

@pytest.fixture
def create_test_files(tmp_path):
    # Create temporary test files
    ontology_info_path = tmp_path / "TestOntologyInfo.csv"
    namespace_path = tmp_path / "TestNameSpace.csv"
    entity_path = tmp_path / "TestVariableDefinitions.csv"
    data_property_path = tmp_path / "TestValueTypeDefinitions.csv"
    obj_property_path = tmp_path / "TestRelationshipDefinitions.csv"


    # Write test data to CSV files
    with open(ontology_info_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(ontology_info_data[0])
        writer.writerow(ontology_info_data[1])
        writer.writerow(ontology_info_data[2])
        writer.writerow(ontology_info_data[3])
        writer.writerow(ontology_info_data[4])
    
    with open(namespace_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Prefix Name", "Ontology URL", "Ontology Info"])
        writer.writeheader()
        writer.writerows(namespace_data)

    with open(entity_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Variable Name", "Belongs to Ontology", "Parent Variable", "Definition of Variable", "Alternative Name(s)", "Unit", "Logical Axioms", "fullName"])
        writer.writeheader()
        writer.writerow({
            "Variable Name": "",
            "Belongs to Ontology": "",
            "Parent Variable": "",
            "Definition of Variable": "",
            "Alternative Name(s)": "",
            "Unit": "",
            "Logical Axioms": "",
            "fullName": ""
        })
        writer.writerow({
            "Variable Name": "Identifier",
            "Belongs to Ontology": "PMDCo",
            "Parent Variable": "",
            "Definition of Variable": "",
            "Alternative Name(s)": "",
            "Unit": "",
            "Logical Axioms": "",
            "fullName": "PMDCo:Identifier"
        })
        
    with open(obj_property_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Relationship Name", "Belongs to Ontology", "Domain", "Range", "Definition", "Logical Axioms", "Alternative Name(s)", "fullName"])
        writer.writeheader()
        writer.writerow({
            "Relationship Name": "",
            "Belongs to Ontology": "",
            "Domain": "",
            "Range": "",
            "Definition": "",
            "Logical Axioms": "",
            "Alternative Name(s)": ""
        })
        writer.writerow({
            "Relationship Name": "",
            "Belongs to Ontology": "",
            "Domain": "",
            "Range": "",
            "Definition": "",
            "Logical Axioms": "",
            "Alternative Name(s)": ""
        })

    with open(data_property_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ValueType Name", "Belongs to Ontology", "Domain", "Range", "Definition of Property", "Logical Axioms", "Alternative Name(s)", "fullName"])
        writer.writeheader()
        writer.writerow({
            "ValueType Name": "",
            "Belongs to Ontology": "",
            "Domain": "",
            "Range": "",
            "Definition of Property": "",
            "Logical Axioms": "",
            "Alternative Name(s)": "",
        })
        writer.writerow({
            "ValueType Name": "",
            "Belongs to Ontology": "",
            "Domain": "",
            "Range": "",
            "Definition of Property": "",
            "Logical Axioms": "",
            "Alternative Name(s)": ""
        })


    return tmp_path

 
def test_init(create_test_files):
    # Arrange
    ontology_sheet_folder = create_test_files
    include_valuetype_graphviz_edges = False
    rdflib_graph = rdfGraph()
    graphviz_graph = graphviz.Digraph(strict=False)

    # Act
    parser = FairSheetParser(ontology_sheet_folder, include_valuetype_graphviz_edges, rdflib_graph, graphviz_graph)

    # Assert
    assert parser.__ontology_name == "TestOntology"
    assert parser.__ontology_base_uri == Namespace("http://example.com/ontology#")
    assert parser.__ontology_version == "1.0"
    assert parser.__namespace_uris == {
        "test": Namespace("http://example.com/test#"),
        "owl": Namespace("http://www.w3.org/2002/07/owl#"),
        "TestOntology": Namespace("http://example.com/ontology#")
    }
