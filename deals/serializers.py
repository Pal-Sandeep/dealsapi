from rest_framework import serializers

from deals.models import Deal, DealProject, Project


class ProjectSerializer(serializers.ModelSerializer):
    """serializer for project model"""

    class Meta:
        model = Project
        fields = '__all__'


class DealProjectSerializer(serializers.ModelSerializer):
    """serializer for dealproject model"""

    project = ProjectSerializer(read_only=True, required=False)
    tax_credit_transfer_rate = serializers.DecimalField(
        max_digits=3, decimal_places=2)
    tax_credit_transfer_amount = serializers.SerializerMethodField(
        read_only=True)

    def get_tax_credit_transfer_amount(self, obj):
        return obj.get_tax_credit_amount()

    class Meta:
        model = DealProject
        fields = ['project', 'tax_credit_transfer_rate',
                  'tax_credit_transfer_amount', 'created_at']


class DealSerializer(serializers.ModelSerializer):
    """serializer for deal model"""

    projects = DealProjectSerializer(many=True, read_only=True)
    total_tax_credit_transfer_amount = serializers.SerializerMethodField(
        read_only=True)

    def get_total_tax_credit_transfer_amount(self, obj):
        dealproject = DealProject.objects.filter(deal=obj)
        return sum(dp.get_tax_credit_amount() for dp in dealproject)

    class Meta:
        model = Deal
        fields = ['id', 'name', 'created_at',
                  'projects', 'total_tax_credit_transfer_amount']


class DealProjectAddSerializer(serializers.ModelSerializer):
    """serializer for adding a project to an existing Deal"""

    class Meta:
        model = DealProject
        fields = ['project', 'tax_credit_transfer_rate', 'created_at']

    def create(self, validated_data):
        dealproject = DealProject.objects.create(
            deal=self.context['deal'],
            project=validated_data['project'],
            tax_credit_transfer_rate=validated_data['tax_credit_transfer_rate']
        )
        return dealproject
