# Copyright (C) 2012 Eduardo Robles Elvira <edulix AT wadobo DOT com>
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

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from agora_site.agora_core.models import Agora

import random

class Command(BaseCommand):
    args = '<n>'
    help = 'Clears the database, except for the admin user'

    def handle(self, *args, **options):
        for i in User.objects.filter(is_superuser=False):
            i.delete()
	for a in Agora.objects.all():
            a.delete()
