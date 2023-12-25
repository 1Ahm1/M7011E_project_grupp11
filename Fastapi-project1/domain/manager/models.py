from pydantic import BaseModel
from domain.user.models import UserProfile
from domain.utils.enums import CompanyType, OrderType, InviteStatus
from enum import Enum
from typing import List
from datetime import datetime

class Owner(BaseModel):
    user_id: int
    name: str = None
    image: str = None

class Company(BaseModel):
    id: int
    name: str = None
    image: str = None

class CompanyStats(BaseModel):
    workers: int
    active_workers: int
    parked_cars: int
    valet_points: int
    

class ManagerPermissions(BaseModel):
    company_permissions: List[str] = None
    valet_point_permissions: List[str] = None
    managed_valet_points: List[str] = None

class CompanyDetailsResponse(BaseModel):
    is_owner: bool
    owner: Owner = None
    stats: CompanyStats = None
    name: str
    type: CompanyType
    location: str = None
    image: str = None
    description: str = None

class ManagerInitData(BaseModel):
    profile: UserProfile
    company: CompanyDetailsResponse = None
    permissions: ManagerPermissions = None

class CreateCompanyRequest(BaseModel):
    name: str
    type: CompanyType
    location: str = None
    image_id: str = None
    description: str = None

class UpdateCompanyRequest(BaseModel):
    name: str = None
    type: CompanyType = None
    location: str = None
    image_id: int = None
    description: str = None

class UpdateCompanyResponse(BaseModel):
    company_id: int
    type: CompanyType
    name: str
    location: str = None
    image_id: int = None
    description: str = None

class CreateValetPointRequest(BaseModel):
    name: str
    location: str
    image_id: int
    description: str

class UpdateValetPointRequest(BaseModel):
    valet_point_id: int
    name: str
    location: str
    image_id: int
    description: str

class UpdateValetPointResponse(BaseModel):
    valet_point_id: int
    company_id: int
    name: str
    location: str
    image_id: int
    description: str

class ValetPoint(BaseModel):
    id: int
    name: str
    image: str = None
    location: str = None
    description: str = None

class ValetPointManager(BaseModel):
    id: int
    name: str = None
    image: str = None

class ValetPointStats(BaseModel):
    total_workers_count: int
    active_workers_count: int
    current_parked_cars_count: int

class ValetPointDetailsResponse(BaseModel):
    id: int
    created_by: ValetPointManager = None
    last_updated_by: ValetPointManager = None
    name: str
    location: str = None
    image: str = None
    stats: ValetPointStats = None
    description: str = None

class ValetPointOrderByColumns(Enum):
    NAME = "name"
    CREATION_TIME = "created_at"
    #ACTIVE_WORKERS_COUNT = "active_workers_count"
    #CURRENT_PARKED_CARS_COUNT = "current_parked_cars_count"

class ValetPointListRequest(BaseModel):
    page_no: int = 1
    page_size: int
    search_query: str = None
    order_by: ValetPointOrderByColumns = None
    order_type: OrderType = None

class ValetPointElementResponse(BaseModel):
    id: int
    image: str = None
    name: str = None
    created_at: datetime
    description: str = None

class ValetPointListResponse(BaseModel):
    total_pages: int
    data: List[ValetPointElementResponse]


class ManagerInviteSendRequest(BaseModel):
    qr_code: bool = False
    invited_manager_id: int = None
    permissions: ManagerPermissions

class ManagerInviteSendResponse(BaseModel):
    verification_code: int = None
    manager_invite_id: int

class ManagerInviteOrderByColumns(Enum):
    NAME = "invited_manager_name"
    

class ManagerInviteListRequest(BaseModel):
    page_no: int = 1
    page_size: int
    search_query: str = None
    order_by: ManagerInviteOrderByColumns = ManagerInviteOrderByColumns.NAME
    order_type: OrderType = OrderType.ASC

class ManagerInviteElementResponse(BaseModel):
    manager_invite_id: int
    status: InviteStatus
    manager_name: str
    invited_manager_name: str

class ManagerInviteListResponse(BaseModel):
    total_pages: int
    data: List[ManagerInviteElementResponse]

class ManagerInviteDetailsResponse(BaseModel):
    manager_invite_id: int
    status: InviteStatus = InviteStatus.PENDING
    manager_name: str
    invited_manager_name: str
    company_permissions: str = ""
    valet_point_ids: str = ""
    valet_point_permissions: str = ""

class InviteOrderByColumns(Enum):
    NAME = "name"
    CREATION_TIME = "created_at"
    

class InviteListRequest(BaseModel):
    page_no: int = 1
    page_size: int
    search_query: str = None
    order_by: InviteOrderByColumns = None
    order_type: OrderType = None

class Manager(BaseModel):
    id: int
    name: str = None
    image: str = None

class InviteElementResponse(BaseModel): 
    manager_invite_id: int
    status: InviteStatus
    created_at: datetime
    inviter_manager: Manager

class InviteListResponse(BaseModel):
    total_pages: int
    data: List[InviteElementResponse]

class InviteDetailsResponse(BaseModel):
    manager_invite_id: int
    status: InviteStatus
    inviter_manager: Manager
    company: Company
    permissions: ManagerPermissions


class WorkerInviteOrderByColumns(Enum):
    NAME = "worker_name"
    


class WorkerInviteSendRequest(BaseModel):
    invited_worker_id: int
    schedule_type:str
    schedule_description: str
    valet_point_id: int 
    schedule_details: str = ""



class WorkerInviteElementResponse(BaseModel):
    worker_invite_id: int
    status: InviteStatus
    manager_name: str
    worker_name: str



class WorkerInviteListResponse(BaseModel):
    total_pages: int
    data: List[WorkerInviteElementResponse]

class WorkerInviteListRequest(BaseModel):
    page_no: int = 1
    page_size: int
    search_query: str = None
    order_by: WorkerInviteOrderByColumns = None
    order_type: OrderType = None

class WorkerInviteDetailsResponse(BaseModel):
    worker_invite_id: int
    status: InviteStatus 
    manager_name: str
    worker_name: str
    valet_point_id: int
    schedule_id: int

class WorkerOrderByColumns(Enum):
    NAME = "name"

class WorkerElementResponse(BaseModel):
    id: int
    name: str
    image: str = None
    is_active: bool

class WorkerListResponse(BaseModel):
    total_pages: int
    data: List[WorkerElementResponse]

class WorkerListRequest(BaseModel):
    page_no: int = 1
    page_size: int
    search_query: str = None
    order_by: WorkerOrderByColumns = None
    order_type: OrderType = None

class WorkerDetailsResponse(BaseModel):
    id: int
    name: str
    image: str = None
    is_active: bool
    active_valet_point: ValetPoint = None

class ManagerOrderByColumns(Enum):
    NAME = "name"

class ManagerElementResponse(BaseModel):
    id: int
    name: str
    image: str = None
    is_active: bool
    is_company_owner:bool

class ManagerListResponse(BaseModel):
    total_pages: int
    data: List[ManagerElementResponse]


class ManagerDetailsResponse(BaseModel):
    id: int
    name: str
    image: str = None
    is_active: bool
    is_company_owner: bool
    permissions: ManagerPermissions

class ManagerListRequest(BaseModel):
    page_no: int = 1
    page_size: int
    search_query: str = None
    order_by: ManagerOrderByColumns = None
    order_type: OrderType = None

