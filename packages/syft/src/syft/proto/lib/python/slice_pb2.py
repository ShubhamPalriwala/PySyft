# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/lib/python/slice.proto
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
    b'\n\x1cproto/lib/python/slice.proto\x12\x0fsyft.lib.python"i\n\x05Slice\x12\r\n\x05start\x18\x01 \x01(\x03\x12\x0c\n\x04stop\x18\x02 \x01(\x03\x12\x0c\n\x04step\x18\x03 \x01(\x03\x12\x11\n\thas_start\x18\x04 \x01(\x08\x12\x10\n\x08has_stop\x18\x05 \x01(\x08\x12\x10\n\x08has_step\x18\x06 \x01(\x08\x62\x06proto3'
)


_SLICE = DESCRIPTOR.message_types_by_name["Slice"]
Slice = _reflection.GeneratedProtocolMessageType(
    "Slice",
    (_message.Message,),
    {
        "DESCRIPTOR": _SLICE,
        "__module__": "proto.lib.python.slice_pb2"
        # @@protoc_insertion_point(class_scope:syft.lib.python.Slice)
    },
)
_sym_db.RegisterMessage(Slice)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _SLICE._serialized_start = 49
    _SLICE._serialized_end = 154
# @@protoc_insertion_point(module_scope)
