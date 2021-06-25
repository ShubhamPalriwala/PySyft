# stdlib
import os
from threading import Thread
from time import sleep
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

# third party
from flask import current_app as app
import jwt
from nacl.signing import SigningKey
from nacl.signing import VerifyKey

from syft import serialize
from syft.core.common.message import SignedImmediateSyftMessageWithReply
from syft.core.common.message import SignedImmediateSyftMessageWithoutReply
from syft.core.io.location import Location
from syft.core.io.location import SpecificLocation
from syft.core.node.common.action.exception_action import ExceptionMessage
from syft.core.node.common.action.exception_action import UnknownPrivateException
from syft.core.node.common.service.auth import AuthorizationException
from syft.core.node.common.service.child_node_lifecycle_service import (
    ChildNodeLifecycleService,
)
from syft.core.node.common.service.get_repr_service import GetReprService
from syft.core.node.common.service.heritage_update_service import HeritageUpdateService
from syft.core.node.common.service.obj_action_service import (
    ImmediateObjectActionServiceWithReply,
)
from syft.core.node.common.service.obj_action_service import (
    ImmediateObjectActionServiceWithoutReply,
)
from syft.core.node.common.service.obj_search_permission_service import (
    ImmediateObjectSearchPermissionUpdateService,
)
from syft.core.node.common.service.obj_search_service import (
    ImmediateObjectSearchService,
)
from syft.core.node.common.service.repr_service import ReprService
from syft.core.node.common.service.resolve_pointer_type_service import (
    ResolvePointerTypeService,
)

from syft.core.node.domain.domain import Domain

# grid relative
from .database import db
from .database.store_disk import DiskObjectStore
from .manager.association_request_manager import AssociationRequestManager
from .manager.environment_manager import EnvironmentManager
from .manager.group_manager import GroupManager
from .manager.request_manager import RequestManager
from .manager.role_manager import RoleManager
from .manager.setup_manager import SetupManager
from .manager.user_manager import UserManager
from .services.association_request import AssociationRequestService
from .services.dataset_service import DatasetManagerService
from .services.group_service import GroupManagerService
from .services.model_service import ModelManagerService

# commenting because these services require Jupyter conflict deps
# from ..services.infra_service import DomainInfrastructureService
from .services.request_service import RequestService
from .services.request_service import RequestServiceWithoutReply
from .services.role_service import RoleManagerService
from .services.setup_service import SetUpService
from .services.tensor_service import RegisterTensorService
from .services.transfer_service import TransferObjectService
from .services.user_service import UserManagerService


class GridDomain(Domain):
    def __init__(
        self,
        name: Optional[str],
        network: Optional[Location] = None,
        domain: SpecificLocation = SpecificLocation(),
        device: Optional[Location] = None,
        vm: Optional[Location] = None,
        signing_key: Optional[SigningKey] = None,
        verify_key: Optional[VerifyKey] = None,
        root_key: Optional[VerifyKey] = None,
        db_path: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            network=network,
            domain=domain,
            device=device,
            vm=vm,
            signing_key=signing_key,
            verify_key=verify_key,
            db_path=db_path,
        )

        # Database Management Instances
        self.users = UserManager(db)
        self.roles = RoleManager(db)
        self.groups = GroupManager(db)
        self.disk_store = DiskObjectStore(db)
        self.environments = EnvironmentManager(db)
        self.setup = SetupManager(db)
        self.association_requests = AssociationRequestManager(db)
        self.data_requests = RequestManager(db)

        self.env_clients = {}
        self.setup_configs = {}

        # Reset Node Services
        self.immediate_msg_with_reply_router = {}
        self.immediate_msg_without_reply_router = {}
        self.immediate_services_with_reply: List[Any] = []
        self.immediate_services_without_reply: List[Any] = []

        # Common Node Services
        self.immediate_services_with_reply.append(ImmediateObjectActionServiceWithReply)
        self.immediate_services_with_reply.append(ImmediateObjectSearchService)
        self.immediate_services_with_reply.append(GetReprService)
        self.immediate_services_with_reply.append(ResolvePointerTypeService)

        self.immediate_services_without_reply.append(ReprService)
        self.immediate_services_without_reply.append(HeritageUpdateService)
        self.immediate_services_without_reply.append(ChildNodeLifecycleService)
        self.immediate_services_without_reply.append(
            ImmediateObjectActionServiceWithoutReply
        )
        self.immediate_services_without_reply.append(
            ImmediateObjectSearchPermissionUpdateService
        )

        # Grid Domain Services
        self.immediate_services_with_reply.append(AssociationRequestService)
        self.immediate_services_with_reply.append(SetUpService)
        self.immediate_services_with_reply.append(RegisterTensorService)
        self.immediate_services_with_reply.append(RoleManagerService)
        self.immediate_services_with_reply.append(UserManagerService)
        self.immediate_services_with_reply.append(DatasetManagerService)
        self.immediate_services_with_reply.append(GroupManagerService)
        self.immediate_services_with_reply.append(TransferObjectService)
        self.immediate_services_with_reply.append(RequestService)
        self.immediate_services_with_reply.append(ModelManagerService)

        self.immediate_services_without_reply.append(RequestServiceWithoutReply)
        self._register_services()

    def login(self, email: str, password: str) -> Dict:
        user = self.users.login(email=email, password=password)
        token = jwt.encode({"id": user.id}, app.config["SECRET_KEY"])
        token = token.decode("UTF-8")
        return {
            "token": token,
            "key": user.private_key,
            "metadata": serialize(self.get_metadata_for_client())
            .SerializeToString()
            .decode("ISO-8859-1"),
        }

    def recv_immediate_msg_with_reply(
        self, msg: SignedImmediateSyftMessageWithReply, raise_exception=False
    ) -> SignedImmediateSyftMessageWithoutReply:
        if raise_exception:
            response = self.process_message(
                msg=msg, router=self.immediate_msg_with_reply_router
            )
            # maybe I shouldn't have created process_message because it screws up
            # all the type inference.
            res_msg = response.sign(signing_key=self.signing_key)  # type: ignore
        else:
            # exceptions can be easily triggered which break any WebRTC loops
            # so we need to catch them here and respond with a special exception
            # message reply
            try:
                # try to process message
                response = self.process_message(
                    msg=msg, router=self.immediate_msg_with_reply_router
                )

            except Exception as e:
                public_exception: Exception
                if isinstance(e, AuthorizationException):
                    private_log_msg = "An AuthorizationException has been triggered"
                    public_exception = e
                else:
                    private_log_msg = f"An {type(e)} has been triggered"  # dont send
                    public_exception = UnknownPrivateException(
                        "UnknownPrivateException has been triggered."
                    )
                try:
                    # try printing a useful message
                    private_log_msg += f" by {type(msg.message)} "
                    private_log_msg += f"from {msg.message.reply_to}"  # type: ignore
                except Exception:
                    pass

                if app.debug:
                    print(private_log_msg)
                    print(e)

                # send the public exception back
                response = ExceptionMessage(
                    address=msg.message.reply_to,  # type: ignore
                    msg_id_causing_exception=msg.message.id,
                    exception_type=type(public_exception),
                    exception_msg=str(public_exception),
                )

            # maybe I shouldn't have created process_message because it screws up
            # all the type inference.
            res_msg = response.sign(signing_key=self.signing_key)  # type: ignore
            output = (
                f"> {self.pprint} Signing {res_msg.pprint} with "
                + f"{self.key_emoji(key=self.signing_key.verify_key)}"  # type: ignore
            )
        return res_msg
