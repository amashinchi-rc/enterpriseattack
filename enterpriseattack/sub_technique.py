#---------------------------------------------------------------------------------#

import enterpriseattack
import logging

#---------------------------------------------------------------------------------#
# SubTechnique class:
#---------------------------------------------------------------------------------#

class SubTechnique:
    def __init__(self, attack_objects, relationships, id_lookup, **kwargs):
        self.relationships = relationships
        self.id_lookup = id_lookup
        self.attack_objects = attack_objects

        self.id = enterpriseattack.utils.expand_external(kwargs.get('external_references'), 'external_id')
        self.mid = kwargs.get('id')
        self.created = kwargs.get('created')
        self.modified = kwargs.get('modified')
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.description = kwargs.get('description')
        self.created_by_ref = kwargs.get('created_by_ref')
        self.object_marking_ref = kwargs.get('object_marking_refs')
        self.url = enterpriseattack.utils.expand_external(kwargs.get('external_references'), 'url')
        self.permissions_required = kwargs.get('x_mitre_permissions_required')
        self.platforms = kwargs.get('x_mitre_platforms')
        self.references = enterpriseattack.utils.obtain_sources(kwargs.get('external_references'))
        self.revoked = kwargs.get('revoked')
        self.deprecated = kwargs.get('x_mitre_deprecated')
        self.x_mitre_data_sources = kwargs.get('x_mitre_data_sources')
        self.detection = kwargs.get('x_mitre_detection')

    #---------------------------------------------------------------------------------#
    # Access Datasources for each Sub Technique object:
    #---------------------------------------------------------------------------------#

    @property
    def datasources(self):
        from .data_source import DataSource

        datasources_ = []
        
        if self.x_mitre_data_sources:
            for attack_obj in self.attack_objects['objects']:
                if attack_obj.get('type') == 'x-mitre-data-source':
                    ds_ = [d_ for d_ in self.x_mitre_data_sources if attack_obj.get('name') in d_]
                    if ds_:
                        datasources_.append(DataSource(self.attack_objects, self.relationships, self.id_lookup, **attack_obj))
        return datasources_

    #---------------------------------------------------------------------------------#
    # Return a list of Techniques to every Sub Technique object:
    #---------------------------------------------------------------------------------#

    @property
    def techniques(self):
        from .technique import Technique

        techniques_ = []

        if self.relationships.get(self.mid):
            for r_id in self.relationships.get(self.mid):
                if self.id_lookup.get(r_id):
                    if self.id_lookup.get(r_id).get('type') == 'attack-pattern' and self.id_lookup.get(r_id).get('x_mitre_is_subtechnique') == False:
                        techniques_.append(Technique(self.attack_objects, self.relationships, self.id_lookup, **self.id_lookup[r_id]))
        return techniques_

    #---------------------------------------------------------------------------------#
    # Access Groups for each Sub Technique object:
    #---------------------------------------------------------------------------------#

    @property
    def groups(self):
        from .group import Group

        groups_ = []

        if self.relationships.get(self.mid):
            for r_id in self.relationships.get(self.mid):
                if self.id_lookup.get(r_id) and self.id_lookup.get(r_id).get('type') == 'intrusion-set':
                        groups_.append(Group(self.attack_objects, self.relationships, self.id_lookup, **self.id_lookup[r_id]))
        return groups_

    #---------------------------------------------------------------------------------#
    # Access Tactics for each Sub Technique object:
    #---------------------------------------------------------------------------------#

    @property
    def tactics(self):

        tactics_ = []

        for technique in self.techniques:
            if technique.tactics:
                for tactic in technique.tactics:
                    tactics_.append(tactic)
        return tactics_
    
    #---------------------------------------------------------------------------------#
    # Access Mitigations for each Sub Technique object:
    #---------------------------------------------------------------------------------#

    @property
    def mitigations(self):
        from .mitigation import Mitigation

        mitigations_ = []

        if self.relationships.get(self.mid):
            for r_id in self.relationships.get(self.mid):
                if self.id_lookup.get(r_id) and self.id_lookup.get(r_id).get('type') == 'course-of-action':
                    mitigations_.append(Mitigation(self.attack_objects, self.relationships, self.id_lookup, **self.id_lookup[r_id]))

        return mitigations_
    
    #---------------------------------------------------------------------------------#
    # Return a json dict of the object:
    #---------------------------------------------------------------------------------#

    def to_json(self):
        try:
            return {
                "id": self.id,
                "mid": self.mid,
                "created": self.created,
                "modified": self.modified,
                "created_by_ref": self.created_by_ref,
                "object_marking_ref": self.object_marking_ref,
                "name": self.name,
                "type": self.type,
                "description": self.description,
                "url": self.url,
                "deprecated": self.deprecated,
                "revoked": self.revoked,
                "platforms": self.platforms,
                "permissions_required": self.permissions_required,
                "references": self.references,
                "techniques": [technique.name for technique in self.techniques],
                "tactics": [tactic.name for tactic in self.tactics],
                "mitigations": [mitigation.name for mitigation in self.mitigations],
                "groups": [group.name for group in self.groups],
                "datasources": [datasource.name for datasource in self.datasources]
            }
        except Exception as e:
            logging.error('Failed to jsonify object, error was: {}'.format(e))
            raise enterpriseattack.Error('Failed to create json object, error was: {}'.format(e))
    
    #---------------------------------------------------------------------------------#
    
    def __str__(self):
        return '{} Mitre Att&ck Sub Technique'.format(self.name)
    
    def __repr__(self):
        return '{} {}'.format(self.__class__, self.name)
