from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.template.defaultfilters import slugify
from list.models import *


class ImportDFI:
    import yaml
    from django.conf import settings
    def loadYML(self, file):
        return self.yaml.load(open(self.settings.BASE_DIR + '/list/' + file))
    def importcommunes(self):
        changes_commune = False
        if not Region.objects.filter(name = 'valais').exists():
            valais = Region(name = 'valais')
            valais.save()
            changes_commune = True
        valais = Region.objects.get(name = 'valais')
        base = self.loadYML('communes.yml')
        for commune in base:
            if not Region_child.objects.filter(name = commune['district'].lower()).exists():
                child = Region_child(name = commune['district'].lower(), region=valais)
                child.save()
                print('district '+child.name+' sauve')
                changes_commune = True
            child = Region_child.objects.get(name = commune['district'].lower())
            if not Region_child2.objects.filter(name = commune['commune']).exists():
                commune = Region_child2(name = commune['commune'].lower(), order = commune['order'], region_child = child)
                commune.save()
                print('commune '+commune.name+' sauvee')
                changes_commune = True
        return changes_commune
