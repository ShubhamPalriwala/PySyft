# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/lib/python/int.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1aproto/lib/python/int.proto\x12\x0fsyft.lib.python"\x13\n\x03Int\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x03\x62\x06proto3'
)


_INT = DESCRIPTOR.message_types_by_name["Int"]
Int = _reflection.GeneratedProtocolMessageType(
    "Int",
    (_message.Message,),
    {
        "DESCRIPTOR": _INT,
        "__module__": "proto.lib.python.int_pb2"
        # @@protoc_insertion_point(class_scope:syft.lib.python.Int)
    },
)
_sym_db.RegisterMessage(Int)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _INT._serialized_start = 47
    _INT._serialized_end = 66
# @@protoc_insertion_point(module_scope)
