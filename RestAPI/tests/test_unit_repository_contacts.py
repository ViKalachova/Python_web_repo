import datetime
import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contacts import ContactSchema
from src.repository.contacts import get_contacts, get_all_contacts, get_contact, search_contact, \
    contacts_upcoming_birthdays, create_contact, update_contact, delete_contact


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, username='testuser', password='testpassword', confirmed=True)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(id=1, name='test', surname='test', email='test@gmail.com', phone='123456789', birthday='25.02.2000',
                    description='test', user=self.user),
            Contact(id=2, name='test', surname='test2', email='test2@gmail.com', phone='123456789',
                    birthday='25.02.1999',
                    description='test2', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(id=1, name='test', surname='test', email='test@gmail.com', phone='123456789', birthday='25.02.2000',
                    description='test', user=self.user),
            Contact(id=2, name='test', surname='test2', email='test2@gmail.com', phone='123456789',
                    birthday='25.02.1999',
                    description='test2', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact_id = 1
        contact = Contact(id=1, name='test', surname='test', email='test@gmail.com', phone='123456789',
                          birthday='25.02.2000', description='test', user=self.user)
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(contact_id, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_search_contact(self):
        query = 'test'
        contacts = [
            Contact(id=1, name='test', surname='test', email='test@gmail.com', phone='123456789', birthday='25.02.2000',
                    description='test', user=self.user),
            Contact(id=2, name='test', surname='test2', email='test2@gmail.com', phone='123456789',
                    birthday='25.02.1999',
                    description='test2', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await search_contact(query, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_contacts_upcoming_birthdays(self):
        contacts = [
            Contact(id=1, name='test', surname='test', email='test@gmail.com', phone='123456789', birthday='25.02.2000',
                    description='test', user=self.user),
            Contact(id=2, name='test', surname='test2', email='test2@gmail.com', phone='123456789',
                    birthday='27.02.1999',
                    description='test2', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await contacts_upcoming_birthdays(self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        test_birthday = datetime.date(2000, 2, 25)
        body = ContactSchema(name='test3', surname='test3', email='test3@gmail.com', phone='123456789',
                             birthday=test_birthday, description='test3')
        result = await create_contact(body, self.session, self.user)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)

    async def test_update_contact(self):
        contact_id = 1
        test_birthday = datetime.date(1999, 2, 25)
        body = ContactSchema(name='test4', surname='test4', email='test4@gmail.com', phone='123456789',
                             birthday=test_birthday, description='test4')
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, name='test', surname='test',
                                                                 email='test@gmail.com', phone='123456789',
                                                                 birthday='25.02.2000', description='test',
                                                                 user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await update_contact(contact_id, body, self.session, self.user)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)

    async def test_delete_contact(self):
        contact_id = 1
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, name='test', surname='test',
                                                                 email='test@gmail.com', phone='123456789',
                                                                 birthday='25.02.2000', description='test',
                                                                 user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(contact_id, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
