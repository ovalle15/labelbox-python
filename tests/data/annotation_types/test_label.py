import numpy as np

from labelbox import OntologyBuilder, Tool, Classification as OClassification, Option
from labelbox.data.annotation_types import (ClassificationAnswer, Radio, Text,
                                            ClassificationAnnotation,
                                            ObjectAnnotation, Point, Line,
                                            ImageData, Label)


def test_schema_assignment_geometry():
    name = "line_feature"
    label = Label(
        data=ImageData(arr=np.ones((32, 32, 3), dtype=np.uint8)),
        annotations=[
            ObjectAnnotation(
                value=Line(
                    points=[Point(x=1, y=2), Point(x=2, y=2)]),
                name=name,
            )
        ])
    feature_schema_id = "expected_id"
    ontology = OntologyBuilder(tools=[
        Tool(Tool.Type.LINE, name=name, feature_schema_id=feature_schema_id)
    ])
    label.assign_feature_schema_ids(ontology)

    assert label.annotations[0].feature_schema_id == feature_schema_id


def test_schema_assignment_classification():
    radio_name = "radio_name"
    text_name = "text_name"
    option_name = "my_option"

    label = Label(data=ImageData(arr=np.ones((32, 32, 3), dtype=np.uint8)),
                  annotations=[
                      ClassificationAnnotation(value=Radio(
                          answer=ClassificationAnswer(name=option_name)),
                                               name=radio_name),
                      ClassificationAnnotation(value=Text(answer="some text"),
                                               name=text_name)
                  ])
    radio_schema_id = "radio_schema_id"
    text_schema_id = "text_schema_id"
    option_schema_id = "option_schema_id"
    ontology = OntologyBuilder(
        tools=[],
        classifications=[
            OClassification(class_type=OClassification.Type.RADIO,
                            instructions=radio_name,
                            feature_schema_id=radio_schema_id,
                            options=[
                                Option(value=option_name,
                                       feature_schema_id=option_schema_id)
                            ]),
            OClassification(
                class_type=OClassification.Type.TEXT,
                instructions=text_name,
                feature_schema_id=text_schema_id,
            )
        ])
    label.assign_feature_schema_ids(ontology)
    assert label.annotations[0].feature_schema_id == radio_schema_id
    assert label.annotations[1].feature_schema_id == text_schema_id
    assert label.annotations[
        0].value.answer.feature_schema_id == option_schema_id


def test_schema_assignment_subclass():
    name = "line_feature"
    radio_name = "radio_name"
    option_name = "my_option"
    classification = ClassificationAnnotation(
        name=radio_name,
        value=Radio(answer=ClassificationAnswer(name=option_name)),
    )
    label = Label(
        data=ImageData(arr=np.ones((32, 32, 3), dtype=np.uint8)),
        annotations=[
            ObjectAnnotation(value=Line(
                points=[Point(x=1, y=2), Point(x=2, y=2)]),
                             name=name,
                             classifications=[classification])
        ])
    feature_schema_id = "expected_id"
    classification_schema_id = "classification_id"
    option_schema_id = "option_schema_id"
    ontology = OntologyBuilder(tools=[
        Tool(Tool.Type.LINE,
             name=name,
             feature_schema_id=feature_schema_id,
             classifications=[
                 OClassification(class_type=OClassification.Type.RADIO,
                                 instructions=radio_name,
                                 feature_schema_id=classification_schema_id,
                                 options=[
                                     Option(value=option_name,
                                            feature_schema_id=option_schema_id)
                                 ])
             ])
    ])
    label.assign_feature_schema_ids(ontology)
    assert label.annotations[0].feature_schema_id == feature_schema_id
    assert label.annotations[0].classifications[
        0].feature_schema_id == classification_schema_id
    assert label.annotations[0].classifications[
        0].value.answer.feature_schema_id == option_schema_id


def test_highly_nested():
    name = "line_feature"
    radio_name = "radio_name"
    nested_name = "nested_name"
    option_name = "my_option"
    nested_option_name = "nested_option_name"
    classification = ClassificationAnnotation(
        name=radio_name,
        value=Radio(answer=ClassificationAnswer(name=option_name)),
        classifications=[
            ClassificationAnnotation(value=Radio(answer=ClassificationAnswer(
                name=nested_option_name)),
                                     name=nested_name)
        ])
    label = Label(
        data=ImageData(arr=np.ones((32, 32, 3), dtype=np.uint8)),
        annotations=[
            ObjectAnnotation(value=Line(
                points=[Point(x=1, y=2), Point(x=2, y=2)]),
                             name=name,
                             classifications=[classification])
        ])
    feature_schema_id = "expected_id"
    classification_schema_id = "classification_id"
    nested_classification_schema_id = "nested_classification_schema_id"
    option_schema_id = "option_schema_id"
    ontology = OntologyBuilder(tools=[
        Tool(Tool.Type.LINE,
             name=name,
             feature_schema_id=feature_schema_id,
             classifications=[
                 OClassification(
                     class_type=OClassification.Type.RADIO,
                     instructions=radio_name,
                     feature_schema_id=classification_schema_id,
                     options=[
                         Option(value=option_name,
                                feature_schema_id=option_schema_id,
                                options=[
                                    OClassification(
                                        class_type=OClassification.Type.RADIO,
                                        instructions=nested_name,
                                        feature_schema_id=
                                        nested_classification_schema_id,
                                        options=[
                                            Option(
                                                value=nested_option_name,
                                                feature_schema_id=
                                                nested_classification_schema_id)
                                        ])
                                ])
                     ])
             ])
    ])
    label.assign_feature_schema_ids(ontology)
    assert label.annotations[0].feature_schema_id == feature_schema_id
    assert label.annotations[0].classifications[
        0].feature_schema_id == classification_schema_id
    assert label.annotations[0].classifications[
        0].value.answer.feature_schema_id == option_schema_id
