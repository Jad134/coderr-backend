from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = '__all__'
        read_only_fields = ['offer']  # Verhindert, dass das `offer`-Feld direkt überschrieben wird


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)  # Nested serializer for related OfferDetail objects

    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']  # Read-only fields

    def create(self, validated_data):
        # Extract details data
        details_data = validated_data.pop('details', [])
        # Create the Offer instance
        offer = Offer.objects.create(**validated_data)
        # Create associated OfferDetail instances
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        # Extract details data
        details_data = validated_data.pop('details', None)

        # Update main Offer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            # Update details intelligently
            existing_details = {detail.id: detail for detail in instance.details.all()}
            for detail_data in details_data:
                detail_id = detail_data.get('id')
                if detail_id and detail_id in existing_details:
                    # Update existing detail
                    detail_instance = existing_details.pop(detail_id)
                    for attr, value in detail_data.items():
                        setattr(detail_instance, attr, value)
                    detail_instance.save()
                else:
                    # Create new detail
                    OfferDetail.objects.create(offer=instance, **detail_data)

            # Delete any remaining old details not included in the update
            for detail in existing_details.values():
                detail.delete()

        return instance