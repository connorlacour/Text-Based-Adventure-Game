import json
import os

from marshmallow import Schema, fields, post_load, pre_load, post_dump
from marshmallow.fields import Int, Str, Nested, Bool
from data_objects import *
from marshmallow_oneofschema import OneOfSchema


def load_items_from_file(filename: str) -> List[Item]:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f'templates/{filename}')
    with open(filename) as file:
        j = json.load(file)

    return ItemSchema().load(j, many=True)


def load_rooms_from_file(filename: str) -> List[Room]:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f'templates/{filename}')
    with open(filename) as file:
        j = json.load(file)

    return RoomSchema().load(j, many=True)

class InventoryItemSchema(Schema):
    item_type = "Inventory"
    name = Str()
    display_name = Str()
    article = Str()
    description = Str()
    can_take = Bool()

    class Meta:
        ordered = True

    @post_load
    def make_item(self, data, **kwargs):
        return InventoryItem(**data)


class SceneryItemSchema(Schema):
    item_type = "Scenery"
    name = Str()
    display_name = Str()
    article = Str()
    description = Str()

    class Meta:
        ordered = True

    @post_load
    def make_item(self, data, **kwargs):
        return SceneryItem(**data)


class CollectiveItemSchema(Schema):
    item_type = "Scenery"
    name = Str()
    display_name = Str()
    article = Str()
    description = Str()
    singular_display_name = Str()
    singular_description = Str()
    max_count = Int()

    class Meta:
        ordered = True

    @post_load
    def make_item(self, data, **kwargs):
        return CollectiveItem(**data)


class ItemSchema(OneOfSchema):

    type_schemas = {
        "Inventory": InventoryItemSchema,
        "Scenery": SceneryItemSchema,
        "Collective": CollectiveItemSchema
    }

    def get_obj_type(self, obj):
        if isinstance(obj, SceneryItem):
            return "Scenery"
        elif isinstance(obj, InventoryItem):
            return "Inventory"
        elif isinstance(obj, CollectiveItem):
            return "Collective"
        else:
            raise Exception(f"Unknown object type {obj.__class__.__name__}")

    class Meta:
        ordered = True

class RoomConnectorSchema(Schema):

    SKIP_VALUES = {None}

    direction = Str()
    room_name = Str()
    connector_item_name = Str(required=False)
    narrative_text = Str()
    known_to_player = Bool()
    article = Str()

    @post_load
    def make_item(self, data, **kwargs):
        return RoomConnector(**data)

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUES
        }

class RoomSchema(Schema):
    name = Str()
    display_name = Str()
    article = Str()
    long_description = Str()
    short_description = Str()
    item_setup_dict = fields.Dict(keys=Str(), values=Str())
    room_list = fields.List(fields.Nested(RoomConnectorSchema))

    @post_load
    def make_room(self, data, **kwargs):
        return Room(**data)
