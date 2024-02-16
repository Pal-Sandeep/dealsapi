from decimal import Decimal

from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.response import Response

from deals.models import Deal, DealProject, Project
from .serializers import DealProjectAddSerializer, DealSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """View for creating, reading, updating, and deleting a deal"""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']


class DealViewSet(viewsets.ModelViewSet):
    """View for creating, reading, and deleting a deal"""

    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract project data from request
        projects_data = None
        if 'projects' in request.data:
            projects_data = request.data.pop('projects')

        with transaction.atomic():
            # Create deal instance
            deal = serializer.save()

            # Create DealProject relations with tax credit rates
            if projects_data:
                for project_data in projects_data:
                    project_id = project_data['project']
                    tax_credit_rate = project_data['tax_credit_transfer_rate']
                    project = get_object_or_404(Project, pk=project_id)
                    DealProject.objects.create(
                        deal=deal, project=project, tax_credit_transfer_rate=Decimal(tax_credit_rate))
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"error": "No Projects data provided"})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        project_pk = request.data.get('project_pk')
        if project_pk:
            project = get_object_or_404(Project, pk=project_pk)
            DealProject.objects.filter(project=project).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return super().destroy(request, *args, **kwargs)


class DealProjectAddCreateAPIView(CreateAPIView):
    """View for adding a project to an existing deal"""

    queryset = Deal.objects.all()
    serializer_class = DealProjectAddSerializer

    def get_object(self):
        deal_id = self.kwargs.get('pk')
        deal = get_object_or_404(Deal, pk=deal_id)
        return deal

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['deal'] = self.get_object()
        return context
