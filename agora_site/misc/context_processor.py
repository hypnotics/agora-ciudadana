# -*- coding: utf-8 -*-
# Copyright (C) 2010 Daniel García Moreno <dani AT danigm DOT net>
# Copyright (C) 2010 Eduardo Robles Elvira <edulix AT gmail DOT com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from agora_site.agora_core.models import Agora

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import get_language
import json

import sys

def base(request):
    '''
    This is a context processor that adds some vars to the base template
    '''
    return {
        'session': request.session,
        'can_create_agoras': Agora.static_has_perms('create', request.user),
        'languages': json.dumps(
            dict(
                current=get_language(),
                objects=[dict(lang_code=lang_code, name=name.decode()) for lang_code, name in settings.LANGUAGES]
            )
        ),
    }

class SettingsProcessor(object):
    def __getattr__(self, attr):
        if attr == '__file__':
            # autoreload support in dev server
            return __file__
        else:
            return lambda request: {attr: getattr(settings, attr)}

sys.modules[__name__ + '.settings'] = SettingsProcessor()
