from django.views import View

from categories.models import Vehicle


def format_duns(text):
    return str(text).zfill(9)


def get_vehicle_name(id):
    vehicle = Vehicle.objects.get(id=id)
    
    if vehicle:
        return vehicle.name
    
    return ''


def get_memberships(vendor):
    membership_map = {}
    
    for membership in vendor.pools.all():
        piid = membership.piid
        vehicle_id = membership.pool.vehicle.id
        vehicle_name = get_vehicle_name(vehicle_id)
        pool_id = membership.pool.id
        pool_number = membership.pool.number
        
        contacts = membership.contacts.all()
        contact_name = contacts[0].name
        contact_phone = ",".join(contacts[0].phones.all().values_list('number', flat=True))
        contact_email = ",".join(contacts[0].emails.all().values_list('address', flat=True))
        
        if piid not in membership_map:
            membership_map[piid] = {
                'vehicle_ids': [],
                'vehicle_names': [],
                'pool_ids': [],
                'pool_numbers': [],
                'zones': [],
                'contacts': [],
                'phones': [],
                'emails': [],
                'setasides': [],
                'reference': membership
            }
            
        if vehicle_id not in membership_map[piid]['vehicle_ids']:
            membership_map[piid]['vehicle_ids'].append(vehicle_id)
            membership_map[piid]['vehicle_names'].append(vehicle_name)
            
        if pool_id not in membership_map[piid]['pool_ids']:
            membership_map[piid]['pool_ids'].append(pool_id)
            membership_map[piid]['pool_numbers'].append(pool_number)
        
        for zone in membership.zones.all():    
            if str(zone.id) not in membership_map[piid]['zones']:
                membership_map[piid]['zones'].append(str(zone.id))
            
        if contact_name not in membership_map[piid]['contacts']:
            membership_map[piid]['contacts'].append(contact_name)
            
        if contact_phone not in membership_map[piid]['phones']:
            membership_map[piid]['phones'].append(contact_phone)
            
        if contact_email not in membership_map[piid]['emails']:
            membership_map[piid]['emails'].append(contact_email)
            
        for setaside in membership.setasides.all():
            if setaside.code not in membership_map[piid]['setasides']:
                membership_map[piid]['setasides'].append(setaside.code)
            
    return membership_map
 
 
def get_membership_name(membership_map, piid):
    info = membership_map[piid]
    vehicles = sorted(info['vehicle_names'])
    
    def sort_key(name):
        try:
            return int(name)
        except Exception:
            return name
    
    pools = sorted(info['pool_numbers'], key=sort_key)
    zones = sorted(info['zones'], key=sort_key)
    
    name = ",".join(vehicles) + ' (Service categories: ' + ",".join(pools) + ') '

    if len(info['zones']):
        name += ' (Zones: ' + ",".join(zones) + ')'
    
    return name.strip()


class BaseCSVView(View):
    
    def get_param(self, name, default = None):
        if name in self.request.GET:
            return self.request.GET[name]
        
        return default
    
    def get_params(self, name, default = []):
        if name in self.request.GET:
            return self.request.GET[name].split(',')
        
        return default

