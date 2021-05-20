# stdlib
import sys

# third party
from google.protobuf.reflection import GeneratedProtocolMessageType
from sympy.core.expr import Expr

# syft relative
from .... import deserialize
from .... import serialize
from ....generate_wrapper import GenerateWrapper
from ....proto.lib.sympy.expression_pb2 import Expression as Expression_PB
from ...util import full_name_with_name

# this is a subclass for Expression with .children: [Expression]
def generate_children_type(real_type: Expr) -> None:
    def object2proto(obj: real_type) -> Expression_PB:
        print("serializing an obj", obj, type(obj))
        a = [serialize(child) for child in obj.children]
        return Expression_PB(
            obj_type=full_name_with_name(klass=type(obj)),
            children=[serialize(child) for child in obj.children],
        )

    def proto2object(proto: Expression_PB) -> real_type:
        module_parts = proto.obj_type.split(".")
        klass = module_parts.pop()
        obj_type = getattr(sys.modules[".".join(module_parts)], klass)
        return obj_type(
            children=tuple([deserialize(child) for child in proto.children])
        )

    GenerateWrapper(
        wrapped_type=real_type,
        import_path=full_name_with_name(klass=real_type),
        protobuf_scheme=Expression_PB,
        type_object2proto=object2proto,
        type_proto2object=proto2object,
    )
