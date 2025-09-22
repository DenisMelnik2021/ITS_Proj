from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils.dateparse import parse_datetime
from .serializers import YoloIncidentReportSerializer
from .models import Incident
from django.utils import timezone
import logging


# Create your views here.

logger = logging.getLogger(__name__)
class IncidentViewSet(viewsets.GenericViewSet):
    queryset = Incident.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='report')
    def report(self, request):
        ser = YoloIncidentReportSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        obj = ser.save()

        raw_ts = ser.validated_data.get('ts') or request.data.get('ts')
        if raw_ts:
            dt = parse_datetime(raw_ts)
            if dt:
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone.utc)
                obj.created_at = dt
                obj.save(update_fields=['created_at'])
            else:
                logger.warning(
                    "YOLO ts parse failed; keeping created_at auto. incident_id=%s ts=%r",
                    obj.id,
                    raw_ts
                )

        payload = {
            "id": obj.id,
            "created_at": obj.created_at.isoformat(),
            "status": obj.status,
        }

        return Response(payload, status=status.HTTP_201_CREATED)

