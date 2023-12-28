from aiohttp import web
import json
from datetime import datetime

app = web.Application()

lab_schedule = {}


async def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False


async def create_lab(request):
    try:
        data = await request.json()
        lab_name = data.get('name')
        deadline = data.get('deadline')
        description = data.get('description', '')
        students = data.get('students', [])

        if not lab_name or not deadline:
            return web.json_response({'error': 'Name and deadline are required'}, status=400)

        if lab_name in lab_schedule:
            return web.json_response({'error': 'Lab with this name already exists'}, status=400)

        if not await validate_date(deadline):
            return web.json_response({'error': 'Invalid date format. Use dd.mm.yyyy'}, status=400)

        lab_schedule[lab_name] = {
            'name': lab_name,
            'deadline': deadline,
            'description': description,
            'students': students
        }

        url = f'http://{request.host}/labs/{lab_name}'
        headers = {'Location': url}
        return web.json_response({'url': url}, headers=headers, status=201)
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON format'}, status=400)


async def update_lab(request):
    lab_name = request.match_info['name']

    if lab_name not in lab_schedule:
        return web.json_response({'error': 'Lab not found'}, status=404)

    try:
        data = await request.json()
        deadline = data.get('deadline')
        description = data.get('description', '')
        students = data.get('students', [])

        if not await validate_date(deadline):
            return web.json_response({'error': 'Invalid date format. Use dd.mm.yyyy'}, status=400)

        lab_schedule[lab_name]['deadline'] = deadline
        lab_schedule[lab_name]['description'] = description
        lab_schedule[lab_name]['students'] = students

        return web.json_response(lab_schedule[lab_name])
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON format'}, status=400)


async def delete_lab(request):
    lab_name = request.match_info['name']

    if lab_name not in lab_schedule:
        return web.json_response({'error': 'Lab not found'}, status=404)

    lab_schedule.pop(lab_name)
    return web.Response(status=204)


async def get_lab(request):
    lab_name = request.match_info['name']

    if lab_name not in lab_schedule:
        return web.json_response({'error': 'Lab not found'}, status=404)

    return web.json_response(lab_schedule[lab_name])


async def get_all_labs(request):
    return web.json_response(list(lab_schedule.values()))


app.router.add_post('/labs', create_lab)
app.router.add_put('/labs/{name}', update_lab)
app.router.add_delete('/labs/{name}', delete_lab)
app.router.add_get('/labs/{name}', get_lab)
app.router.add_get('/labs/', get_all_labs)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
