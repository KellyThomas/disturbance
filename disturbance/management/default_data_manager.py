import logging

from disturbance.components.main.models import ApplicationType
from disturbance.components.proposals.models import ApiarySiteFeeType, SiteCategory

logger = logging.getLogger(__name__)


class DefaultDataManager(object):

    def __init__(self):
        # Store default ApiarySiteFeeType data
        for item in ApiarySiteFeeType.FEE_TYPE_CHOICES:
            obj, created = ApiarySiteFeeType.objects.get_or_create(name=item[0])
            if created:
                logger.info("Created apiary site fee type: %s" % obj)

        # Store default
        for item in SiteCategory.CATEGORY_CHOICES:
            obj, created = SiteCategory.objects.get_or_create(name=item[0])
            if created:
                logger.info("Created apiary site category: %s" % obj)

        for type_name in ApplicationType.APPLICATION_TYPES:
            q_set = ApplicationType.objects.filter(name=type_name[0])
            if not q_set:
                visibility = True if type_name[0] in (
                        ApplicationType.DISTURBANCE, 
                        ApplicationType.APIARY, 
                        ApplicationType.POWERLINE_MAINTENANCE
                        ) else False
                obj = ApplicationType.objects.create(
                        name=type_name[0],
                        application_fee=0,
                        oracle_code_application='',
                        visible=visibility,
                        )
                logger.info("Created application type: %s" % obj)

