import aiohttp
import asyncio
import csv
import argparse


async def send_request(url, method='GET', data=None):
    async with aiohttp.ClientSession() as session:
        if method == 'GET':
            async with session.get(url) as response:
                return await response.json(), response.status
        elif method == 'POST':
            async with session.post(url, json=data) as response:
                return await response.json(), response.status
        elif method == 'PUT':
            async with session.put(url, json=data) as response:
                return await response.json(), response.status
        elif method == 'DELETE':
            async with session.delete(url) as response:
                return None, response.status


async def create_new_lab(name, deadline, description, students):
    base_url = 'http://127.0.0.1:8080/labs'
    new_lab_data = {
        'name': name,
        'deadline': deadline,
        'description': description,
        'students': students
    }
    response_data, status = await send_request(base_url, method='POST', data=new_lab_data)
    if status // 100 == 2:
        print(f"Lab added successfully. URL: {response_data['url']}")
    else:
        print(f"Failed to add lab. Status: {status}, Reason: {response_data['error']}")


async def edit_lab(name, deadline, description, students):
    base_url = f'http://127.0.0.1:8080/labs/{name}'
    edit_lab_data = {
        'deadline': deadline,
        'description': description,
        'students': students
    }
    response_data, status = await send_request(base_url, method='PUT', data=edit_lab_data)
    if status // 100 == 2:
        print("Lab edited successfully.")
    else:
        print(f"Failed to edit lab. Status: {status}, Reason: {response_data['error']}")


async def delete_lab(name):
    base_url = f'http://127.0.0.1:8080/labs/{name}'
    response_data, status = await send_request(base_url, method='DELETE')
    if status // 100 == 2:
        print("Lab deleted successfully.")
    else:
        print(f"Failed to delete lab. Status: {status}, Reason: {response_data['error']}")


async def get_lab(name, csv_filename):
    base_url = f'http://127.0.0.1:8080/labs/{name}'
    response_data, status = await send_request(base_url)
    if status // 100 == 2:
        print(f"Lab Data: {response_data}")
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Name', 'Deadline', 'Description'])
            csv_writer.writerow([response_data['name'], response_data['deadline'], response_data['description']])
    else:
        print(f"Failed to get lab data. Status: {status}, Reason: {response_data['error']}")


async def get_all_labs(csv_filename):
    base_url = f'http://127.0.0.1:8080/labs/'
    response_data, status = await send_request(base_url)
    if status // 100 == 2:
        print(f"All Labs Data: {response_data}")
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Student', 'Lab Name', 'Deadline', 'Description'])
            for lab in response_data:
                for i in range(len(lab['students'])):
                    csv_writer.writerow([lab['students'][i], lab['name'], lab['deadline'], lab['description']])
    else:
        print(f"Failed to get all labs data. Status: {status}, Reason: {response_data['error']}")


async def main():
    parser = argparse.ArgumentParser(description='Lab Client')
    parser.add_argument('command', choices=['new_lab', 'edit_lab', 'delete_lab', 'get_lab', 'get_all_labs'],
                        help='The command to execute')
    parser.add_argument('--name', help='Lab name')
    parser.add_argument('--deadline', help='Lab deadline')
    parser.add_argument('--description', help='Lab description')
    parser.add_argument('--students', nargs='+', help='List of students')

    args = parser.parse_args()
    if args.command == 'new_lab':
        await create_new_lab(args.name, args.deadline, args.description, args.students)
    elif args.command == 'edit_lab':
        await edit_lab(args.name, args.deadline, args.description, args.students)
    elif args.command == 'delete_lab':
        await delete_lab(args.name)
    elif args.command == 'get_lab':
        await get_lab(args.name, args.name + '.csv')
    elif args.command == 'get_all_labs':
        await get_all_labs(args.name + '.csv')


if __name__ == '__main__':
    asyncio.run(main())
