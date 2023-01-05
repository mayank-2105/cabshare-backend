from rest_framework import routers
# from rest_framework_extensions import routers

router = routers.DefaultRouter()

import sharinglogic.views as sharinglogic_views

router.register(r'cabshare/sharinglogic', sharinglogic_views.SharingUserViewSet, basename='SharingLogic')