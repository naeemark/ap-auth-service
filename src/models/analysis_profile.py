# pylint: disable=too-many-instance-attributes
"""
    Analysis Profile Model
"""
import os

from dynamorm import DynaModel
from marshmallow import fields
from src.utils.logger import log_info
from src.utils.utils import get_epoch_utc_timestamp

SLUG_ENTITY_HASH_KEY = "#AP-ANALYSIS-PROFILE#"
SLUG_ENTITY_SORT_KEY = "#ANLS-PRF#USR#{}#"


class AnalysisProfileModel(DynaModel):
    """ Provides an instance of entity AnalysisProfileModel::DynaModel """

    # for partial updates
    _validated_data = {}

    class Table:
        """  DynamoDB Table Specifications """

        name = os.environ.get("DYNAMODB_TABLE_NAME_USERS")
        hash_key = "entity_hash_key"
        range_key = "entity_sort_key"

    def __init__(self, **kwargs):
        self.entity_hash_key = SLUG_ENTITY_HASH_KEY
        self.entity_sort_key = SLUG_ENTITY_SORT_KEY.format(kwargs.get("created_by"))
        self.analysis_profile_id = kwargs.get("analysis_profile_id")
        self.zignal_profile_id = kwargs.get("zignal_profile_id", None)
        self.zignal_profile_json = kwargs.get("zignal_profile_json", None)
        self.created_by = kwargs.get("created_by")
        self.created_at = int(kwargs.get("created_at", get_epoch_utc_timestamp()))
        self.updated_at = int(kwargs.get("updated_at", get_epoch_utc_timestamp()))

    class Schema:
        """  Attributes Schema """

        entity_hash_key = fields.String(required=True)
        entity_sort_key = fields.String(required=True)
        analysis_profile_id = fields.String(required=True)
        zignal_profile_id = fields.String(required=False)
        zignal_profile_json = fields.Mapping(required=False)
        created_by = fields.String(required=True, unique=True)
        created_at = fields.Integer()
        updated_at = fields.Integer()

    def save(self):
        """  Overridden Save """
        super(AnalysisProfileModel, self).save(unique=True)

    def update(self, **kwargs):
        """  Overridden Update - Includes new value for updated_at """
        super(AnalysisProfileModel, self).update(updated_at=get_epoch_utc_timestamp(), **kwargs)

    @classmethod
    def get(cls, email=None):
        """  Overridden Get """
        return super(AnalysisProfileModel, cls).get(entity_hash_key=SLUG_ENTITY_HASH_KEY, entity_sort_key=SLUG_ENTITY_SORT_KEY.format(email))

    @classmethod
    def get_all(cls):
        """  Get All """
        return super(AnalysisProfileModel, cls).query(entity_hash_key=SLUG_ENTITY_HASH_KEY)

    def dict(self):
        """  Coverts `self` to `dict` """
        return {
            "analysisProfileId": self.analysis_profile_id,
            "zignalProfileId": self.zignal_profile_id,
            "zignalProfileJson": self.zignal_profile_json,
            "createdBy": self.created_by,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    def __repr__(self):
        """  Provides a Representation of `self` """
        return "{}: {}".format(self.__class__.__name__, self.dict())

    def log(self, log_at=None):
        """  Logs Representation """
        log_data = f"{log_at} => {self}" if log_at else self
        log_info(log_data)
