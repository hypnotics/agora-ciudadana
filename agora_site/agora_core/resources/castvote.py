from agora_site.agora_core.models import CastVote
from agora_site.misc.generic_resource import GenericResource, GenericMeta
from agora_site.agora_core.resources.user import TinyUserResource
from agora_site.misc.utils import JSONApiField

from tastypie import fields


DELEGATION_URL = "http://example.com/delegation/has/no/url/"


class CastVoteResource(GenericResource):
    voter = fields.ForeignKey(TinyUserResource, 'voter', full=True)
    election = fields.ForeignKey('agora_site.agora_core.resources.election.ResultsElectionResource',
                                 'election')
    delegate_election_count = fields.DictField(readonly=True)
    public_data = fields.DictField(readonly=True)

    class Meta(GenericMeta):
        queryset = CastVote.objects.select_related(
                'election', 'voter', 'voter__profile', 'delegate_election_count'
            ).all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        excludes = ['data']

    def dehydrate_public_data(self, bundle):
        return bundle.obj.get_public_data()

    def dehydrate_delegate_election_count(self, bundle):
        q = bundle.obj.delegate_election_count.all()
        if len(q) == 0:
            # TODO return the previous most recent election delegate_election_count
            return None
        else:
            dec=q[0]
            from agora_site.agora_core.resources.delegateelectioncount import DelegateElectionCountResource
            decr = DelegateElectionCountResource()
            cbundle = decr.build_bundle(obj=dec, request=bundle.request)
            cbundle = decr.full_dehydrate(cbundle)
            return cbundle
