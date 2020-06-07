from django.conf import settings

from disturbance.components.organisations.serializers import OrganisationSerializer
from disturbance.components.proposals.serializers_base import (
        BaseProposalSerializer, 
        #ProposalReferralSerializer,
        ProposalDeclinedDetailsSerializer,
        EmailUserSerializer,
        )
from disturbance.components.proposals.models import (
    Proposal,
    ProposalApiary,
    ProposalApiaryTemporaryUse,
    ProposalApiarySiteTransfer,

    ApiaryApplicantChecklistQuestion,
    ApiaryApplicantChecklistAnswer,

    ProposalApiaryDocument,
    ApiarySite,

    OnSiteInformation,
    ApiaryReferralGroup,
    TemporaryUseApiarySite,
    ApiaryReferral,
    Referral, ApiarySiteApproval,
)

from rest_framework import serializers
from ledger.accounts.models import Address



class ApplicantAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id',
            'line1',
            'line2',
            'line3',
            'locality',
            'state',
            'country',
            'postcode'
        ) 

class OnSiteInformationSerializer(serializers.ModelSerializer):
    apiary_site_id = serializers.IntegerField(write_only=True, required=False)
    # apiary_site = ApiarySiteSerializer(read_only=True)
    datetime_deleted = serializers.DateTimeField(write_only=True, required=False)

    class Meta:
        model = OnSiteInformation
        fields = (
            'id',
            # 'apiary_site',
            'apiary_site_id',
            'period_from',
            'period_to',
            'comments',
            'datetime_deleted',
        )

    def validate(self, data):
        field_errors = {}
        non_field_errors = []

        if not self.partial:
            if not data['period_from']:
                field_errors['Period from'] = ['Please select a date.',]
            if not data['period_to']:
                field_errors['Period to'] = ['Please select a date.',]
            if not data['apiary_site_id'] and not data['apiary_site_id'] > 0:
                field_errors['Site'] = ['Please select a site',]
            if not data['comments']:
                field_errors['comments'] = ['Please enter comments.',]

            # Raise errors
            if field_errors:
                raise serializers.ValidationError(field_errors)

            if data['period_from'] > data['period_to']:
                non_field_errors.append('Period "from" date must be before "to" date.')

            # Raise errors
            if non_field_errors:
                raise serializers.ValidationError(non_field_errors)
        else:
            # Partial udpate, which means the dict data doesn't have all the field
            pass


        return data


class ApiarySiteSerializer(serializers.ModelSerializer):
    proposal_apiary_id = serializers.IntegerField(write_only=True,)
    site_category_id = serializers.IntegerField(write_only=True,)
    onsiteinformation_set = OnSiteInformationSerializer(read_only=True, many=True,)

    class Meta:
        model = ApiarySite
        fields = (
            'id',
            'available',
            # 'temporary_used',
            'site_guid',
            'proposal_apiary_id',
            'site_category_id',
            'onsiteinformation_set',
        )


class ProposalApiarySerializer(serializers.ModelSerializer):
    apiary_sites = ApiarySiteSerializer(read_only=True, many=True)
    on_site_information_list = serializers.SerializerMethodField()  # This is used for displaying OnSite table at the frontend

    #checklist_questions = serializers.SerializerMethodField()
    checklist_answers = serializers.SerializerMethodField()

    class Meta:
        model = ProposalApiary
        # geo_field = 'location'

        fields = (
            'id',
            'title',
            'proposal',
            # 'location',
            'apiary_sites',
            'longitude',
            'latitude',
            'on_site_information_list',
            #'checklist_questions',
            'checklist_answers',
        )

    def get_on_site_information_list(self, obj):
        on_site_information_list = OnSiteInformation.objects.filter(
            apiary_site__in=ApiarySite.objects.filter(proposal_apiary=obj),
            datetime_deleted=None,
        ).order_by('-period_from')
        ret = OnSiteInformationSerializer(on_site_information_list, many=True).data
        return ret

    #def get_checklist_questions(self, obj):
     #   checklistQuestion = ApiaryApplicantChecklistQuestion.objects.values('text')
      #  ret = ApiaryApplicantChecklistQuestionSerializer(checklistQuestion, many=True).data
       # return ret

    def get_checklist_answers(self, obj):
        return ApiaryApplicantChecklistAnswerSerializer(obj.apiary_applicant_checklist, many=True).data


class SaveProposalApiarySerializer(serializers.ModelSerializer):
    proposal_id = serializers.IntegerField(
            required=True, write_only=True, allow_null=False)

    class Meta:
        model = ProposalApiary
        # geo_field = 'location'

        fields = (
            'id',
            'title',
            'proposal_id',
            # 'location',
            #'apiary_sites',
            'longitude',
            'latitude',
            #'on_site_information_list',
            #'checklist_questions',
        )
        read_only_fields = (
                'id',
                )


class ApiarySiteApprovalSerializer(serializers.ModelSerializer):
    apiary_site_id = serializers.IntegerField(write_only=True, required=False)
    apiary_site = ApiarySiteSerializer(read_only=True)

    class Meta:
        model = ApiarySiteApproval
        fields = (
            'apiary_site_id',
            'apiary_site',
            # 'approval',
        )


class TemporaryUseApiarySiteSerializer(serializers.ModelSerializer):
    proposal_apiary_temporary_use_id = serializers.IntegerField(write_only=True, required=False)
    # apiary_site_id = serializers.IntegerField(write_only=True, required=False)
    # apiary_site = ApiarySiteSerializer(read_only=True)
    apiary_site_approval = ApiarySiteApprovalSerializer(read_only=True)
    apiary_site_approval_id = serializers.IntegerField(write_only=True, required=False)
    # apiary_site = serializers.SerializerMethodField()

    def validate(self, attrs):
        return attrs

    def get_apiary_site(self, obj):
        serializers = ApiarySiteSerializer(self.apiary_site_approval.apiary_site)
        return serializers.data

    class Meta:
        model = TemporaryUseApiarySite
        fields = (
            'proposal_apiary_temporary_use_id',
            'apiary_site_approval',
            'apiary_site_approval_id',
            # 'apiary_site_id',
            # 'apiary_site',
        )


class ProposalApiaryTemporaryUseSerializer(serializers.ModelSerializer):
    proposal_id = serializers.IntegerField(write_only=True, required=False)
    # proposal_apiary_base_id = serializers.IntegerField(write_only=True, required=False)
    apiary_sites = TemporaryUseApiarySiteSerializer(many=True, read_only=True)

    class Meta:
        model = ProposalApiaryTemporaryUse
        fields = (
            'id',
            'from_date',
            'to_date',
            'temporary_occupier_name',
            'temporary_occupier_phone',
            'temporary_occupier_mobile',
            'temporary_occupier_email',
            'proposal_id',
            # 'proposal_apiary_base_id',
            'apiary_sites',
        )


class ProposalApiarySiteTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalApiarySiteTransfer
        fields = '__all__'


class ProposalApiaryDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalApiaryDocument
        fields = ('id', 'name', '_file')


class SaveProposalApiarySiteLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalApiary
        fields = ('id', 'title', 'proposal')


class ProposalApiaryTypeSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    documents_url = serializers.SerializerMethodField()
    proposal_type = serializers.SerializerMethodField()
    get_history = serializers.ReadOnlyField()
    fee_invoice_url = serializers.SerializerMethodField()

    submitter = serializers.CharField(source='submitter.get_full_name')
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)

    application_type = serializers.CharField(source='application_type.name', read_only=True)
    proposal_apiary = ProposalApiarySerializer()
    apiary_temporary_use = ProposalApiaryTemporaryUseSerializer()
    apiary_site_transfer = ProposalApiarySiteTransferSerializer()

    class Meta:
        model = Proposal
        fields = (
                'id',
                'application_type',
                'proposal_type',
                'title',
                'customer_status',
                'processing_status',
                'review_status',
                #'applicant_type',
                'applicant',
                #'org_applicant',
                #'proxy_applicant',
                'submitter',
                'assigned_officer',
                'previous_application',
                'get_history',
                'lodgement_date',
                'modified_date',
                'documents',
                'requirements',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'documents_url',
                'reference',
                'lodgement_number',
                'lodgement_sequence',
                'can_officer_process',
                'proposal_type',
                #'pending_amendment_request',
                #'is_amendment_proposal',

                #'applicant_details',
                #'training_completed',
                'fee_invoice_url',
                'fee_invoice_reference',
                'fee_paid',
                'activity',
                'proposal_apiary',
                'apiary_temporary_use',
                'apiary_site_transfer',

                )
        read_only_fields=('documents',)

    def get_documents_url(self,obj):
        return '/media/{}/proposals/{}/documents/'.format(settings.MEDIA_APP_DIR, obj.id)

    def get_readonly(self,obj):
        return False

    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_review_status(self,obj):
        return obj.get_review_status_display()

    def get_customer_status(self,obj):
        return obj.get_customer_status_display()

    def get_proposal_type(self,obj):
        return obj.get_proposal_type_display()

    def get_fee_invoice_url(self,obj):
        return '/payments/invoice-pdf/{}'.format(obj.fee_invoice_reference) if obj.fee_paid else None


class ApiaryReferralGroupSerializer(serializers.ModelSerializer):
    all_members_list = serializers.SerializerMethodField()
    class Meta:
        model = ApiaryReferralGroup
        fields = (
                'id',
                'name',
                'all_members_list',
                )

    def get_all_members_list(self, obj):
        serializer = EmailUserSerializer(obj.all_members, many=True)
        return serializer.data


class ApiaryProposalReferralSerializer(serializers.ModelSerializer):
    referral = serializers.CharField(source='referral.get_full_name')
    processing_status = serializers.CharField(source='get_processing_status_display')
    apiary_referral = serializers.SerializerMethodField()
    class Meta:
        model = Referral
        fields = '__all__'

    def get_apiary_referral(self, obj):
        return ApiaryReferralSerializer(obj.apiary_referral).data


class ApiaryInternalProposalSerializer(BaseProposalSerializer):
    # TODO next 3 commented lines - related to 'apply as an Org or as an individual'
    #applicant = ApplicantSerializer()
    #applicant = serializers.CharField(read_only=True)
    #org_applicant = OrganisationSerializer()
    #applicant = OrganisationSerializer() # for apply as Org only
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)
    #submitter = EmailUserAppViewSerializer()
    submitter = serializers.CharField(source='submitter.get_full_name')
    proposaldeclineddetails = ProposalDeclinedDetailsSerializer()
    assessor_mode = serializers.SerializerMethodField()
    current_assessor = serializers.SerializerMethodField()
    assessor_data = serializers.SerializerMethodField()
    latest_referrals = ApiaryProposalReferralSerializer(many=True)
    allowed_assessors = EmailUserSerializer(many=True)
    approval_level_document = serializers.SerializerMethodField()
    application_type = serializers.CharField(source='application_type.name', read_only=True)
    #region = serializers.CharField(source='region.name', read_only=True)
    #district = serializers.CharField(source='district.name', read_only=True)
    #assessor_assessment=ProposalAssessmentSerializer(read_only=True)
    #referral_assessments=ProposalAssessmentSerializer(read_only=True, many=True)
    fee_invoice_url = serializers.SerializerMethodField()
    applicant = serializers.SerializerMethodField()
    applicant_type = serializers.SerializerMethodField()
    applicant_address = serializers.SerializerMethodField()

    proposal_apiary = ProposalApiarySerializer()
    apiary_temporary_use = ProposalApiaryTemporaryUseSerializer()
    apiary_site_transfer = ProposalApiarySiteTransferSerializer()

    class Meta:
        model = Proposal
        fields = (
                'id',
                'application_type',
                'activity',
                'approval_level',
                'approval_level_document',
                #'region',
                #'district',
                'title',
                'data',
                'schema',
                'customer_status',
                'processing_status',
                'review_status',
                #applicant',
                #'org_applicant',
                #'proxy_applicant',
                'submitter',
                #'applicant_type',
                'assigned_officer',
                'assigned_approver',
                'previous_application',
                'get_history',
                'lodgement_date',
                'modified_date',
                'documents',
                'requirements',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'documents_url',
                'assessor_mode',
                'current_assessor',
                'assessor_data',
                'comment_data',
                'latest_referrals',
                'allowed_assessors',
                'proposed_issuance_approval',
                'proposed_decline_status',
                'proposaldeclineddetails',
                'permit',
                'reference',
                'lodgement_number',
                'lodgement_sequence',
                'can_officer_process',
                'proposal_type',
                # tab field models
                #'applicant_details',
                #'assessor_assessment',
                #'referral_assessments',
                'fee_invoice_reference',
                'fee_invoice_url',
                'fee_paid',
                'applicant',
                'applicant_type',
                'proposal_apiary',
                'apiary_temporary_use',
                'apiary_site_transfer',
                'applicant_address',
                )
        read_only_fields=('documents','requirements')

    def get_applicant_address(self, obj):
        address_serializer = None
        if obj.relevant_applicant_address:
            address_serializer = ApplicantAddressSerializer(obj.relevant_applicant_address)
            return address_serializer.data
        return address_serializer

    def get_approval_level_document(self,obj):
        if obj.approval_level_document is not None:
            return [obj.approval_level_document.name,obj.approval_level_document._file.url]
        else:
            return obj.approval_level_document

    def get_assessor_mode(self,obj):
        # TODO check if the proposal has been accepted or declined
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        return {
            'assessor_mode': True,
            'has_assessor_mode': obj.has_assessor_mode(user),
            'assessor_can_assess': obj.can_assess(user),
            'assessor_level': 'assessor',
            'assessor_box_view': obj.assessor_comments_view(user)
        }

    def get_can_edit_activities(self,obj):
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        return obj.can_edit_activities(user)

    def get_readonly(self,obj):
        return True

    def get_current_assessor(self,obj):
        return {
            'id': self.context['request'].user.id,
            'name': self.context['request'].user.get_full_name(),
            'email': self.context['request'].user.email
        }

    def get_assessor_data(self,obj):
        return obj.assessor_data

    def get_reversion_ids(self,obj):
        return obj.reversion_ids[:5]

    def get_fee_invoice_url(self,obj):
        return '/payments/invoice-pdf/{}'.format(obj.fee_invoice_reference) if obj.fee_paid else None

    def get_applicant(self,obj):
        serializer = None
        if obj.relevant_applicant_type == 'organisation':
            serializer = OrganisationSerializer(obj.relevant_applicant)
        else:
            serializer = EmailUserSerializer(obj.relevant_applicant)
        return serializer.data

    def get_applicant_type(self,obj):
        return obj.relevant_applicant_type


class ApiaryReferralSerializer(serializers.ModelSerializer):
    #processing_status = serializers.CharField(source='get_processing_status_display')
    #latest_referrals = ProposalReferralSerializer(many=True)
    #can_be_completed = serializers.BooleanField()
    referral_group = ApiaryReferralGroupSerializer()
    class Meta:
        model = ApiaryReferral
        fields = (
                'id',
                'referral_group',
                )

    #def __init__(self,*args,**kwargs):
     #   super(ReferralSerializer, self).__init__(*args, **kwargs)
      #  self.fields['proposal'] = ReferralProposalSerializer(context={'request':self.context['request']})


class FullApiaryReferralSerializer(serializers.ModelSerializer):
    processing_status = serializers.CharField(source='get_processing_status_display')
    latest_referrals = ApiaryProposalReferralSerializer(many=True)
    can_be_completed = serializers.BooleanField()
    apiary_referral = ApiaryReferralSerializer()
    class Meta:
        model = Referral
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(FullApiaryReferralSerializer, self).__init__(*args, **kwargs)
        self.fields['proposal'] = ApiaryReferralProposalSerializer(context={'request':self.context['request']})


class ApiaryReferralProposalSerializer(ApiaryInternalProposalSerializer):
    def get_assessor_mode(self,obj):
        # TODO check if the proposal has been accepted or declined
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        try:
            referral = Referral.objects.get(proposal=obj,referral=user)
        except:
            referral = None
        return {
            'assessor_mode': True,
            'assessor_can_assess': referral.can_assess_referral(user) if referral else None,
            'assessor_level': 'referral',
            'assessor_box_view': obj.assessor_comments_view(user)
        }

class ApiaryApplicantChecklistQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiaryApplicantChecklistQuestion
        fields=('id',
                'text',
                'answer_type',
                'order'
                )

class ApiaryApplicantChecklistAnswerSerializer(serializers.ModelSerializer):
    question = ApiaryApplicantChecklistQuestionSerializer()

    class Meta:
        model = ApiaryApplicantChecklistAnswer
        fields=('id',
                'question',
                'answer',
                'proposal_id',
                )


class SendApiaryReferralSerializer(serializers.Serializer):
    #email = serializers.EmailField()
    group_id = serializers.IntegerField()
    text = serializers.CharField(allow_blank=True)


class DTApiaryReferralSerializer(serializers.ModelSerializer):
    processing_status = serializers.CharField(source='proposal.get_processing_status_display')
    referral_status = serializers.CharField(source='get_processing_status_display')
    proposal_lodgement_date = serializers.CharField(source='proposal.lodgement_date')
    proposal_lodgement_number = serializers.CharField(source='proposal.lodgement_number')
    submitter = serializers.SerializerMethodField()
    region = serializers.CharField(source='region.name', read_only=True)
    #referral = EmailUserSerializer()
    apiary_referral = ApiaryReferralSerializer()
    class Meta:
        model = Referral
        fields = (
            'id',
            'region',
            'activity',
            'title',
            'applicant',
            'submitter',
            'processing_status',
            'referral_status',
            'lodged_on',
            'proposal',
            'can_be_processed',
            'referral',
            'proposal_lodgement_date',
            'proposal_lodgement_number',
            'referral_text',
            'apiary_referral',
        )

    def get_submitter(self,obj):
        return EmailUserSerializer(obj.proposal.submitter).data

