# Import your dependencies
from dotenv import load_dotenv
import os
from nylas import APIClient  # type: ignore
from nicegui import app, ui

# Add the assets folder as a local folder
app.add_static_files('/assets', 'assets')

# Load your env variables
load_dotenv()

# Initialize an instance of the Nylas SDK using the client credentials
nylas = APIClient(
    os.environ.get("CLIENT_ID"),
    os.environ.get("CLIENT_SECRET"),
    os.environ.get("ACCESS_TOKEN"),
)

# Dictionary to hold all contacts information
contact_info = {'id':'','given_name':'', 'surname':'', 'company_name':'',
                       'job_title':'', 'email':'', 'email_type':'', 'country':'', 'street_address':'',
                       'phone_number':'', 'phone_type':'', 'city':'', 'state':'', 'postal_code':'', 
                       'address_type':''}

# List to hold all contacts
contact_list = []

# Function to update a contact using our dictionary
def update_contact():
    contact = nylas.contacts.get(contact_info['id'])
    contact.given_name = contact_info['given_name']
    contact.surname = contact_info['surname']
    contact.company_name = contact_info['company_name']
    contact.job_title = contact_info['job_title']
    contact.emails[contact_info['email_type']] = [contact_info['email']]
    contact.phone_numbers[contact_info['phone_type']]  = [contact_info['phone_number']]
    if contact_info['street_address'] is not None or contact_info['street_address'] != '':
        contact.physical_addresses['Work'] = [{
                'format': 'structured',
                'city': contact_info['city'],
                'country': contact_info['country'],
                'state': contact_info['state'],
                'postal_code': contact_info['postal_code'],
                'type': contact_info['address_type'],
                'street_address': contact_info['street_address']}]
    try:
        # We try to save the contact
        contact.save()
        ui.notify('The contact was updated!')
    except Exception as e:
        # If the update fails, display the error message
        ui.notify(f'{e}')

# Update the dictionary with the updated values
def update_field(field, value):
    contact_info[f'{field}'] = value

# For each selected contact, bring the details
def fill_contact_details(contact_id):
    # Call the contacts endpoint
    contact = nylas.contacts.get(contact_id)
    contact_info['id'] = contact.id	
    picture = contact.get_picture()
    file_name = f'{contact.id}.png'
    profile_image = open(f'assets/{file_name}', 'wb')
    profile_image.write(picture.read())
    profile_image.close()
    profile_pic.set_source(f'assets/{file_name}')
    first_name.set_value(contact.given_name)
    try:
        contact_info['phone_number'] = list(contact.phone_numbers.values())[0][0]
        contact_info['phone_type'] = list(contact.phone_numbers)[0]
        phone_number.set_value(list(contact.phone_numbers.values())[0][0])
    except Exception as e:
        contact_info['phone_number'] = '123'
        contact_info['phone_type'] = 'Mobile'
        phone_number.set_value('123')
        print(f'{e}')
    contact_info['given_name'] = contact.given_name
    last_name.set_value(contact.surname)
    contact_info['surname'] = contact.surname
    company_name.set_value(contact.company_name)
    contact_info['company_name'] = contact.company_name
    job_title.set_value(contact.job_title)
    contact_info['job_title'] = contact.job_title
    try:
        contact_info['address_type'] = list(contact.physical_addresses.values())[0][0]["type"]
    except Exception as e:
        print(f'{e}')
        contact_info['address_type'] = ""
    try:
        email.set_value(list(contact.emails.values())[0][0])
        contact_info['email'] = list(contact.emails.values())[0][0]
        contact_info['email_type'] = list(contact.emails.keys())[0]
    except Exception as e:
        email.set_value("")
        contact_info['email'] = ''
        contact_info['email_type'] = ''
        print(f'{e}')
    try:
        country.set_value(list(contact.physical_addresses.values())[0][0]["country"])
        contact_info['country'] = list(contact.physical_addresses.values())[0][0]["country"]
    except Exception as e:
        country.set_value("")
        contact_info['country'] = ''
        print(f'{e}')
    try:
        address.set_value(list(contact.physical_addresses.values())[0][0]["street_address"])
        contact_info['street_address'] = list(contact.physical_addresses.values())[0][0]["street_address"]
    except Exception as e:
        address.set_value("")
        contact_info['street_address'] = ''
        print(f'{e}')
    try:
        city.set_value(list(contact.physical_addresses.values())[0][0]["city"])
        contact_info['city'] = list(contact.physical_addresses.values())[0][0]["city"]
    except Exception as e:
        city.set_value("")
        contact_info['city'] = ''
        print(f'{e}')
    try:
        state.set_value(list(contact.physical_addresses.values())[0][0]["state"])
        contact_info['state'] = list(contact.physical_addresses.values())[0][0]["state"]
    except Exception as e:
        state.set_value("")
        contact_info['state'] = ''
        print(f'{e}')
    try:
        postal_code.set_value(list(contact.physical_addresses.values())[0][0]["postal_code"])
        contact_info['postal_code'] = list(contact.physical_addresses.values())[0][0]["postal_code"]
    except Exception as e:
        postal_code.set_value("")
        contact_info['postal_code'] = ''
        print(f'{e}')
        
# Grab the first 5 contacts from the specified group
contacts = nylas.contacts.where(source = 'address_book', limit = 5, group = "517v55haghlcvnuu7lcm4f7k8")
# Loop all contacts and get the Id and Full Name
for contact in contacts:
    contact_list.append({'id': contact.id ,'full_name' : contact.given_name + " " + contact.surname})

# Build the UI
with ui.row():
    with ui.column():
        # Define the table as an AG Grid
        grid = ui.aggrid({
            'columnDefs': [
                {'headerName': 'Id', 'field': 'id', 'hide': True},
                {'headerName': 'Contact Name', 'field': 'full_name', 'checkboxSelection': True},
            ],
            'rowData': 
                contact_list,
            'rowSelection': 'simple',
        }).classes('h-45 w-80')

        # When we select a contact and press "Update"
        async def output_selected_row():
            row = await grid.get_selected_row()
            if row:
                fill_contact_details(row['id'])
            else:
                pass

        # The update button
        ui.button('Update', on_click=output_selected_row)
    
    # Form to display the updatable fields
    with ui.column():
        profile_pic = ui.image()
        first_name = ui.input(label='First Name', placeholder='First Name', on_change = lambda e: update_field('given_name', e.value))
        last_name = ui.input(label='Last Name', placeholder='Surname', on_change = lambda e: update_field('surname', e.value))
        company_name = ui.input(label='Company Name', placeholder='Company Name', on_change = lambda e: update_field('company_name', e.value))
        job_title = ui.input(label='Job Title', placeholder='Job Title', on_change = lambda e: update_field('job_title', e.value))
        email = ui.input(label='Email', placeholder='Email', on_change = lambda e: update_field('email', e.value))
        phone_number = ui.input(label='Phone Number', placeholder='Phone Number', on_change = lambda e: update_field('phone_number', e.value))        
        country = ui.input(label='Country', placeholder='Country', on_change = lambda e: update_field('country', e.value))
        address = ui.input(label='Address', placeholder='Address', on_change = lambda e: update_field('street_address', e.value))
        city = ui.input(label='City', placeholder='City', on_change = lambda e: update_field('city', e.value))
        state = ui.input(label='State', placeholder='State', on_change = lambda e: update_field('state', e.value))
        postal_code = ui.input(label='Postal Code', placeholder='Postal Code', on_change = lambda e: update_field('postal_code', e.value))
        # Submit button
        ui.button('Submit', on_click=update_contact)

# Run our application
ui.run(title = 'NiceGUI Contacts')
