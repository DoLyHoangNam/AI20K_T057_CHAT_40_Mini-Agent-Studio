import urllib.request
import urllib.parse
import json

base_url = 'http://localhost:8080'

# 1. Login lấy Admin token
data = urllib.parse.urlencode({
    'client_id': 'admin-cli',
    'username': 'admin',
    'password': 'admin123',
    'grant_type': 'password'
}).encode()

req = urllib.request.Request(f'{base_url}/realms/master/protocol/openid-connect/token', data=data)
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read().decode())['access_token']

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 2. Lấy ID của client mini-agent-studio-app
req = urllib.request.Request(f'{base_url}/admin/realms/mini-agent-platform/clients?clientId=mini-agent-studio-app', headers=headers)
with urllib.request.urlopen(req) as resp:
    clients = json.loads(resp.read().decode())
    client_uuid = clients[0]['id']

# 3. Tạo Protocol Mappers cho tenant_id và department
mappers = [
    {
        'name': 'tenant_id_mapper',
        'protocol': 'openid-connect',
        'protocolMapper': 'oidc-usermodel-attribute-mapper',
        'consentRequired': False,
        'config': {
            'user.attribute': 'tenant_id',
            'claim.name': 'tenant_id',
            'jsonType.label': 'String',
            'id.token.claim': 'true',
            'access.token.claim': 'true',
            'userinfo.token.claim': 'true'
        }
    },
    {
        'name': 'department_mapper',
        'protocol': 'openid-connect',
        'protocolMapper': 'oidc-usermodel-attribute-mapper',
        'consentRequired': False,
        'config': {
            'user.attribute': 'department',
            'claim.name': 'department',
            'jsonType.label': 'String',
            'id.token.claim': 'true',
            'access.token.claim': 'true',
            'userinfo.token.claim': 'true'
        }
    }
]

for m in mappers:
    try:
        req = urllib.request.Request(f'{base_url}/admin/realms/mini-agent-platform/clients/{client_uuid}/protocol-mappers/models', data=json.dumps(m).encode(), headers=headers)
        urllib.request.urlopen(req)
        print('Created Mapper:', m['name'])
    except Exception as e:
        print('Mapper exists or error:', e)

# 4. Lấy thông tin các roles để gán
req = urllib.request.Request(f'{base_url}/admin/realms/mini-agent-platform/roles', headers=headers)
with urllib.request.urlopen(req) as resp:
    roles_list = json.loads(resp.read().decode())
    roles_dict = {r['name']: r for r in roles_list}

# 5. Danh sách User mẫu
users_to_create = [
    {
        'username': 'superadmin@platform.vn',
        'email': 'superadmin@platform.vn',
        'firstName': 'Super',
        'lastName': 'Admin',
        'enabled': True,
        'credentials': [{'type': 'password', 'value': 'super123', 'temporary': False}],
        'attributes': {'tenant_id': ['PLATFORM'], 'department': ['Executive']},
        'role': 'SUPER_ADMIN'
    },
    {
        'username': 'admin@vinfast.vn',
        'email': 'admin@vinfast.vn',
        'firstName': 'Admin',
        'lastName': 'VinFast',
        'enabled': True,
        'credentials': [{'type': 'password', 'value': 'admin123', 'temporary': False}],
        'attributes': {'tenant_id': ['VINFAST'], 'department': ['HR']},
        'role': 'TENANT_ADMIN'
    },
    {
        'username': 'nam.dlh@vinfast.vn',
        'email': 'nam.dlh@vinfast.vn',
        'firstName': 'Đỗ Lý Hoàng',
        'lastName': 'Nam',
        'enabled': True,
        'credentials': [{'type': 'password', 'value': '123456', 'temporary': False}],
        'attributes': {'tenant_id': ['VINFAST'], 'department': ['Production']},
        'role': 'EMPLOYEE'
    },
    {
        'username': 'vng.admin@gmail.com',
        'email': 'vng.admin@gmail.com',
        'firstName': 'Admin',
        'lastName': 'VNG Games',
        'enabled': True,
        'credentials': [{'type': 'password', 'value': '123456', 'temporary': False}],
        'attributes': {'tenant_id': ['VNG'], 'department': ['Game Studio']},
        'role': 'TENANT_ADMIN'
    }
]

for u in users_to_create:
    role_name = u.pop('role')
    username = u['username']
    try:
        req = urllib.request.Request(f'{base_url}/admin/realms/mini-agent-platform/users', data=json.dumps(u).encode(), headers=headers)
        urllib.request.urlopen(req)
        print('Created user:', username)
    except Exception as e:
        print('User may exist:', username, e)
        
    try:
        # Lấy ID user vừa tạo để gán role
        encoded_user = urllib.parse.quote(username)
        req = urllib.request.Request(f'{base_url}/admin/realms/mini-agent-platform/users?username={encoded_user}', headers=headers)
        with urllib.request.urlopen(req) as resp:
            u_id = json.loads(resp.read().decode())[0]['id']
            
        role_obj = roles_dict[role_name]
        req = urllib.request.Request(f'{base_url}/admin/realms/mini-agent-platform/users/{u_id}/role-mappings/realm', data=json.dumps([role_obj]).encode(), headers=headers)
        urllib.request.urlopen(req)
        print(f'Assigned role {role_name} to {username}')
    except Exception as e:
        print('Role assign error for:', username, e)

print('=== ALL KEYCLOAK SEEDING COMPLETED SUCCESSFULLY ===')
