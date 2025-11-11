from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'service-centers', ServiceCenterViewSet, basename='servicecenter')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'cars', CarViewSet, basename='car')
router.register(r'parts', PartViewSet, basename='part')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'repairs', RepairViewSet, basename='repair')
router.register(r'repair-details', RepairDetailViewSet, basename='repairdetail')

urlpatterns = router.urls
