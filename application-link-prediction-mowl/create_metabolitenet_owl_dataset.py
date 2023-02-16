import click as ck
from pathlib import Path
import mowl
mowl.init_jvm('2g')

from mowl.owlapi import OWLAPIAdapter
from mowl.owlapi.adapter import IRI
import java

@ck.command()
@ck.option('--data-root', '-dr', default=Path('../knowledge-graph/'), type=Path,
            help='Data folder with the ABox (knowledge graph)')
def main(data_root):
    annotations_file = data_root / 'edges_v2023-02-10.csv'
    owlapi = OWLAPIAdapter()
    ABox = owlapi.owl_manager.createOntology()

    with open(annotations_file) as f:
        for line in f:
            if line[0] == ':':
                continue
            it = line.strip().split(',')
            #print(it)
            id1 = it[0].split(':')
            id1_iri = f'http://mowl.borg/{id1[0]}_{id1[1]}'
            #print(it[2])
            id2 = it[2].split(':')
            id2_iri = f'http://mowl.borg/{id2[0]}_{id2[1]}'
            #print(id2_iri)
            id1_cls = owlapi.create_class(id1_iri)
            id2_cls = owlapi.create_class(id2_iri)
            related_to = owlapi.create_object_property(
                'http://purl.obolibrary.org/obo/RO_0002616')
            related_to_some_id2 = owlapi.create_object_some_values_from(
                related_to, id2_cls)
            axiom = owlapi.create_subclass_of(
                id1_cls, related_to_some_id2)
            owlapi.owl_manager.addAxiom(ABox, axiom)

    print('id1: ', id1_iri)
    print('id2: ',  id2_iri)
    out_file = java.io.File(str(data_root / 'metabolitenet_dataset.owl'))
    owlapi.owl_manager.saveOntology(ABox,
    IRI.create(f'file://{out_file.getAbsolutePath()}'))

if __name__ == '__main__':
    main()
