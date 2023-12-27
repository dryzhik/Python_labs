import aiohttp
import asyncio
import csv


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


async def main():
    base_url = 'http://127.0.0.1:8080/labs'
    csv_filename_all = 'labs.csv'
    csv_filename_single = 'lab.csv'

    new_lab_data = {
        'name': 'Lab1',
        'deadline': '01.01.2024',
        'description': 'Description for Lab1',
        'students': ['Ivanov', 'Petrov']
    }
    response_data, status = await send_request(base_url, method='POST', data=new_lab_data)
    if status // 100 == 2:
        print(f"Lab added successfully. URL: {response_data['url']}")
    else:
        print(f"Failed to add lab. Status: {status}, Reason: {response_data['error']}")

    edit_lab_data = {
        'deadline': '02.01.2024',
        'description': 'Updated description for Lab1'
    }
    edit_url = f"{base_url}/Lab1"
    response_data, status = await send_request(edit_url, method='PUT', data=edit_lab_data)
    if status // 100 == 2:
        print("Lab edited successfully.")
    else:
        print(f"Failed to edit lab. Status: {status}, Reason: {response_data['error']}")

    delete_url = f"{base_url}/Lab1"
    response_data, status = await send_request(delete_url, method='DELETE')
    if status // 100 == 2:
        print("Lab deleted successfully.")
    else:
        print(f"Failed to delete lab. Status: {status}, Reason: {response_data['error']}")

    single_lab_url = f"{base_url}/Lab1"
    response_data, status = await send_request(single_lab_url)
    if status // 100 == 2:
        print(f"Lab Data: {response_data}")
        with open(csv_filename_single, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Name', 'Deadline', 'Description'])
            csv_writer.writerow([response_data['name'], response_data['deadline'], response_data['description']])
    else:
        print(f"Failed to get lab data. Status: {status}, Reason: {response_data['error']}")

    new_lab2_data = {
        'name': 'Lab3',
        'deadline': '07.02.2024',
        'description': 'Description for Lab3',
        'students': ['Ivanov', 'Petrov']
    }
    response_data, status = await send_request(base_url, method='POST', data=new_lab2_data)
    if status // 100 == 2:
        print(f"Lab added successfully. URL: {response_data['url']}")
    else:
        print(f"Failed to add lab. Status: {status}, Reason: {response_data['error']}")

    all_labs_url = f"{base_url}/"
    response_data, status = await send_request(all_labs_url)
    if status // 100 == 2:
        print(f"All Labs Data: {response_data}")
        with open(csv_filename_all, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Student', 'Lab Name', 'Deadline', 'Description'])
            for lab in response_data:
                for i in range(len(lab['students'])):
                    csv_writer.writerow([lab['students'][i], lab['name'], lab['deadline'], lab['description']])
    else:
        print(f"Failed to get all labs data. Status: {status}, Reason: {response_data['error']}")


if __name__ == '__main__':
    asyncio.run(main())
